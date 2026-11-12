"""Motor de vídeos Me ContAI (v2): MAIA + narração ElevenLabs + legendas sincronizadas.

Uso típico (num script de vídeo):
    from motor import render
    CENAS = [dict(tipo="gancho", fala="...", titulo="VOCÊ SABIA?"),
             dict(tipo="fato", fala="...", titulo="...", desenho=funcao(d, img, t, T), fundo=((r,g,b),(r,g,b))),
             dict(tipo="cta", fala="...", titulo="SEGUE PRA MAIS!")]
    render(CENAS, "saida.mp4")
desenho(d, img, t, T): desenha a ilustração do tema (t = tempo na cena, T = tempo total).
"""
import base64, json, math, os, subprocess, wave, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from maia import maia_pose
import idioma
from idioma import tr

W, H, FPS = 1080, 1920, 30
SR = 44100
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
VOZ_ALICE = "xMGbstDe7gGBMg3DqxOc"
NAVY1, NAVY2 = (12, 22, 58), (26, 44, 104)
CIANO, AMARELO = (35, 210, 225), (255, 196, 30)
_fonts = {}


def fnt(s):
    if s not in _fonts: _fonts[s] = ImageFont.truetype(FONT, s)
    return _fonts[s]


def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3


def pop(t):
    if t <= 0: return 0
    if t >= 1: return 1
    return ease(t) + 0.25 * math.sin(t * math.pi * 2.5) * (1 - t)


# ---------------- voz ----------------
def tts(texto, voz=VOZ_ALICE, cache_dir="_cache_voz"):
    """Retorna (pcm float32 mono 44.1k, lista de palavras [(palavra, ini, fim)])."""
    os.makedirs(cache_dir, exist_ok=True)
    if voz.startswith("kokoro:"):
        return tts_kokoro(texto, voz.split(":", 1)[1], cache_dir)
    import hashlib
    vel = idioma.conf().get("velocidade", 1.0)
    h = hashlib.md5((voz + texto + (f"@{vel}" if vel != 1.0 else "")).encode()).hexdigest()[:16]
    jpath = os.path.join(cache_dir, h + ".json")
    if not os.path.exists(jpath):
        key = open(os.path.expanduser("~/.secrets/elevenlabs")).read().strip()
        body = json.dumps({"text": texto, "model_id": "eleven_multilingual_v2",
                           "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35,
                                              **({"speed": vel} if vel != 1.0 else {})}}).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format=mp3_44100_128",
            data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(jpath, "wb").write(r.read())
    data = json.load(open(jpath))
    mp3 = os.path.join(cache_dir, h + ".mp3")
    open(mp3, "wb").write(base64.b64decode(data["audio_base64"]))
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp3, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    pcm = np.frombuffer(raw, dtype=np.float32).copy()
    al = data["alignment"]
    palavras, cur, ini = [], "", None
    for ch, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur: palavras.append((cur, ini, fim)); cur = ""
        else:
            if not cur: ini = a
            cur += ch; fim = b
    if cur: palavras.append((cur, ini, fim))
    return pcm, palavras


# ---------------- voz gratuita (Kokoro, código aberto, Apache-2.0) ----------------
KOKORO_DIR = os.path.expanduser(os.environ.get("KOKORO_DIR", "~/kokoro"))
KOKORO_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
_kokoro = None


def _kokoro_modelo():
    """Carrega o Kokoro (baixa o modelo na 1ª vez; requer: pip install kokoro-onnx soundfile)."""
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        os.makedirs(KOKORO_DIR, exist_ok=True)
        for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
            p = os.path.join(KOKORO_DIR, f)
            if not os.path.exists(p) or os.path.getsize(p) < 1e6:
                urllib.request.urlretrieve(KOKORO_URL + f, p)
        _kokoro = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.onnx"), os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    return _kokoro


