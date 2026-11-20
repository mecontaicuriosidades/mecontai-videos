"""Gálio, Parte 1 (CIÊNCIA BIZARRA #1). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, termometro, brilhos, O
import idioma

SERIE = "CIÊNCIA BIZARRA #1"
PELE = (240, 190, 150); PELE2 = (205, 150, 115)
PRATA = (205, 215, 225); PRATA2 = (150, 165, 180); BRILHO = (250, 252, 255)
XICARA = (230, 90, 80); CHA = (150, 85, 40); VIDRO = (190, 230, 240)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def graus(v, casas=0):
    return f"{idioma.num(v, casas)} °C"


def mao(d, cx, cy, s=1.0):
    """Palma da mão aberta, vista de cima (dedos para cima)."""
    # dedos
    for i, (dx, h) in enumerate(((-120, 230), (-45, 280), (30, 290), (105, 250))):
        x = cx + dx * s
        d.rounded_rectangle([x - 32 * s, cy - (120 + h) * s, x + 32 * s, cy - 60 * s], int(32 * s), fill=PELE, outline=O, width=5)
    # polegar
    d.polygon([(cx - 150 * s, cy + 10 * s), (cx - 270 * s, cy - 120 * s), (cx - 225 * s, cy - 165 * s), (cx - 120 * s, cy - 60 * s)],
              fill=PELE, outline=O)
    d.ellipse([cx - 175 * s, cy - 180 * s, cx + 175 * s, cy + 130 * s], fill=PELE, outline=O, width=5)
    d.rectangle([cx - 120 * s, cy + 80 * s, cx + 120 * s, cy + 320 * s], fill=PELE, outline=O, width=5)
    d.ellipse([cx - 165 * s, cy - 170 * s, cx + 165 * s, cy + 120 * s], fill=PELE)
    d.arc([cx - 110 * s, cy - 90 * s, cx + 80 * s, cy + 60 * s], 200, 330, fill=PELE2, width=5)


def poca(d, cx, cy, k, T, s=1.0):
    """Metal: cubo que vira poça brilhante conforme k vai de 0 a 1."""
    k = max(0.0, min(1.0, k))
    hcubo = 120 * (1 - k) * s
    w = (110 + 120 * k) * s
    d.ellipse([cx - w, cy - 30 * s - 20 * k * s, cx + w, cy + 30 * s + 15 * k * s], fill=PRATA, outline=O, width=4)
    if hcubo > 4:
        lado = 110 * s * (1 - 0.4 * k)
        d.rectangle([cx - lado / 2, cy - hcubo, cx + lado / 2, cy], fill=PRATA, outline=O, width=4)
        d.polygon([(cx - lado / 2, cy - hcubo), (cx - lado / 2 + 30 * s, cy - hcubo - 28 * s),
                   (cx + lado / 2 + 30 * s, cy - hcubo - 28 * s), (cx + lado / 2, cy - hcubo)], fill=BRILHO, outline=O)
    d.ellipse([cx - w * 0.5, cy - 14 * s, cx - w * 0.1, cy + 2 * s], fill=BRILHO)
    # gotas escorrendo
    if k > 0.4:
        for i, dx in enumerate((-0.7, 0.2, 0.8)):
            f = (T * 0.8 + i * 0.37) % 1
            gx, gy = cx + dx * w, cy + 30 * s + f * 160 * s
            d.ellipse([gx - 13 * s, gy - 18 * s, gx + 13 * s, gy + 18 * s], fill=PRATA, outline=O, width=3)


def g_mao(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    mao(d, 560, 1020, 1.15)
    k = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(T * 1.2))
    poca(d, 560, 1010, k, T, 1.0)
    brilhos(d, 560, 960, 230, T, 8, BRILHO)
    rotulo(d, 870, 640, graus(29.8, 1), 50, AMARELO)


def c_termo(d, img, t, T):
    selo(d)
    termometro(d, 300, 1240, min(1, ease(t / 2.4)) * 0.85, (235, 70, 60), 640)
    # marcas
    d.line([(340, 900), (470, 900)], fill=PRATA, width=8)
    d.line([(340, 760), (470, 760)], fill=PELE, width=8)
    rotulo(d, 700, 900, "GÁLIO " + graus(30), 46, PRATA)
    rotulo(d, 700, 760, "MÃO " + graus(36), 46, PELE)
    poca(d, 760, 1170, min(1, max(0, (t - 1.2) / 2.0)), T, 0.9)


def xicara(d, cx, cy, s=1.0):
    d.rounded_rectangle([cx - 170 * s, cy - 150 * s, cx + 170 * s, cy + 110 * s], int(50 * s), fill=XICARA, outline=O, width=6)
    d.arc([cx + 120 * s, cy - 100 * s, cx + 260 * s, cy + 40 * s], -90, 90, fill=O, width=int(36 * s))
    d.arc([cx + 120 * s, cy - 100 * s, cx + 260 * s, cy + 40 * s], -90, 90, fill=XICARA, width=int(22 * s))
    d.ellipse([cx - 160 * s, cy - 175 * s, cx + 160 * s, cy - 125 * s], fill=CHA, outline=O, width=5)
    d.ellipse([cx - 260 * s, cy + 90 * s, cx + 300 * s, cy + 150 * s], fill=(245, 240, 230), outline=O, width=5)


def c_colher(d, img, t, T):
    selo(d)
    xicara(d, 520, 1100, 1.2)
    # vapor
    for i in range(3):
        f = (T * 0.5 + i / 3) % 1
        x = 440 + i * 80 + 20 * math.sin(T * 3 + i)
        d.arc([x - 30, 820 - f * 220, x + 30, 880 - f * 220], 90, 270, fill=(255, 255, 255, int(200 * (1 - f))), width=8)
    # colher afundando e encolhendo
    k = min(1, t / 3.2)
    L = 420 * (1 - 0.8 * k)
    x0, y0 = 600, 890
    ang = math.radians(-60)
    x1, y1 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
    d.line([(x0, y0), (x1, y1)], fill=O, width=30)
    d.line([(x0, y0), (x1, y1)], fill=PRATA, width=20)
    d.ellipse([x0 - 40, y0 - 18, x0 + 40, y0 + 18], fill=PRATA2, outline=O, width=3)
    if t > 1.0:
        rotulo(d, 820, 640, "SUMIU?!", 60, AMARELO)


def pote(d, cx, cy, T, k):
    """Pote de vidro com gálio que vira sólido, incha e racha o vidro."""
    w, h = 180, 250
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], 40, fill=VIDRO + (90,), outline=O, width=6)
    d.rectangle([cx - w - 15, cy - h - 50, cx + w + 15, cy - h], fill=(120, 120, 140), outline=O, width=5)
    nivel = cy + h - 280 - 60 * k
    d.rounded_rectangle([cx - w + 14, nivel, cx + w - 14, cy + h - 14], 30, fill=PRATA2 if k > 0.3 else PRATA, outline=O, width=3)
    # cristais quando congela
    if k > 0.3:
        for i in range(7):
            x = cx - w + 40 + i * 50
            y = nivel + 40 + 30 * (i % 2)
            d.polygon([(x, y - 22), (x + 16, y), (x, y + 22), (x - 16, y)], fill=BRILHO, outline=O)
    # rachaduras
    if k > 0.6:
        tr = int(8 + 4 * math.sin(T * 20))
        d.line([(cx + w, cy - 80), (cx + w - 70, cy - 20), (cx + w - 30, cy + 40), (cx + w - 100, cy + 110)], fill=O, width=tr)
        d.line([(cx - w, cy + 30), (cx - w + 60, cy + 90), (cx - w + 20, cy + 160)], fill=O, width=tr)


def c_incha(d, img, t, T):
    selo(d)
    k = min(1, t / 3.0)
    pote(d, 540, 1000, T, k)
    if k > 0.3:
        seta(d, 860, 1000, 860, 760, AMARELO)
        seta(d, 220, 1000, 220, 760, AMARELO)
    if k > 0.6:
        p = pop((t - 1.8) / 0.4)
        rotulo(d, 540, 560, "CRACK!", int(84 * max(0.3, p)), AMARELO)


def c_cta(d, img, t, T):
    g_mao(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="DERRETE!", titulo_y=400, desenho=g_mao, fundo=((60, 70, 120), (20, 25, 60)),
         fala="Esse metal derrete na palma da sua mão! E o último fato é o pior."),
    dict(tipo="fato", titulo="O GÁLIO", desenho=c_termo, fundo=((70, 50, 120), (30, 20, 70)),
         fala="É o gálio. Segue a Maia, que piora: ele derrete a uns trinta graus, e a sua mão tem uns trinta e seis."),
    dict(tipo="fato", titulo="SUMIU", desenho=c_colher, fundo=((200, 150, 90), (120, 75, 40)),
         fala="Uma colher de gálio some dentro de um chá quente, como se fosse gelo."),
    dict(tipo="fato", titulo="CONGELA", desenho=c_incha, fundo=((40, 110, 150), (15, 50, 90)),
         fala="E quando volta a ficar sólido, ele incha, igual à água, e pode até rachar o vidro do pote."),
    dict(tipo="cta", titulo="DERRETE!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((60, 70, 120), (20, 25, 60)),
         fala="E o pior: tem outro metal que ele destrói só de encostar. Segue a Maia pra ver a parte dois às seis da tarde. Porque esse metal..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "galio_p1.mp4"))
