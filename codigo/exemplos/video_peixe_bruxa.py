"""Peixe-bruxa: o bicho que enche um balde de gosma em segundos. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, brilhos, O

PELE = (200, 130, 150); PELE2 = (160, 90, 115); GOSMA = (190, 245, 210, 200); GOSMA2 = (140, 220, 170)
ASFALTO = (70, 70, 80); BALDE = (90, 140, 210)


def peixe_bruxa(d, x, y, s, T, fase=0, cor=PELE, cor2=PELE2, rosto=True):
    """Corpo de enguia ondulando, cabeça à direita com barbilhões."""
    pts = []
    for i in range(30):
        u = i / 29
        pts.append((x - 230 * s + u * 230 * s, y + math.sin(u * 6 - T * 4 + fase) * 22 * s))
    d.line(pts, fill=O, width=int(46 * s) + 8, joint="curve")
    d.line(pts, fill=cor, width=int(46 * s), joint="curve")
    for i in range(3, 27, 3):  # poros de gosma
        px, py = pts[i]
        d.ellipse([px - 5 * s, py + 8 * s, px + 5 * s, py + 16 * s], fill=cor2)
    hx, hy = pts[-1]
    d.ellipse([hx - 30 * s, hy - 26 * s, hx + 34 * s, hy + 26 * s], fill=cor, outline=O, width=5)
    for k in (-1, 0, 1):
        d.line([(hx + 30 * s, hy + k * 10 * s), (hx + 52 * s, hy + k * 18 * s + math.sin(T * 8 + k) * 4 * s)],
               fill=O, width=max(3, int(5 * s)))
    if rosto:
        d.ellipse([hx - 4 * s, hy - 16 * s, hx + 10 * s, hy - 2 * s], fill="white", outline=O, width=2)
        d.ellipse([hx + 1 * s, hy - 12 * s, hx + 7 * s, hy - 5 * s], fill=O)


def bolha_gosma(d, cx, cy, r, T, cor=GOSMA):
    pts = []
    for i in range(24):
        a = i / 24 * 2 * math.pi
        rr = r * (1 + 0.12 * math.sin(a * 5 + T * 3))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.8))
    d.polygon(pts, fill=cor, outline=GOSMA2)
    for i in range(4):  # brilhos da gosma
        a = i * 1.6 + T
        d.ellipse([cx + math.cos(a) * r * 0.5 - 12, cy + math.sin(a) * r * 0.4 - 8,
                   cx + math.cos(a) * r * 0.5 + 12, cy + math.sin(a) * r * 0.4 + 8], fill=(255, 255, 255, 180))


def balde(d, cx, cy, s, nivel, T):
    d.polygon([(cx - 150 * s, cy - 170 * s), (cx + 150 * s, cy - 170 * s), (cx + 115 * s, cy + 170 * s),
               (cx - 115 * s, cy + 170 * s)], fill=BALDE, outline=O)
    h = 330 * s * nivel
    if nivel > 0:
        top = cy + 170 * s - h
        d.polygon([(cx - 115 * s - (h / (340 * s)) * 35 * s, top), (cx + 115 * s + (h / (340 * s)) * 35 * s, top),
                   (cx + 115 * s, cy + 170 * s), (cx - 115 * s, cy + 170 * s)], fill=GOSMA2)
        if nivel > 0.95:  # transbordando
            for k in range(3):
                xx = cx - 120 * s + k * 120 * s
                d.ellipse([xx - 40 * s, top - 30 * s, xx + 40 * s, top + 20 * s], fill=GOSMA2, outline=O, width=3)
    d.arc([cx - 150 * s, cy - 280 * s, cx + 150 * s, cy - 60 * s], 180, 360, fill=O, width=int(10 * s))


# ---------------- cenas ----------------
def g_gosma(d, img, t, T):
    k = ease(t / 1.2)
    bolha_gosma(d, 640, 880, 130 + k * 230, T)
    peixe_bruxa(d, 760, 860, 1.25, T)
    if t > 0.2:
        brilhos(d, 640, 880, 330, T, n=7, cor=(200, 255, 210))


def c_balde(d, img, t, T):
    nivel = ease(t / 2.0)
    balde(d, 420, 900, 1.1, nivel, T)
    peixe_bruxa(d, 820, 700, 0.6, T)
    seta(d, 720, 760, 600, 820, cor=AMARELO, w=10)
    if t > 1.6:
        rotulo(d, 420, 1150, "EM SEGUNDOS", 60, (210, 255, 220))


def c_tubarao(d, img, t, T):
    # tubarão com a boca entupida de gosma
    cx, cy = 430, 860
    d.polygon([(cx - 330, cy), (cx - 420, cy - 110), (cx - 400, cy), (cx - 420, cy + 110)], fill=(120, 140, 160), outline=O)
    d.ellipse([cx - 360, cy - 130, cx + 200, cy + 130], fill=(140, 160, 180), outline=O, width=6)
    d.polygon([(cx - 120, cy - 120), (cx - 60, cy - 250), (cx + 20, cy - 120)], fill=(120, 140, 160), outline=O)
    d.ellipse([cx + 60, cy - 60, cx + 100, cy - 20], fill="white", outline=O, width=4)
    d.line([(cx + 66, cy - 46), (cx + 94, cy - 34)], fill=O, width=6)  # olho apertado
    bolha_gosma(d, cx + 220, cy + 30, 110 + 20 * math.sin(T * 3), T)
    peixe_bruxa(d, 900, 1040, 0.55, T, fase=1)
    if t > 1.2:
        rotulo(d, 540, 1170, "ENGASGOU!", 64, (255, 230, 140))


def c_no(d, img, t, T):
    # peixe-bruxa dando um nó em si mesmo
    cx, cy = 500, 860
    fase = min(1, t / 1.5)
    pts = []
    for i in range(80):
        u = i / 79
        a = u * 2 * math.pi * 1.5 * fase
        r = 150 * fase
        x = cx - 330 + u * 600 + math.sin(a) * r * 0.3
        y = cy + math.cos(a) * r * 0.9 - r * 0.9 * fase
        pts.append((x, y))
    d.line(pts, fill=O, width=58, joint="curve")
    d.line(pts, fill=PELE, width=48, joint="curve")
    hx, hy = pts[-1]
    d.ellipse([hx - 34, hy - 30, hx + 38, hy + 30], fill=PELE, outline=O, width=5)
    d.ellipse([hx - 2, hy - 18, hx + 14, hy - 2], fill="white", outline=O, width=2)
    for k in range(6):  # gosma sendo raspada
        x = cx - 300 + k * 110 + math.sin(T * 2 + k) * 10
        y = cy + 120 + ((T * 90 + k * 40) % 140)
        d.ellipse([x - 22, y - 16, x + 22, y + 16], fill=GOSMA2, outline=O, width=3)
    if t > 1.4:
        rotulo(d, 540, 1170, "SE LIMPA COM UM NÓ", 54, (255, 255, 255))


def carro(d, x, y, s, cor):
    d.rounded_rectangle([x - 150 * s, y - 60 * s, x + 150 * s, y + 40 * s], int(20 * s), fill=cor, outline=O, width=5)
    d.polygon([(x - 90 * s, y - 60 * s), (x - 50 * s, y - 120 * s), (x + 60 * s, y - 120 * s), (x + 100 * s, y - 60 * s)],
              fill=cor, outline=O)
    d.polygon([(x - 70 * s, y - 64 * s), (x - 40 * s, y - 108 * s), (x + 50 * s, y - 108 * s), (x + 80 * s, y - 64 * s)],
              fill=(180, 220, 240))
    for sx in (-1, 1):
        d.ellipse([x + sx * 95 * s - 35 * s, y + 10 * s, x + sx * 95 * s + 35 * s, y + 80 * s], fill=O)


def c_estrada(d, img, t, T):
    d.rectangle([0, 980, 1080, 1300], fill=ASFALTO)
    for i in range(5):
        d.rectangle([40 + i * 230, 1120, 170 + i * 230, 1140], fill=(240, 220, 90))
    # caminhão tombado
    d.rounded_rectangle([90, 820, 520, 1000], 18, fill=(230, 230, 235), outline=O, width=6)
    d.rectangle([520, 860, 650, 1000], fill=(220, 70, 60), outline=O, width=6)
    carro(d, 820, 960, 0.9, (90, 160, 230))
    k = ease(t / 2.0)
    for i in range(7):  # gosma se espalhando
        x = 200 + i * 120
        d.ellipse([x - 80 * k - 20, 990 - 30 * k, x + 80 * k + 20, 1040 + 20 * k], fill=GOSMA2)
    for i in range(3):
        peixe_bruxa(d, 240 + i * 260, 1060 + (i % 2) * 40, 0.45, T, fase=i, rosto=False)
    bolha_gosma(d, 820, 900, 90 * k + 10, T)
    if t > 0.8:
        rotulo(d, 540, 650, "OREGON, 2017", 62, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="BALDE DE GOSMA", desenho=g_gosma, fundo=((40, 120, 140), (10, 40, 60)),
         fala="Esse bicho transforma água em gosma em menos de um segundo. E já engasgou até tubarão!"),
    dict(tipo="fato", titulo="FÁBRICA DE MELECA", desenho=c_balde, fundo=((60, 90, 150), (20, 30, 70)),
         fala="É o peixe-bruxa. Quando é atacado, solta um muco que incha na água e pode encher um balde inteiro."),
    dict(tipo="fato", titulo="TUBARÃO ENGASGADO", desenho=c_tubarao, fundo=((20, 80, 120), (5, 25, 50)),
         fala="Já filmaram tubarões mordendo um peixe-bruxa e cuspindo na hora, com as guelras entupidas de gosma."),
    dict(tipo="fato", titulo="NÓ DE LIMPEZA", desenho=c_no, fundo=((120, 70, 130), (40, 20, 60)),
         fala="Pra não se sufocar na própria meleca, ele dá um nó no corpo e escorrega por dentro dele, raspando tudo."),
    dict(tipo="fato", titulo="ESTRADA MELECADA", desenho=c_estrada, fundo=((240, 160, 90), (120, 70, 60)),
         fala="Em dois mil e dezessete, nos Estados Unidos, um caminhão cheio deles tombou e cobriu carros e a estrada de gosma!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Nojo de 0 a 10?",
         fala="Comenta: de zero a dez, quanto nojo isso te deu? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "peixe_bruxa.mp4"))