def _apara(s, sr, lim=0.012):
    """Remove silêncio do começo e do fim (deixa 30 ms de folga)."""
    idx = np.where(np.abs(s) > lim)[0]
    if not len(idx): return s
    a, b = max(0, idx[0] - int(0.03 * sr)), min(len(s), idx[-1] + int(0.03 * sr))
    return s[a:b]


def tts_kokoro(texto, spec, cache_dir):
    """spec = "voz@lang" (ex.: ef_dora@es). Gera a fala por trechos (vírgula/ponto) e
    estima o tempo de cada palavra proporcionalmente às letras dentro do trecho."""
    import hashlib, re
    vel = idioma.conf().get("velocidade", 1.0)
    h = hashlib.md5(f"kokoro|{spec}|{vel}|{texto}".encode()).hexdigest()[:16]
    wav, jp = os.path.join(cache_dir, h + ".wav"), os.path.join(cache_dir, h + ".words.json")
    if not os.path.exists(jp):
        voz, lang = spec.split("@")
        k = _kokoro_modelo()
        trechos = [t.strip() for t in re.findall(r"[^,.!?;:]+[,.!?;:…]*", texto) if t.strip()]
        partes, palavras, t0 = [], [], 0.0
        for tr_ in trechos:
            s, sr = k.create(tr_, voice=voz, speed=vel, lang=lang)
            s = _apara(np.asarray(s, dtype=np.float32), sr)
            if sr != SR:
                raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                                      "-f", "f32le", "-ar", str(SR), "-"], input=s.tobytes(), capture_output=True, check=True).stdout
                s = np.frombuffer(raw, dtype=np.float32).copy()
            dur = len(s) / SR
            ws = tr_.split(); pesos = [len(w) + 2 for w in ws]; tot = sum(pesos); acc = 0
            for w, p in zip(ws, pesos):
                a = t0 + dur * acc / tot; acc += p
                palavras.append((w, a, t0 + dur * acc / tot))
            pausa = 0.32 if tr_[-1] in ".!?…" else (0.16 if tr_[-1] in ",;:" else 0.08)
            partes += [s, np.zeros(int(SR * pausa), dtype=np.float32)]
            t0 += dur + pausa
        pcm = np.concatenate(partes[:-1]) if partes else np.zeros(1, dtype=np.float32)
        pcm = pcm / max(1e-9, np.abs(pcm).max()) * 0.9
        with wave.open(wav, "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(pcm, -1, 1) * 32767).astype(np.int16).tobytes())
        json.dump(palavras, open(jp, "w"))
    with wave.open(wav) as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767
    return pcm, [tuple(p) for p in json.load(open(jp))]


def envelope(pcm, n_frames):
    """Abertura da boca 0..1 por quadro, a partir do volume da voz."""
    hop = SR // FPS
    out = np.zeros(n_frames)
    for i in range(n_frames):
        seg = pcm[i * hop:(i + 1) * hop]
        if len(seg): out[i] = np.sqrt(np.mean(seg ** 2))
    if out.max() > 0: out = out / np.percentile(out[out > 0], 90)
    out = np.clip((out - 0.12) * 1.3, 0, 1)
    sm = out.copy()  # suaviza
    for i in range(1, len(sm)): sm[i] = 0.55 * out[i] + 0.45 * sm[i - 1]
    return sm


# ---------------- desenho ----------------
def fundo(d, T, c1, c2, estrelas=True):
    for y in range(0, H, 8):
        k = y / H
        d.rectangle([0, y, W, y + 8], fill=tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3)))
    if estrelas:
        rng = np.random.default_rng(3)
        for i in range(40):
            x, y0, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6)
            y = (y0 - T * rng.uniform(10, 40)) % H
            a = 0.5 + 0.5 * math.sin(T * 3 + i)
            c = tuple(int(255 * (0.5 + 0.5 * a)) for _ in range(3))
            d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def texto(img, s, y, size, t_in, t, cor=(255, 255, 255), borda=(10, 15, 40), maxw=960):
    s = tr(s)
    if t < t_in: return
    sc = pop((t - t_in) / 0.45)
    if sc <= 0.02: return
    f = fnt(size)
    pal, linhas, cur = s.split(), [], ""
    for p in pal:
        tst = (cur + " " + p).strip()
        if f.getlength(tst) > maxw and cur: linhas.append(cur); cur = p
        else: cur = tst
    linhas.append(cur)
    lh = int(size * 1.12)
    layer = Image.new("RGBA", (W, lh * len(linhas) + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, l in enumerate(linhas):
        ld.text((W // 2, 20 + i * lh), l, font=f, fill=cor, anchor="ma", stroke_width=max(4, size // 9), stroke_fill=borda)
    nw, nh = max(1, int(layer.width * sc)), max(1, int(layer.height * sc))
    layer = layer.resize((nw, nh), Image.BILINEAR)
    img.alpha_composite(layer, ((W - nw) // 2, int(y - nh / 2)))


def legenda(img, palavras, t, y):
    """Mostra grupos de até 3 palavras; a palavra falada fica amarela."""
    grupos = [palavras[i:i + 3] for i in range(0, len(palavras), 3)]
    g = None
    for gr in grupos:
        if gr[0][1] - 0.05 <= t <= gr[-1][2] + 0.25: g = gr
    if not g: return
    partes = [p[0].upper() for p in g]
    ativos = [a - 0.03 <= t <= b + 0.08 for (_, a, b) in g]
    base = 74
    while True:
        fs = [fnt(int(base * (1.12 if at else 1))) for at in ativos]
        total = sum(f.getlength(p) for f, p in zip(fs, partes)) + 24 * (len(partes) - 1)
        if total <= 940 or base <= 50: break
        base -= 4
    x = (W - total) / 2
    d = ImageDraw.Draw(img)
    pad = 26
    d.rounded_rectangle([x - pad, y - 58, x + total + pad, y + 58], 28, fill=(10, 15, 40, 170))
    for txt, ff, at in zip(partes, fs, ativos):
        d.text((x, y), txt, font=ff, fill=AMARELO if at else (255, 255, 255), anchor="lm",
               stroke_width=7, stroke_fill=(10, 15, 40))
        x += ff.getlength(txt) + 24


def marca(d):
    nome = idioma.conf()["marca"]
    w = max(300, int(fnt(40).getlength(nome)) + 110)
    d.rounded_rectangle([30, 40, 30 + w, 110], 34, fill=(10, 15, 40), outline=CIANO, width=4)
    d.text((30 + (w - 40) / 2, 75), nome, font=fnt(40), fill=(255, 255, 255), anchor="mm")
    d.ellipse([w - 10, 52, w + 16, 78], fill=AMARELO)


# ---------------- render ----------------
def render(cenas, saida, voz=None):
    voz = voz or idioma.conf()["voz"]
    tmpdir = os.path.dirname(os.path.abspath(saida))
    vozes, total = [], 0.0
    for c in cenas:
        pcm, pal = tts(c["fala"], voz)
        dur = len(pcm) / SR + c.get("pausa", 0.45)
        c["_pcm"], c["_pal"], c["_dur"], c["_ini"] = pcm, pal, dur, total
        total += dur
    arquivos = []
    for idx, c in enumerate(cenas):
        n = int(round(c["_dur"] * FPS))
        env = envelope(c["_pcm"], n)
        tmp = os.path.join(tmpdir, f"_c{idx}.tmp.mp4"); fin = os.path.join(tmpdir, f"_c{idx}.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "23", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for f in range(n):
            t = f / FPS; T = c["_ini"] + t
            p.stdin.write(frame(c, t, T, env[f], total).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.replace(tmp, fin)
        arquivos.append(fin)
    lst = os.path.join(tmpdir, "_lista.txt")
    open(lst, "w").writelines(f"file '{a}'\n" for a in arquivos)
    wav = os.path.join(tmpdir, "_audio.wav"); audio(cenas, total, wav)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", saida], check=True)
    for a in arquivos + [lst, wav]: os.remove(a)
    return total


def frame(c, t, T, boca, total):
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img, "RGBA")
    tp = c["tipo"]
    if tp in ("gancho", "cta"):
        c1, c2 = c.get("fundo", (NAVY1, NAVY2))
        fundo(d, T, c1, c2)
        # anel ciano atrás da MAIA
        if not c.get("desenho"):
            r = 430 + math.sin(T * 2) * 10
            d.ellipse([W / 2 - r, 1180 - r, W / 2 + r, 1180 + r], outline=CIANO, width=14)
        if c.get("desenho"):  # abertura com o desenho do tema + MAIA menor
            c["desenho"](d, img, t, T)
            m = maia_pose(T, boca, escala=0.62)
            img.alpha_composite(m, (-10, H - m.height + 30))
        else:
            m = maia_pose(T, boca, escala=1.05)
            s = ease(t / 0.5) if tp == "gancho" and c["_ini"] == 0 else 1
            y = 860 + int((1 - s) * 500)
            img.alpha_composite(m, ((W - m.width) // 2, y))
        tam = 140 if len(tr(c["titulo"])) <= 16 else 96
        texto(img, c["titulo"], 300 if tam == 140 else 290, tam, 0.15, t, cor=AMARELO if tp == "cta" else (255, 255, 255))
        if c.get("subtitulo"): texto(img, c["subtitulo"], 560, 56, 0.6, t, cor=CIANO)
        legenda(img, c["_pal"], t, 1330 if c.get("desenho") else 720)
    else:
        c1, c2 = c.get("fundo", (NAVY1, NAVY2))
        fundo(d, T, c1, c2, estrelas=c.get("estrelas", False))
        c["desenho"](d, img, t, T)
        texto(img, c["titulo"], 300, 104, 0.1, t)
        legenda(img, c["_pal"], t, 1330)
        m = maia_pose(T, boca, escala=0.5)  # MAIA pequena no canto, comentando
        img.alpha_composite(m, (W - m.width + 20, H - m.height + 40))
    marca(ImageDraw.Draw(img))
    dd = ImageDraw.Draw(img)
    dd.rectangle([0, H - 12, int(W * T / total), H], fill=CIANO)
    return img.convert("RGB")


def audio(cenas, total, path):
    out = np.zeros(int(SR * total) + SR)
    for c in cenas:  # narração
        s = int(c["_ini"] * SR); out[s:s + len(c["_pcm"])] += c["_pcm"]
    trilha = np.zeros_like(out)  # trilha leve (ukulele)
    def pluck(freq, dur=0.9):
        n = int(SR * dur); N = int(SR / freq)
        buf = np.random.default_rng(int(freq)).uniform(-1, 1, N); y = np.zeros(n)
        for i in range(n):
            y[i] = buf[i % N]; buf[i % N] = 0.996 * 0.5 * (buf[i % N] + buf[(i + 1) % N])
        return y
    notas = {"C": 261.6, "D": 293.7, "E": 329.6, "F": 349.2, "G": 392.0, "A": 440.0, "B": 493.9, "c": 523.3}
    acordes = [("C", "E", "G"), ("A", "C", "E"), ("F", "A", "c"), ("G", "B", "D")]
    beat, cache, t, k = 60 / 112, {}, 0.0, 0
    while t < total - 0.3:
        ac = acordes[(k // 4) % 4]; nota = ac[k % 3]
        f = notas[nota] * (0.5 if k % 4 == 0 else 1)
        if f not in cache: cache[f] = pluck(f)
        s = int(t * SR); y = cache[f][: len(trilha) - s]; trilha[s:s + len(y)] += y
        t += beat / 2; k += 1
    trilha = trilha / max(1e-9, np.abs(trilha).max())
    out = out / max(1e-9, np.abs(out).max()) * 0.9 + trilha * 0.12
    n = int(SR * total); out = out[:n]
    fade = int(SR * 0.6); out[-fade:] *= np.linspace(1, 0, fade)
    out = np.clip(out, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
