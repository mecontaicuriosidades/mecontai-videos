"""Relâmpago do Catatumbo, Parte 1 (LUGARES MORTAIS #5). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "LUGARES MORTAIS #5"
RAIO = (255, 250, 210); RAIO2 = (180, 140, 255); AGUA = (30, 60, 110); AGUA2 = (20, 40, 80)
NUVEM = (70, 70, 110); NUVEM2 = (50, 50, 85); MORRO = (25, 35, 55)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def nuvem(d, cx, cy, s=1.0, cor=NUVEM, brilho=0.0):
    c = tuple(int(cor[i] + (RAIO2[i] - cor[i]) * brilho * 0.6) for i in range(3))
    for dx, dy, r in ((-150, 20, 90), (-60, -30, 120), (60, -20, 110), (160, 25, 85), (0, 40, 100)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=c, outline=O, width=5)
    for dx, dy, r in ((-150, 20, 84), (-60, -30, 114), (60, -20, 104), (160, 25, 79), (0, 40, 94)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=c)


def raio(d, x0, y0, y1, semente, larg=14, cor=RAIO):
    """Raio em zigue-zague com galhos, de y0 até y1."""
    pts = [(x0, y0)]
    x, y, i = x0, y0, 0
    passo = (y1 - y0) / 7
    while y < y1 - 1:
        i += 1
        y = min(y1, y + passo)
        x += 55 * math.sin(semente * 3.7 + i * 2.3)
        pts.append((x, y))
    d.line(pts, fill=RAIO2, width=larg + 14)
    d.line(pts, fill=cor, width=larg)
    a, b = pts[3], pts[4]
    gx = a[0] + 90 * (1 if semente % 2 else -1)
    d.line([a, (gx, a[1] + 70), (gx + 20, a[1] + 140)], fill=cor, width=max(4, larg // 2))


def lago(d, y0, T, brilho=0.0):
    d.rectangle([0, y0, 1080, 1320], fill=AGUA)
    for i in range(6):
        y = y0 + 30 + i * 45
        off = 40 * math.sin(T * 1.5 + i)
        cor = tuple(int(AGUA2[k] + (RAIO2[k] - AGUA2[k]) * brilho * 0.5) for k in range(3))
        d.line([(80 + off, y), (420 + off, y)], fill=cor, width=6)
        d.line([(600 - off, y + 20), (980 - off, y + 20)], fill=cor, width=6)


def palafita(d, cx, cy, s=1.0, cor=(200, 120, 70)):
    for dx in (-60, 0, 60):
        d.line([(cx + dx * s, cy), (cx + dx * s, cy + 90 * s)], fill=O, width=int(10 * s))
    d.rectangle([cx - 90 * s, cy - 90 * s, cx + 90 * s, cy], fill=cor, outline=O, width=5)
    d.polygon([(cx - 110 * s, cy - 85 * s), (cx, cy - 160 * s), (cx + 110 * s, cy - 85 * s)], fill=(150, 60, 50), outline=O)
    d.rectangle([cx - 25 * s, cy - 60 * s, cx + 25 * s, cy - 20 * s], fill=(255, 220, 120), outline=O, width=3)


def flash(T, per=0.9, fase=0.0):
    """1 durante um piscar curto a cada 'per' segundos."""
    f = ((T + fase) % per) / per
    return 1.0 if f < 0.18 else 0.0


def g_raios(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    lago(d, 1050, T, 0.6)
    nuvem(d, 620, 690, 1.0, brilho=0.7)
    n = int(T / 0.6)
    raio(d, 540 + 60 * math.sin(n), 760, 1060, n, 16)
    if flash(T, 0.6, 0.3):
        raio(d, 780, 750, 1000, n + 1, 10)
    palafita(d, 860, 1060, 0.8)
    rotulo(d, 860, 1210, "VENEZUELA", 42, (255, 255, 255))


def c_catatumbo(d, img, t, T):
    selo(d)
    # mapa simples do Lago Maracaibo
    d.polygon([(360, 560), (720, 540), (760, 700), (720, 1000), (600, 1180), (450, 1150), (380, 960), (420, 760)],
              fill=(80, 150, 80), outline=O)
    d.polygon([(470, 620), (620, 610), (650, 760), (640, 960), (560, 1080), (480, 1020), (450, 820)], fill=AGUA, outline=O)
    rotulo(d, 555, 830, "LAGO", 44, (255, 255, 255))
    rotulo(d, 555, 885, "MARACAIBO", 44, (255, 255, 255))
    # foz do rio com raios piscando
    d.line([(660, 1150), (600, 1060), (575, 1030)], fill=(90, 160, 230), width=12)
    if flash(T, 0.5):
        raio(d, 650, 930, 1050, int(T * 2), 8)
    brilhos(d, 610, 1040, 70, T, 6, RAIO)
    rotulo(d, 820, 1160, "RIO CATATUMBO", 40, CIANO)
    # relógio de 9 horas
    d.ellipse([140, 1000, 320, 1180], fill=(245, 245, 250), outline=O, width=6)
    ang = -math.pi / 2 + min(1, t / 2.5) * 2 * math.pi * 0.75
    d.line([(230, 1090), (230 + 70 * math.cos(ang), 1090 + 70 * math.sin(ang))], fill=O, width=8)
    rotulo(d, 230, 1220, "9 HORAS", 46, AMARELO)


def c_por_minuto(d, img, t, T):
    selo(d)
    nuvem(d, 540, 680, 1.15, brilho=flash(T, 0.35))
    for i in range(3):
        if flash(T, 0.35, i * 0.11):
            raio(d, 300 + i * 240, 760, 1050, int(T * 3) + i, 11)
    lago(d, 1050, T, flash(T, 0.35))
    d.rounded_rectangle([700, 850, 1000, 1010], 26, fill=(15, 20, 40), outline=CIANO, width=6)
    contador(d, 850, 920, 28, t, 2.4, 92, "", AMARELO)
    rotulo(d, 850, 985, "POR MINUTO", 34, CIANO)


def c_recorde(d, img, t, T):
    selo(d)
    # globo com o ponto do recorde
    d.ellipse([200, 560, 640, 1000], fill=(50, 110, 190), outline=O, width=6)
    d.polygon([(360, 640), (470, 620), (520, 720), (470, 860), (430, 940), (390, 840), (330, 740)], fill=(80, 170, 90), outline=O)
    r = 22 + 10 * math.sin(T * 6)
    d.ellipse([410 - r, 690 - r, 410 + r, 690 + r], fill=AMARELO, outline=O, width=4)
    # troféu
    k = pop(min(1, t / 0.8))
    cx, cy = 800, 830
    d.polygon([(cx - 110 * k, cy - 140 * k), (cx + 110 * k, cy - 140 * k), (cx + 70 * k, cy + 10 * k), (cx - 70 * k, cy + 10 * k)],
              fill=AMARELO, outline=O)
    d.rectangle([cx - 20 * k, cy + 10 * k, cx + 20 * k, cy + 80 * k], fill=AMARELO, outline=O, width=4)
    d.rectangle([cx - 80 * k, cy + 80 * k, cx + 80 * k, cy + 115 * k], fill=(200, 140, 30), outline=O, width=4)
    rotulo(d, 800, 760, "Nº 1", 50, (255, 255, 255), traduzir=False)
    rotulo(d, 540, 1100, "~250 RAIOS", 60, RAIO)
    rotulo(d, 540, 1175, "POR KM² POR ANO", 44, CIANO)


def c_cta(d, img, t, T):
    g_raios(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="300 NOITES", titulo_y=400, desenho=g_raios, fundo=((40, 30, 90), (10, 10, 35)),
         fala="Nesse lago cai raio em até trezentas noites por ano! E o último fato é o pior."),
    dict(tipo="fato", titulo="CATATUMBO", desenho=c_catatumbo, fundo=((30, 50, 90), (10, 20, 45)),
         fala="É o Relâmpago do Catatumbo, na Venezuela. Segue a Maia, que piora: a tempestade pode durar nove horas seguidas."),
    dict(tipo="fato", titulo="SEM PARAR", desenho=c_por_minuto, fundo=((45, 35, 85), (15, 10, 40)),
         fala="Numa noite forte, caem até vinte e oito raios por minuto."),
    dict(tipo="fato", titulo="RECORDE", desenho=c_recorde, fundo=((30, 40, 80), (10, 15, 40)),
         fala="O Guinness diz que é o lugar com mais raios do planeta: quase duzentos e cinquenta por quilômetro quadrado, todo ano."),
    dict(tipo="cta", titulo="300 NOITES", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 30, 90), (10, 10, 35)),
         fala="Mas um dia esses raios sumiram. Segue a Maia pra ver a parte dois às seis da tarde. Porque nesse lago..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "catatumbo_p1.mp4"))
