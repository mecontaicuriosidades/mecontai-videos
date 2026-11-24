"""Cabos submarinos de internet (TECNOLOGIA INSANA #3). Formato v3 + ESTRATÉGIA DA SEMANA 23/11.
Fatos (TeleGeography, FAQ 2026): cabos submarinos levam quase todo o tráfego de dados entre continentes;
mais de 1,5 milhão de km em serviço (~37 voltas na Terra); no fundo do mar o cabo é da grossura de
uma mangueira de jardim, com fibras finas como fio de cabelo; ~200 falhas por ano, 2/3 por acidentes
com barcos de pesca e âncoras; tubarões já morderam cabos, mas não são ameaça relevante."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, terra, contador, O

SERIE = "TECNOLOGIA INSANA #3"
MAR1 = (10, 60, 110); MAR2 = (3, 15, 40)
AREIA = (190, 165, 110); AREIA2 = (150, 125, 80)
CABO = (35, 35, 45); LUZ = (120, 255, 240)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def fundo_mar(d, y=1150):
    d.polygon([(0, 1260), (0, y), (200, y - 25), (420, y + 10), (650, y - 20), (860, y + 15), (1080, y - 10), (1080, 1260)],
              fill=AREIA, outline=O)
    for i in range(7):
        x = 80 + i * 150
        d.ellipse([x - 14, y + 40, x + 14, y + 52], fill=AREIA2)


def cabo(d, pts, T, w=26):
    d.line(pts, fill=O, width=w + 8, joint="curve")
    d.line(pts, fill=CABO, width=w, joint="curve")
    # pulsos de dados andando no cabo
    n = len(pts) - 1
    for k in range(4):
        u = ((T * 0.5 + k / 4) % 1) * n
        i = min(int(u), n - 1); f = u - i
        x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
        y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
        d.ellipse([x - w * 0.55, y - w * 0.55, x + w * 0.55, y + w * 0.55], fill=LUZ)


def peixinho(d, x, y, s, cor, T):
    y += math.sin(T * 3 + x) * 6
    d.polygon([(x - 40 * s, y), (x - 65 * s, y - 20 * s), (x - 65 * s, y + 20 * s)], fill=cor, outline=O)
    d.ellipse([x - 45 * s, y - 22 * s, x + 35 * s, y + 22 * s], fill=cor, outline=O, width=3)
    d.ellipse([x + 12 * s, y - 8 * s, x + 22 * s, y + 2 * s], fill=O)


def celular(d, x, y, T):
    d.rounded_rectangle([x - 70, y - 120, x + 70, y + 120], radius=18, fill=(30, 30, 40), outline=O, width=6)
    d.rectangle([x - 55, y - 95, x + 55, y + 95], fill=(40, 120, 200))
    d.polygon([(x - 20, y - 30), (x - 20, y + 30), (x + 30, y)], fill=(255, 255, 255))


def g_mar(d, img, t, T, label=True):
    etiqueta(d)
    # superfície
    d.rectangle([0, 585, 1080, 600], fill=(120, 200, 255))
    fundo_mar(d)
    pts = [(-20, 1120), (220, 1090), (480, 1130), (740, 1095), (1100, 1125)]
    cabo(d, pts, T, 30)
    peixinho(d, 300 + (T * 60) % 600, 820, 1.0, (255, 170, 60), T)
    peixinho(d, 800 - (T * 40) % 400, 940, 0.8, (120, 220, 140), T)
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if k > 0.05 and label:
        rotulo(d, 650, 1010, "INTERNET", int(56 * k) + 1, LUZ)
        seta(d, 650, 1045, 640, 1095, LUZ, 9)
        celular(d, 900, 700, T)


def c_voltas(d, img, t, T):
    selo(d)
    terra(d, 540, 850, 230, T, rosto=False)
    # cabo dando voltas no planeta
    voltas = int(1 + 36 * ease(t / 2.4))
    for i in range(min(voltas, 12)):
        rx, ry = 270 + i * 3, 70 + i * 9
        d.arc([540 - rx, 850 - ry, 540 + rx, 850 + ry], 0 + i * 15, 180 + i * 15, fill=(40, 40, 50), width=7)
    contador(d, 540, 1180, 37, t, 2.4, 80, " VOLTAS")
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 540, 560, "+1,5 MILHÃO DE KM", int(50 * k) + 1, AMARELO)


def c_mangueira(d, img, t, T):
    selo(d)
    # corte do cabo: camadas e fibras finas como cabelo
    cx, cy = 360, 830
    for r, cor in ((170, (30, 30, 40)), (140, (90, 90, 100)), (110, (200, 120, 40)), (80, (180, 180, 190)), (45, (240, 240, 240))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor, outline=O, width=4)
    for i in range(8):
        a = i * math.pi / 4 + T * 0.5
        x, y = cx + math.cos(a) * 25, cy + math.sin(a) * 25
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=LUZ)
    rotulo(d, cx, cy + 230, "FIBRAS = FIO DE CABELO", 40, LUZ)
    # mangueira de jardim ao lado
    k = pop(min(1, max(0, t - 0.4) / 0.5))
    if k > 0.05:
        pts = [(640, 620), (760, 700), (700, 820), (850, 900), (780, 1020), (960, 1080)]
        d.line(pts, fill=O, width=78, joint="curve")
        d.line(pts, fill=(60, 180, 80), width=64, joint="curve")
        rotulo(d, 820, 590, "MANGUEIRA", int(48 * k) + 1, AMARELO)


def ancora(d, x, y, s, cor=(150, 150, 160)):
    d.line([(x, y - 140 * s), (x, y + 100 * s)], fill=O, width=int(30 * s))
    d.line([(x, y - 140 * s), (x, y + 100 * s)], fill=cor, width=int(20 * s))
    d.ellipse([x - 30 * s, y - 190 * s, x + 30 * s, y - 130 * s], outline=cor, width=int(14 * s))
    d.line([(x - 70 * s, y - 80 * s), (x + 70 * s, y - 80 * s)], fill=cor, width=int(18 * s))
    d.arc([x - 110 * s, y - 20 * s, x + 110 * s, y + 140 * s], 0, 180, fill=O, width=int(30 * s))
    d.arc([x - 110 * s, y - 20 * s, x + 110 * s, y + 140 * s], 0, 180, fill=cor, width=int(20 * s))


def c_inimigo(d, img, t, T):
    selo(d)
    fundo_mar(d, 1120)
    k = ease(t / 1.2)
    # cabo puxado pela âncora
    mid = 540 + 0 * k
    cabo(d, [(-20, 1090), (300, 1080), (mid, 1080 - 260 * k), (780, 1080), (1100, 1090)], T, 26)
    ancora(d, 540, 760 - 30 * (1 - k), 1.0)
    d.line([(540, 570), (540, 520)], fill=(120, 100, 80), width=8)
    # tubarão pequeno com X
    tx, ty = 880, 640
    d.polygon([(tx - 110, ty), (tx - 150, ty - 40), (tx - 150, ty + 40)], fill=(120, 140, 160), outline=O)
    d.ellipse([tx - 120, ty - 45, tx + 90, ty + 45], fill=(140, 160, 180), outline=O, width=4)
    d.polygon([(tx - 20, ty - 40), (tx + 10, ty - 95), (tx + 30, ty - 40)], fill=(120, 140, 160), outline=O)
    d.line([(tx - 120, ty - 80), (tx + 90, ty + 80)], fill=(255, 70, 70), width=12)
    d.line([(tx - 120, ty + 80), (tx + 90, ty - 80)], fill=(255, 70, 70), width=12)
    k2 = pop(min(1, max(0, t - 0.6) / 0.5))
    if k2 > 0.05:
        rotulo(d, 260, 640, "ÂNCORAS E REDES", int(44 * k2) + 1, AMARELO)
        rotulo(d, 260, 700, "2/3 DAS QUEBRAS", int(44 * k2) + 1, AMARELO)


def c_cta(d, img, t, T):
    g_mar(d, img, t, T, label=False)
    rotulo(d, 650, 1010, "INTERNET", 56, LUZ)


CENAS = [
    dict(tipo="gancho", titulo="NO MAR!", titulo_y=400, desenho=g_mar, fundo=(MAR1, MAR2),
         fala="Quase toda a internet do mundo passa pelo fundo do mar! E o fim é o mais louco."),
    dict(tipo="fato", titulo="GIGANTE", desenho=c_voltas, fundo=((20, 30, 70), (5, 8, 25)),
         fala="São cabos com mais de um milhão e meio de quilômetros. Segue a Maia, que tem mais: dá pra dar trinta e sete voltas na Terra."),
    dict(tipo="fato", titulo="FININHO", desenho=c_mangueira, fundo=((30, 50, 70), (10, 18, 30)),
         fala="Lá embaixo, o cabo tem a grossura de uma mangueira. Eu esperava um tubo gigante!"),
    dict(tipo="fato", titulo="O VILÃO", desenho=c_inimigo, fundo=(MAR1, MAR2),
         fala="Tubarão já mordeu cabo, mas o vilão mesmo são âncoras e redes de pesca."),
    dict(tipo="cta", titulo="NO MAR!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana. Porque..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "cabos_submarinos.mp4"))
