"""Cratera de Darvaza (LUGARES MORTAIS #1). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, O

SERIE = "LUGARES MORTAIS #1"
AREIA = (230, 180, 110); AREIA2 = (190, 135, 75); LARANJA = (255, 140, 30); FOGO2 = (255, 220, 80)
VERMELHO = (230, 60, 60)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def dunas(d, y0, T):
    for k, (cor, amp) in enumerate(((AREIA2, 60), (AREIA, 40))):
        pts = [(0, 1920)]
        for x in range(0, 1101, 50):
            pts.append((x, y0 + k * 70 + math.sin(x / 180 + k * 2) * amp))
        pts.append((1080, 1920))
        d.polygon(pts, fill=cor)


def chamas(d, cx, cy, larg, alt, T, n=9, forca=1.0):
    for i in range(n):
        x = cx - larg / 2 + (i + 0.5) * larg / n
        h = alt * forca * (0.6 + 0.4 * abs(math.sin(T * 7 + i * 1.7)))
        w = larg / n * 0.9
        d.polygon([(x - w / 2, cy), (x - w * 0.15, cy - h * 0.6), (x, cy - h), (x + w * 0.2, cy - h * 0.55), (x + w / 2, cy)],
                  fill=LARANJA, outline=O)
        d.polygon([(x - w / 4, cy), (x, cy - h * 0.55), (x + w / 4, cy)], fill=FOGO2)


def cratera(d, cx, cy, rx, ry, T, forca=1.0):
    d.ellipse([cx - rx - 30, cy - ry - 20, cx + rx + 30, cy + ry + 30], fill=AREIA2, outline=O, width=7)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(60, 20, 10), outline=O, width=6)
    brilho = int(120 + 100 * forca)
    d.ellipse([cx - rx * 0.85, cy - ry * 0.6, cx + rx * 0.85, cy + ry * 0.8], fill=(brilho, 60, 20))
    # chamas pela borda de dentro
    for i in range(14):
        a = math.pi * (i / 13)
        x = cx - math.cos(a) * rx * 0.8
        y = cy + math.sin(a) * ry * 0.55
        h = (40 + 60 * abs(math.sin(T * 6 + i * 1.3))) * forca
        if h > 6:
            d.polygon([(x - 18, y), (x, y - h), (x + 18, y)], fill=LARANJA if i % 2 else FOGO2, outline=O)


def g_cratera(d, img, t, T):
    etiqueta(d)
    dunas(d, 900, T)
    cratera(d, 540, 1020, 360, 130, T)
    chamas(d, 540, 1000, 520, 260, T, n=8)
    # brasas subindo
    for i in range(12):
        y = 980 - ((T * 160 + i * 53) % 380)
        x = 330 + (i * 37) % 420 + math.sin(T * 3 + i) * 12
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=FOGO2)
    rotulo(d, 820, 1210, "+50 ANOS", 76, AMARELO)


def torre(d, x, y, ang, s=1.0):
    c, sn = math.cos(ang), math.sin(ang)
    P = lambda px, py: (x + (px * c - py * sn) * s, y + (px * sn + py * c) * s)
    d.polygon([P(-70, 0), P(70, 0), P(15, -330), P(-15, -330)], fill=(120, 120, 130), outline=O)
    for k in range(5):
        yy = -50 - k * 60
        d.line([P(-60 + k * 9, yy), P(60 - k * 9, yy - 50)], fill=O, width=5)
    d.rectangle([P(-25, -360)[0], P(-25, -360)[1], P(-25, -360)[0] + 50 * s, P(-25, -360)[1] + 30 * s], fill=VERMELHO, outline=O)


def c_desabou(d, img, t, T):
    selo(d)
    dunas(d, 860, T)
    k = ease((t - 0.6) / 1.2) if t > 0.6 else 0
    # buraco abre
    d.ellipse([540 - 300 * k, 1000 - 100 * k, 540 + 300 * k, 1000 + 100 * k], fill=(40, 15, 10), outline=O, width=6)
    torre(d, 540 + 120 * k, 990 + 140 * k, 0.5 * k, 0.9)
    rotulo(d, 220, 620, "1971", 84, (255, 255, 255))
    if t > 2.3:
        s = pop((t - 2.3) / 0.5)
        chamas(d, 540, 1010, 480 * s, 220 * s, T, n=7)
    if t > 3.0:
        rotulo(d, 820, 640, "NUNCA APAGOU", 50, AMARELO)


def explorador(d, x, y, T):
    # corda
    d.line([(x, 520), (x, y - 70)], fill=(240, 240, 240), width=8)
    pr = (210, 215, 225)
    d.rounded_rectangle([x - 45, y - 60, x + 45, y + 60], 20, fill=pr, outline=O, width=6)
    d.ellipse([x - 42, y - 135, x + 42, y - 50], fill=pr, outline=O, width=6)
    d.rounded_rectangle([x - 28, y - 112, x + 28, y - 78], 12, fill=(60, 90, 140), outline=O, width=4)
    for sx in (-1, 1):
        d.line([(x + sx * 40, y - 40), (x + sx * 85, y - 100)], fill=pr, width=24)
        d.line([(x + sx * 20, y + 55), (x + sx * 35, y + 140)], fill=pr, width=26)
    d.rectangle([x - 32, y + 10, x + 32, y + 30], fill=(250, 210, 40), outline=O, width=3)


def c_explorador(d, img, t, T):
    selo(d)
    cratera(d, 540, 1120, 470, 190, T)
    chamas(d, 540, 1130, 700, 200, T, n=10)
    desce = min(1, t / 3.0)
    explorador(d, 540, 640 + 300 * desce + math.sin(T * 2) * 10, T)
    rotulo(d, 860, 600, "2013", 80, (255, 255, 255))
    if t > 1.2:
        rotulo(d, 230, 760, "ROUPA", 48, CIANO)
        rotulo(d, 230, 815, "ANTIFOGO", 48, CIANO)


def c_apagando(d, img, t, T):
    selo(d)
    dunas(d, 960, T)
    f = 1 - 0.68 * ease(t / 3.0)
    cratera(d, 380, 1080, 300, 110, T, forca=f)
    chamas(d, 380, 1065, 420, 240, T, n=7, forca=f)
    # poços que capturam o gás
    for i, x in enumerate((780, 930)):
        d.rectangle([x - 18, 820, x + 18, 1080], fill=(170, 170, 185), outline=O, width=5)
        d.rectangle([x - 45, 790, x + 45, 830], fill=(250, 210, 40), outline=O, width=5)
    d.line([(690, 1060), (780, 1060), (930, 1060)], fill=(170, 170, 185), width=14)
    # barra de força do fogo
    d.rounded_rectangle([140, 560, 940, 640], 30, fill=(30, 20, 20), outline=O, width=6)
    d.rounded_rectangle([150, 570, 150 + 780 * f, 630], 26, fill=LARANJA)
    if t > 2.0:
        rotulo(d, 540, 720, "FOGO ÷ 3", 76, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="50 ANOS!", titulo_y=400, desenho=g_cratera, fundo=((40, 30, 80), (120, 50, 40)),
         fala="Esse buraco no deserto pega fogo há mais de cinquenta anos! E o final é o mais estranho."),
    dict(tipo="fato", titulo="DARVAZA", desenho=c_desabou, fundo=((60, 120, 200), (230, 170, 110)),
         fala="É a cratera de Darvaza. Segue a Maia, que piora: dizem que em 1971 o chão desabou. Botaram fogo no gás, e nunca apagou."),
    dict(tipo="fato", titulo="DESCEU LÁ", desenho=c_explorador, fundo=((30, 20, 50), (90, 30, 30)),
         fala="Em 2013, um explorador desceu até o fundo, de roupa antifogo, pra coletar amostras."),
    dict(tipo="fato", titulo="SE APAGANDO", desenho=c_apagando, fundo=((50, 60, 120), (200, 120, 80)),
         fala="E o mais estranho: puxando o gás por poços, já reduziram o fogo a um terço. Ela está se apagando."),
    dict(tipo="cta", titulo="50 ANOS!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=g_cratera,
         fundo=((40, 30, 80), (120, 50, 40)),
         fala="Segue a Maia: amanhã tem mais Lugares Mortais. Porque esse buraco..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "darvaza.mp4"))
