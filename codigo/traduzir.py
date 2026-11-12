"""Gera a versão de um vídeo em outro idioma (mesmos desenhos, texto e voz traduzidos).

  python3 traduzir.py video_venus es --listar           # mostra os textos que faltam traduzir (JSON)
  python3 traduzir.py video_venus es --preview folha.jpg # folha de conferência (gasta voz)
  python3 traduzir.py video_venus es out/venus_es.mp4    # renderiza

Traduções em traducoes/<tema>.json  ({"es": {"texto pt": "texto es"}}), onde <tema> = nome sem "video_".
Nada é renderizado se faltar tradução (para não sair português no meio).
"""
import sys, json, importlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import idioma


def preparar(modulo, lang):
    tema = modulo.replace("video_", "")
    idioma.ativar(lang, tema)
    import motor
    v = importlib.import_module(modulo)
    cenas = [dict(c) for c in v.CENAS]
    # passada "a seco": chama os desenhos em vários instantes para achar todo texto mostrado
    for c in cenas:
        for k in ("fala", "titulo", "subtitulo"):
            if c.get(k): idioma.tr(c[k])
        c.update(_pal=[], _dur=12, _ini=0, _pcm=None)
        for t in (0.2, 0.8, 1.6, 2.6, 3.6, 5, 7, 10):
            motor.frame(c, t, t, 0.0, 60)
    falta = list(idioma.FALTANDO)
    cenas = [dict(c) for c in v.CENAS]
    for c in cenas:
        for k in ("fala", "titulo", "subtitulo"):
            if c.get(k): c[k] = idioma.tr(c[k])
    return motor, cenas, falta


if __name__ == "__main__":
    modulo, lang = sys.argv[1], sys.argv[2]
    motor, cenas, falta = preparar(modulo, lang)
    if "--listar" in sys.argv:
        print(json.dumps({lang: {s: "" for s in falta}}, ensure_ascii=False, indent=1)); sys.exit(0)
    if falta:
        print("FALTA TRADUZIR:", *falta, sep="\n  "); sys.exit(1)
    voz = idioma.conf()["voz"]
    if "--preview" in sys.argv:
        saida = sys.argv[sys.argv.index("--preview") + 1]
        from PIL import Image
        tot = 0
        for c in cenas:
            pcm, pal = motor.tts(c["fala"], voz); c["_pcm"], c["_pal"] = pcm, pal
            c["_dur"] = len(pcm) / motor.SR + c.get("pausa", 0.45); c["_ini"] = tot; tot += c["_dur"]
        print("total", round(tot, 1), [round(c["_dur"], 1) for c in cenas])
        ims = []
        for c in cenas[:12]:
            t = min(3.4, c["_dur"] - 0.5); ims.append(motor.frame(c, t, c["_ini"] + t, 0.5, tot).resize((270, 480)))
        lin = (len(ims) + 3) // 4
        s = Image.new("RGB", (1080, 480 * lin)); [s.paste(im, ((i % 4) * 270, (i // 4) * 480)) for i, im in enumerate(ims)]
        s.save(saida)
    else:
        print("duração:", motor.render(cenas, sys.argv[3], voz))
