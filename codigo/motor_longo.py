"""Motor do VÍDEO LONGO (horizontal 1920x1080) da MAIA.

Reaproveita a voz, a trilha e a MAIA do motor dos Shorts (motor.py, que continua vertical e
não é alterado). Cada cena é um dict:
    dict(tipo="abre"|"fato"|"ficha"|"gancho"|"cta", fala="...", titulo="...", ...)
Campos:
  - item: número do item da lista (mostra o selo "#7" e entra nos capítulos)
  - nome: nome do item (vai para os capítulos e para a cena "abre")
  - vert: função de desenho VERTICAL dos Shorts (d, img, t, T); é desenhada numa tela
          1080x1920, recortada (recorte=(y0, y1), padrão 360–1290) e ampliada num painel.
  - desenho: função de desenho HORIZONTAL nativa (d, img, t, T) em 1920x1080 (opcional).
  - fundo: cores (c1, c2) do degradê.
  - numero / rotulo_num / sufixo: cena "ficha" (um número gigante contando + legenda).
Uso: render_longo(CENAS, "saida.mp4") -> (duração, capítulos[(segundos, texto)])
"""
import math, os, subprocess, multiprocessing as mp
import numpy as np
from PIL import Image, ImageDraw
import motor
from motor import tts, envelope, audio, escolher_voz, fnt, pop, ease, limpa_emoji, SR, AMARELO, CIANO, NAVY1, NAVY2
from maia import maia_pose
import idioma
from idioma import tr

W, H = 1920, 1080
FPS = int(os.environ.get("MAIA_FPS_LONGO", "30"))
ESCURO = (10, 15, 40)
PAINEL = (40, 140, 990, 1010)  # x0, y0, x1, y1 do painel do desenho (lado esquerdo)
_grad = {}


def degrade(c1, c2, w=W, h=H):
    k = (c1, c2, w, h)
    if k not in _grad:
        a = np.linspace(0, 1, h)[:, None, None]
        arr = (np.array(c1)[None, None, :] * (1 - a) + np.array(c2)[None, None, :] * a)
        arr = np.repeat(arr, w, axis=1).astype(np.uint8)
        _grad[k] = Image.fromarray(arr, "RGB").convert("RGBA")
    return _grad[k].copy()


