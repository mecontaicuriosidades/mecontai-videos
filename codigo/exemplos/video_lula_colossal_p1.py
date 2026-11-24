"""Lula-colossal (Mesonychoteuthis hamiltoni), Parte 1 (BICHOS INSANOS #9).
Formato v3 + ESTRATÉGIA DA SEMANA 23/11 (20–28 s, fato chocante no 1º segundo, frase de opinião da MAIA).
Decisão do Wellington 24/11: selo e convite 'Segue a Maia' continuam, sem a palavra proibida."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "BICHOS INSANOS #9"
LULA = (200, 70, 70); LULA2 = (150, 40, 50); PELE = (235, 120, 110)
OLHO = (245, 245, 235); IRIS = (40, 140, 160)
BOLA = (235, 120, 30); BOLA2 = (120, 50, 10)
MAR1 = (10, 35, 80); MAR2 = (2, 10, 30)
GELO = (225, 245, 255)


def etiqueta(d, parte="P1"):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def bolhas(d, T, n=18, y0=520, y1=1260):
    for i in range(n):
        x = (i * 211 + T * 12 * (1 + i % 2)) % 1080
        y = y1 - ((i * 83 + T * 40 * (1 + i % 3)) % (y1 - y0))
        r = 4 + i % 4
        d.ellipse([x - r, y - r, x + r, y + r], outline=(150, 200, 240), width=3)


def olho(d, cx, cy, r, T, olhar=(0.0, 0.0)):
    """Olhão: esclera clara, íris azul-esverdeada, pupila escura, reflexo."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OLHO, outline=O, width=max(5, int(r / 14)))
    ox, oy = olhar
    ir = r * 0.62
    ix, iy = cx + ox * r * 0.2, cy + oy * r * 0.2
    d.ellipse([ix - ir, iy - ir, ix + ir, iy + ir], fill=IRIS, outline=O, width=4)
    pr = ir * (0.55 + 0.05 * math.sin(T * 3))
    d.ellipse([ix - pr, iy - pr, ix + pr, iy + pr], fill=(10, 10, 20))
    d.ellipse([ix - ir * 0.55, iy - ir * 0.6, ix - ir * 0.15, iy - ir * 0.2], fill=(255, 255, 255))
    if (T % 3.7) < 0.12:  # piscada (pálpebra)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LULA2, outline=O, width=5)


def bracos(d, cx, cy, s, T, ganchos=False, n=8, comp=330):
    """Braços ondulando para a direita, saindo de (cx,cy)."""
    for k in range(n):
        base_y = cy + (k - (n - 1) / 2) * 22 * s
        pts = []
        for j in range(12):
            u = j / 11
            x = cx + u * comp * s
            y = base_y + (k - (n - 1) / 2) * 18 * s * u + math.sin(T * 3 + k + u * 5) * 22 * s * u
            pts.append((x, y))
        larg = int(20 * s)
        d.line(pts, fill=O, width=larg + 8, joint="curve")
        d.line(pts, fill=PELE if k % 2 else LULA, width=larg, joint="curve")
        if ganchos:
            for j in (4, 7, 10):
                x, y = pts[j]
                ang = T * 4 + k + j  # ganchos que giram
                ex, ey = x + math.cos(ang) * 16 * s, y + math.sin(ang) * 16 * s
                d.line([(x, y), (ex, ey)], fill=(250, 250, 250), width=max(3, int(6 * s)))


def lula(d, cx, cy, s=1.0, T=0.0, ganchos=False, olho_r=None):
    """Lula-colossal deitada: manto para a esquerda, braços para a direita, olhão no meio."""
    bal = math.sin(T * 1.8) * 8 * s
    cy = cy + bal
    # nadadeiras na ponta do manto
    aba = math.sin(T * 4) * 14 * s
    d.polygon([(cx - 380 * s, cy), (cx - 470 * s, cy - 120 * s - aba), (cx - 300 * s, cy - 40 * s)], fill=LULA2, outline=O)
    d.polygon([(cx - 380 * s, cy), (cx - 470 * s, cy + 120 * s + aba), (cx - 300 * s, cy + 40 * s)], fill=LULA2, outline=O)
    # braços
    bracos(d, cx + 90 * s, cy, s, T, ganchos)
    # manto
    d.ellipse([cx - 420 * s, cy - 95 * s, cx + 40 * s, cy + 95 * s], fill=LULA, outline=O, width=7)
    for k in range(5):
        xx = cx - 340 * s + k * 70 * s
        d.ellipse([xx - 12 * s, cy - 40 * s, xx + 12 * s, cy - 20 * s], fill=PELE)
    # cabeça
    d.ellipse([cx - 30 * s, cy - 110 * s, cx + 150 * s, cy + 110 * s], fill=LULA, outline=O, width=7)
    olho(d, cx + 60 * s, cy - 5 * s, olho_r if olho_r else 72 * s, T)