def estrelas(d, T, w=W, h=H, n=50):
    rng = np.random.default_rng(3)
    for i in range(n):
        x, y0, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(2, 5)
        y = (y0 - T * rng.uniform(8, 30)) % h
        a = 0.5 + 0.5 * math.sin(T * 3 + i)
        c = tuple(int(255 * (0.5 + 0.5 * a)) for _ in range(3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def texto(img, s, cx, y, size, t_in, t, cor=(255, 255, 255), maxw=820, anchor_x="m"):
    """Texto com quebra de linha, entrando com 'pop'. cx = centro (ou esquerda se anchor_x='l')."""
    s = limpa_emoji(tr(s))
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
    lw = int(max(f.getlength(l) for l in linhas)) + 60
    layer = Image.new("RGBA", (lw, lh * len(linhas) + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, l in enumerate(linhas):
        if anchor_x == "l":
            ld.text((30, 20 + i * lh), l, font=f, fill=cor, anchor="la", stroke_width=max(4, size // 9), stroke_fill=ESCURO)
        else:
            ld.text((lw // 2, 20 + i * lh), l, font=f, fill=cor, anchor="ma", stroke_width=max(4, size // 9), stroke_fill=ESCURO)
    nw, nh = max(1, int(layer.width * sc)), max(1, int(layer.height * sc))
    layer = layer.resize((nw, nh), Image.BILINEAR)
    x = int(cx - 30) if anchor_x == "l" else int(cx - nw / 2)
    img.alpha_composite(layer, (x, int(y - nh / 2)))


def legenda(img, palavras, t, cx=W // 2, y=1000, maxw=1500):
    """Grupos de até 4 palavras; a palavra falada fica amarela."""
    grupos = [palavras[i:i + 4] for i in range(0, len(palavras), 4)]
    g = None
    for gr in grupos:
        if gr[0][1] - 0.05 <= t <= gr[-1][2] + 0.25: g = gr
    if not g: return
    partes = [p[0].upper() for p in g]
    ativos = [a - 0.03 <= t <= b + 0.08 for (_, a, b) in g]
    base = 60
    while True:
        fs = [fnt(int(base * (1.1 if at else 1))) for at in ativos]
        total = sum(f.getlength(p) for f, p in zip(fs, partes)) + 20 * (len(partes) - 1)
        if total <= maxw or base <= 40: break
        base -= 4
    x = cx - total / 2
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x - 24, y - 46, x + total + 24, y + 46], 24, fill=(10, 15, 40, 190))
    for txt, ff, at in zip(partes, fs, ativos):
        d.text((x, y), txt, font=ff, fill=AMARELO if at else (255, 255, 255), anchor="lm", stroke_width=6, stroke_fill=ESCURO)
        x += ff.getlength(txt) + 20


def marca(d):
    nome = idioma.conf()["marca"]
    w = max(260, int(fnt(34).getlength(nome)) + 90)
    d.rounded_rectangle([30, 30, 30 + w, 90], 30, fill=ESCURO, outline=CIANO, width=4)
    d.text((30 + (w - 34) / 2, 60), nome, font=fnt(34), fill=(255, 255, 255), anchor="mm")
    d.ellipse([w - 4, 48, w + 18, 70], fill=AMARELO)


def selo_item(d, n, x=1700, y=95, r=70):
    d.ellipse([x - r, y - r, x + r, y + r], fill=AMARELO, outline=ESCURO, width=8)
    d.text((x, y + 4), f"#{n}", font=fnt(int(r * 0.95)), fill=ESCURO, anchor="mm")


def painel_vertical(img, c, t, T, caixa=PAINEL):
    """Desenha a cena vertical dos Shorts numa tela 1080x1920, recorta e amplia no painel."""
    c1, c2 = c.get("fundo", (NAVY1, NAVY2))
    tela = degrade(c1, c2, 1080, 1920)
    dv = ImageDraw.Draw(tela, "RGBA")
    if c.get("estrelas"): estrelas(dv, T, 1080, 1920, 40)
    c["vert"](dv, tela, t, T)
    y0, y1 = c.get("recorte", (360, 1290))
    x0, x1 = c.get("recorte_x", (0, 1080))
    rec = tela.crop((x0, y0, x1, y1))
    bx0, by0, bx1, by1 = caixa
    esc = min((bx1 - bx0) / rec.width, (by1 - by0) / rec.height)
    zoom = 1 + 0.04 * ease(t / 6)  # leve "Ken Burns" para não ficar parado
    nw, nh = int(rec.width * esc * zoom), int(rec.height * esc * zoom)
    rec = rec.resize((nw, nh), Image.BILINEAR)
    cw, ch = int(rec.width / zoom), int(rec.height / zoom)
    ox, oy = (nw - cw) // 2, (nh - ch) // 2
    rec = rec.crop((ox, oy, ox + cw, oy + ch))
    px, py = bx0 + ((bx1 - bx0) - cw) // 2, by0 + ((by1 - by0) - ch) // 2
    masc = Image.new("L", rec.size, 0)
    ImageDraw.Draw(masc).rounded_rectangle([0, 0, cw - 1, ch - 1], 36, fill=255)
    rec.putalpha(masc)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([px - 10, py - 10, px + cw + 10, py + ch + 10], 44, fill=ESCURO)
    img.alpha_composite(rec, (px, py))
    d.rounded_rectangle([px - 4, py - 4, px + cw + 4, py + ch + 4], 40, outline=CIANO, width=6)


def frame(c, t, T, boca, total):
    c1, c2 = c.get("fundo", (NAVY1, NAVY2))
    tp = c["tipo"]
    if tp in ("gancho", "cta", "ficha", "abre"):
        img = degrade(c1, c2)
    else:  # nas cenas de fato o fundo geral é escuro e o painel tem as cores do tema
        k = 0.35
        img = degrade(tuple(int(x * k) for x in c1), tuple(int(x * k) for x in c2))
    d = ImageDraw.Draw(img, "RGBA")
    estrelas(d, T, n=35 if tp in ("gancho", "cta") else 20)

    if tp in ("gancho", "cta") and not c.get("vert") and not c.get("desenho"):
        # MAIA grande à direita, título à esquerda
        r = 360 + math.sin(T * 2) * 8
        d.ellipse([1380 - r, 640 - r, 1380 + r, 640 + r], outline=CIANO, width=12)
        m = maia_pose(T, boca, escala=0.95)
        s = ease(t / 0.5) if c["_ini"] == 0 else 1
        img.alpha_composite(m, (1380 - m.width // 2, 230 + int((1 - s) * 400)))
        texto(img, c["titulo"], 560, 330, 120 if len(tr(c["titulo"])) <= 14 else 92, 0.15, t,
              cor=AMARELO if tp == "cta" else (255, 255, 255), maxw=900)
        if c.get("subtitulo"): texto(img, c["subtitulo"], 560, 560, 58, 0.6, t, cor=CIANO, maxw=900)
        legenda(img, c["_pal"], t, cx=560, y=840, maxw=980)
    elif tp == "abre":
        # abertura do item: número enorme + nome + bicho ampliado
        if c.get("vert"): painel_vertical(img, c, t, T, caixa=(900, 120, 1880, 930))
        n = c.get("item")
        sc = pop(t / 0.5)
        if n is not None:
            if sc > 0.02:
                f = fnt(int(280 * sc))
                d.text((450, 330), f"#{n}", font=f, fill=AMARELO, anchor="mm", stroke_width=14, stroke_fill=ESCURO)
            ny, sy = 580, 720
        else:  # abertura do vídeo: só o título grande
            ny, sy = 400, 660
        texto(img, c.get("nome") or c.get("titulo", ""), 450, ny, 76 if n is not None else 84, 0.35, t, maxw=780)
        if c.get("subtitulo"): texto(img, c["subtitulo"], 450, sy, 46, 0.7, t, cor=CIANO, maxw=780)
        m = maia_pose(T, boca, escala=0.42)
        img.alpha_composite(m, (1880 - m.width + 40, H - m.height + 40))
        legenda(img, c["_pal"], t, cx=450, y=940, maxw=820)
    elif tp == "ficha":
        # número gigante contando + legenda; bicho pequeno no painel da direita
        if c.get("vert"): painel_vertical(img, c, t, T, caixa=(1180, 150, 1860, 690))
        alvo = c["numero"]
        v = alvo * ease(t / 1.8)
        s = idioma.num(v, 0) if isinstance(alvo, int) or alvo >= 100 else idioma.num(v, 1)
        s = c.get("prefixo", "") + s + c.get("sufixo", "")
        f = fnt(200 if len(s) <= 6 else (150 if len(s) <= 9 else 110))
        if t > 0.1:
            d.text((600, 400), s, font=f, fill=AMARELO, anchor="mm", stroke_width=12, stroke_fill=ESCURO)
        texto(img, c["titulo"], 600, 640, 70, 0.6, t, maxw=1000)
        m = maia_pose(T, boca, escala=0.4)
        img.alpha_composite(m, (W - m.width - 60, H - m.height + 40))
        legenda(img, c["_pal"], t, cx=700, y=960, maxw=1250)
    else:  # fato
        if c.get("desenho"):
            c["desenho"](d, img, t, T)
        elif c.get("vert"):
            painel_vertical(img, c, t, T)
        texto(img, c["titulo"], 1430, 260, 80 if len(tr(c["titulo"])) <= 16 else 64, 0.1, t, maxw=820)
        m = maia_pose(T, boca, escala=0.62)
        img.alpha_composite(m, (1430 - m.width // 2, H - m.height + 60))
        legenda(img, c["_pal"], t, cx=W // 2, y=1010, maxw=1700)
    if c.get("item") is not None and tp != "abre":
        selo_item(ImageDraw.Draw(img), c["item"])
    marca(ImageDraw.Draw(img))
    dd = ImageDraw.Draw(img)
    dd.rectangle([0, H - 10, int(W * T / total), H], fill=CIANO)
    return img.convert("RGB")


def preparar(cenas, voz=None):
    voz = escolher_voz(cenas, voz)
    total = 0.0
    for c in cenas:
        pcm, pal = tts(c["fala"], voz)
        dur = len(pcm) / SR + c.get("pausa", 0.45)
        c["_pcm"], c["_pal"], c["_dur"], c["_ini"] = pcm, pal, dur, total
        total += dur
    return voz, total


def capitulos(cenas):
    caps = []
    for c in cenas:
        if c.get("capitulo"):
            caps.append((c["_ini"], c["capitulo"]))
    return caps


_CENAS, _TOTAL, _DIR = None, 0, ""


def _render_cena(idx):
    c = _CENAS[idx]
    n = int(round(c["_dur"] * FPS))
    env = envelope_fps(c["_pcm"], n)
    tmp = os.path.join(_DIR, f"_L{idx}.tmp.mp4"); fin = os.path.join(_DIR, f"_L{idx}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "22", "-pix_fmt", "yuv420p", "-threads", "1", tmp], stdin=subprocess.PIPE)
    for f in range(n):
        t = f / FPS; T = c["_ini"] + t
        p.stdin.write(frame(c, t, T, env[f], _TOTAL).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, fin)
    return fin


def envelope_fps(pcm, n_frames):
    hop = SR // FPS
    out = np.zeros(n_frames)
    for i in range(n_frames):
        seg = pcm[i * hop:(i + 1) * hop]
        if len(seg): out[i] = np.sqrt(np.mean(seg ** 2))
    if out.max() > 0: out = out / np.percentile(out[out > 0], 90)
    out = np.clip((out - 0.12) * 1.3, 0, 1)
    sm = out.copy()
    for i in range(1, len(sm)): sm[i] = 0.55 * out[i] + 0.45 * sm[i - 1]
    return sm


def render_longo(cenas, saida, voz=None, procs=None):
    global _CENAS, _TOTAL, _DIR
    voz, total = preparar(cenas, voz)
    print("voz:", voz, "| duração:", round(total, 1), "s", flush=True)
    _CENAS, _TOTAL, _DIR = cenas, total, os.path.dirname(os.path.abspath(saida))
    procs = procs or max(1, os.cpu_count() or 1)
    with mp.get_context("fork").Pool(procs) as pool:
        arquivos = []
        for i, a in enumerate(pool.imap(_render_cena, range(len(cenas)))):
            arquivos.append(a)
            print(f"cena {i + 1}/{len(cenas)} ok", flush=True)
    lst = os.path.join(_DIR, "_listaL.txt")
    open(lst, "w").writelines(f"file '{a}'\n" for a in arquivos)
    wav = os.path.join(_DIR, "_audioL.wav"); audio(cenas, total, wav)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", saida], check=True)
    for a in arquivos + [lst, wav]: os.remove(a)
    return total, capitulos(cenas)


def folha(cenas, saida, voz=None, inicio=0, n=12):
    """Folha de conferência: 1 quadro por cena (4 colunas, 480x270 cada)."""
    voz, total = preparar(cenas, voz)
    sel = cenas[inicio:inicio + n]
    ims = []
    for c in sel:
        t = min(3.4, c["_dur"] - 0.5)
        ims.append(frame(c, t, c["_ini"] + t, 0.5, total).resize((480, 270)))
    linhas = (len(ims) + 3) // 4
    s = Image.new("RGB", (1920, 270 * linhas))
    for i, im in enumerate(ims): s.paste(im, ((i % 4) * 480, (i // 4) * 270))
    s.save(saida, quality=85)
    return total, [round(c["_dur"], 1) for c in cenas]