def bola(d, cx, cy, r, T=0.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BOLA, outline=O, width=7)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BOLA2, width=6)
    d.line([(cx, cy - r), (cx, cy + r)], fill=BOLA2, width=6)
    d.arc([cx - r * 1.5, cy - r, cx - r * 0.3, cy + r], 300, 60, fill=BOLA2, width=6)
    d.arc([cx + r * 0.3, cy - r, cx + r * 1.5, cy + r], 120, 240, fill=BOLA2, width=6)


def g_olho(d, img, t, T, label=True):
    etiqueta(d)
    bolhas(d, T)
    # cabeça gigante entrando pela direita, com o olhão
    d.ellipse([480, 560, 1260, 1260], fill=LULA, outline=O, width=9)
    for k in range(6):
        d.ellipse([560 + k * 90, 1150 - (k % 2) * 30, 590 + k * 90, 1175 - (k % 2) * 30], fill=PELE)
    olho(d, 790, 880, 210, T, (math.sin(T) * 0.4 - 0.5, 0))
    # bola de basquete ao lado, mesmo tamanho
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if k > 0.05:
        bola(d, 250, 880, int(190 * k) + 1, T)
        if label:
            rotulo(d, 540, 1200, "OLHO = BOLA DE BASQUETE", int(42 * k) + 1, AMARELO)


def c_antartida(d, img, t, T):
    selo(d)
    # Antártida (gelo) embaixo e mar gelado
    d.polygon([(0, 1250), (0, 1100), (160, 1060), (330, 1090), (520, 1030), (720, 1080), (900, 1040), (1080, 1090), (1080, 1250)],
              fill=GELO, outline=O)
    rotulo(d, 540, 1170, "ANTÁRTIDA", 50, (60, 110, 170))
    for i in range(3):
        x = 180 + i * 330 + math.sin(T + i) * 10
        d.polygon([(x - 50, 1000), (x, 930), (x + 60, 1000)], fill=(240, 250, 255), outline=O)
    bolhas(d, T, 10, 520, 1000)
    k = ease(t / 1.0)
    lula(d, 1200 - 620 * k, 720, 0.85, T)


def c_peso(d, img, t, T):
    selo(d)
    # balança: lula de um lado, contador de quilos
    lula(d, 600, 680, 0.75, T)
    d.rectangle([160, 960, 920, 990], fill=(200, 200, 210), outline=O, width=5)
    d.polygon([(500, 990), (580, 990), (540, 1150)], fill=(160, 160, 170), outline=O)
    d.rectangle([380, 1150, 700, 1180], fill=(160, 160, 170), outline=O, width=5)
    contador(d, 540, 1060, 495, t, 1.6, 90, " KG")
    k = pop(min(1, max(0, t - 1.2) / 0.5))
    if k > 0.05:
        rotulo(d, 540, 1235, "INVERTEBRADO MAIS PESADO", int(40 * k) + 1, CIANO)


def c_ganchos(d, img, t, T):
    selo(d)
    # zoom num braço: ventosas e ganchos girando
    pts = [(80 + i * 90, 820 + math.sin(T * 2 + i * 0.6) * 40) for i in range(11)]
    d.line(pts, fill=O, width=150, joint="curve")
    d.line(pts, fill=LULA, width=136, joint="curve")
    for i, (x, y) in enumerate(pts[1:-1]):
        d.ellipse([x - 26, y + 18, x + 26, y + 58], fill=PELE, outline=O, width=4)
        ang = T * 3.5 + i
        ex, ey = x + math.cos(ang) * 34, y - 30 + math.sin(ang) * 34
        d.ellipse([x - 12, y - 42, x + 12, y - 18], fill=(250, 250, 250), outline=O, width=3)
        d.line([(x, y - 30), (ex, ey)], fill=O, width=12)
        d.line([(x, y - 30), (ex, ey)], fill=(250, 250, 250), width=6)
    k = pop(min(1, max(0, t - 0.4) / 0.5))
    if k > 0.05:
        rotulo(d, 330, 600, "GANCHOS QUE GIRAM", int(46 * k) + 1, AMARELO)
        seta(d, 330, 640, 440, 740, AMARELO, 10)
        rotulo(d, 760, 1060, "VENTOSAS", int(42 * k) + 1, CIANO)
        seta(d, 760, 1020, 640, 900, CIANO, 8)


def c_cta(d, img, t, T):
    g_olho(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="OLHÃO!", titulo_y=400, desenho=g_olho, fundo=(MAR1, MAR2),
         fala="Um olho do tamanho de uma bola de basquete! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="LULA-COLOSSAL", desenho=c_antartida, fundo=((20, 60, 110), MAR2),
         fala="É a lula-colossal, do mar gelado da Antártida. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="495 KG", desenho=c_peso, fundo=((40, 30, 80), (15, 10, 35)),
         fala="ela pode passar de meia tonelada: é o invertebrado mais pesado do mundo."),
    dict(tipo="fato", titulo="GANCHOS", desenho=c_ganchos, fundo=((60, 20, 40), (20, 5, 15)),
         fala="E nos braços tem ganchos que giram. Filme de terror!"),
    dict(tipo="cta", titulo="OLHÃO!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Por cem anos, ninguém viu uma viva. Segue a Maia pra ver a parte dois às seis da tarde. Tudo por causa de..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lula_colossal_p1.mp4"))
