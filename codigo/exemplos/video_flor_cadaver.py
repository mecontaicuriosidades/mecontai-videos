"""Flor-cadáver (BICHOS INSANOS #5). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, termometro, O

SERIE = "BICHOS INSANOS #5"
VINHO = (120, 20, 45); VINHO2 = (80, 10, 30); VERDE = (90, 140, 70); VERDE2 = (60, 100, 50)
ESPADICE = (230, 200, 120); ESPADICE2 = (200, 165, 90); FEDOR = (150, 200, 80)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def flor(d, cx, base, T, s=1.0, aberta=1.0):
    """Flor gigante: pétala (espata) vinho em forma de saia + espádice amarela alta."""
    # caule/vaso
    d.rectangle([cx - 40 * s, base - 40 * s, cx + 40 * s, base + 120 * s], fill=VERDE2, outline=O, width=5)
    # espádice (coluna)
    h = 560 * s
    d.polygon([(cx - 55 * s, base - 200 * s), (cx - 22 * s, base - 200 * s - h), (cx + 22 * s, base - 200 * s - h),
               (cx + 55 * s, base - 200 * s)], fill=ESPADICE, outline=O)
    d.ellipse([cx - 24 * s, base - 225 * s - h, cx + 24 * s, base - 175 * s - h], fill=ESPADICE, outline=O, width=4)
    d.line([(cx - 10 * s, base - 260 * s), (cx - 4 * s, base - 140 * s - h)], fill=ESPADICE2, width=int(8 * s))
    # espata (saia) aberta
    w = (170 + 120 * aberta) * s
    pts = [(cx - w, base - 300 * s), (cx - w * 0.6, base - 330 * s - 30 * math.sin(T * 2) * s), (cx, base - 280 * s),
           (cx + w * 0.6, base - 330 * s + 30 * math.sin(T * 2) * s), (cx + w, base - 300 * s), (cx + 120 * s, base - 20 * s),
           (cx - 120 * s, base - 20 * s)]
    d.polygon(pts, fill=VINHO, outline=O)
    d.polygon([(cx - w * 0.75, base - 290 * s), (cx, base - 270 * s), (cx + w * 0.75, base - 290 * s), (cx + 90 * s, base - 60 * s),
               (cx - 90 * s, base - 60 * s)], fill=VINHO2)
    # babado verde por fora
    d.line([(cx - w, base - 300 * s), (cx - 120 * s, base - 20 * s)], fill=VERDE, width=int(10 * s))
    d.line([(cx + w, base - 300 * s), (cx + 120 * s, base - 20 * s)], fill=VERDE, width=int(10 * s))


def fedor(d, cx, cy, T, n=4, alt=300):
    for i in range(n):
        f = (T * 0.5 + i / n) % 1
        x = cx - 160 + i * (320 / max(1, n - 1))
        y = cy - f * alt
        a = int(230 * (1 - f))
        for j in range(3):
            yy = y - j * 40
            off = 22 * math.sin(T * 4 + i + j)
            d.arc([x - 30 + off, yy - 20, x + 30 + off, yy + 20], 180 if j % 2 else 0, 360 if j % 2 else 180,
                  fill=FEDOR + (a,), width=9)


def mosca(d, x, y, T, s=1.0):
    a = 12 * math.sin(T * 40)
    d.ellipse([x - 26 * s, y - 14 * s - a, x + 2 * s, y + 4 * s], fill=(220, 240, 255, 180), outline=O, width=2)
    d.ellipse([x - 2 * s, y - 14 * s + a, x + 26 * s, y + 4 * s], fill=(220, 240, 255, 180), outline=O, width=2)
    d.ellipse([x - 14 * s, y - 6 * s, x + 14 * s, y + 18 * s], fill=(30, 40, 30), outline=O, width=2)
    d.ellipse([x - 8 * s, y - 12 * s, x + 8 * s, y + 2 * s], fill=(170, 30, 30))


def regua(d, x, y0, y1):
    d.rectangle([x - 22, y1, x + 22, y0], fill=(250, 230, 120), outline=O, width=4)
    for i in range(7):
        y = y0 - i * (y0 - y1) / 6
        d.line([(x - 22, y), (x, y)], fill=O, width=4)


def g_flor(d, img, t, T):
    etiqueta(d)
    flor(d, 560, 1280, T, 0.9)
    regua(d, 900, 1250, 560)
    rotulo(d, 900, 520, "3 M", 50, AMARELO)
    fedor(d, 560, 860, T, 4, 150)
    for i in range(3):
        a = T * 2 + i * 2.1
        mosca(d, 560 + 260 * math.cos(a), 900 + 120 * math.sin(a * 1.3), T + i)


def ilha(d, T):
    d.rectangle([0, 1000, 1080, 1300], fill=(40, 110, 170))
    for i in range(6):
        x = (i * 200 + T * 40) % 1200 - 60
        d.arc([x, 1020, x + 90, 1060], 180, 360, fill=(200, 230, 255), width=6)
    d.polygon([(130, 980), (300, 760), (520, 700), (760, 780), (950, 990)], fill=VERDE, outline=O)
    for x in (300, 460, 620, 780):
        d.line([(x, 980), (x + 10, 820)], fill=(110, 70, 40), width=14)
        d.ellipse([x - 70, 760, x + 90, 850], fill=VERDE2, outline=O, width=4)


def c_sumatra(d, img, t, T):
    selo(d)
    if t < 2.3:
        ilha(d, T)
        rotulo(d, 540, 600, "SUMATRA", 64, AMARELO)
        rotulo(d, 540, 1180, "INDONÉSIA", 50, "white")
        return
    flor(d, 380, 1250, T, 0.75)
    fedor(d, 380, 860, T, 3, 200)
    for i in range(4):
        x = 700 + 120 * math.sin(T * 2 + i * 1.5)
        y = 700 + i * 120
        mosca(d, x, y, T + i, 1.3)
    rotulo(d, 820, 1100, "MOSCAS", 46, "white")
    rotulo(d, 820, 1150, "BESOUROS", 46, "white")


def c_esquenta(d, img, t, T):
    selo(d)
    flor(d, 400, 1260, T, 0.8)
    # ondas de calor ao redor da coluna
    for i in range(3):
        f = (T * 0.7 + i / 3) % 1
        r = 80 + f * 150
        d.ellipse([400 - r, 860 - r * 1.4, 400 + r, 860 + r * 1.4], outline=(255, 140, 40, int(220 * (1 - f))), width=8)
    termometro(d, 860, 1220, min(1, t / 2.6) * 0.8, (235, 80, 40), 600)
    if t > 1.5:
        rotulo(d, 860, 560, "QUASE 36 °C", 46, AMARELO)


def calendario(d, cx, cy, T, k):
    d.rounded_rectangle([cx - 170, cy - 150, cx + 170, cy + 170], 24, fill="white", outline=O, width=6)
    d.rectangle([cx - 170, cy - 150, cx + 170, cy - 70], fill=(200, 50, 60), outline=O, width=6)
    for r in range(3):
        for c in range(4):
            x, y = cx - 120 + c * 80, cy - 30 + r * 65
            d.rectangle([x - 22, y - 20, x + 22, y + 20], fill=(220, 225, 235))
    # folhas voando (anos passando)
    for i in range(3):
        f = (T * 0.9 + i / 3) % 1
        x, y = cx + 120 + f * 200, cy - 120 - f * 260
        d.rectangle([x - 40, y - 30, x + 40, y + 30], fill=(255, 255, 255, int(220 * (1 - f))), outline=O + (int(220 * (1 - f)),), width=3)


def c_rara(d, img, t, T):
    selo(d)
    if t < 2.6:
        calendario(d, 340, 860, T, t)
        rotulo(d, 340, 1130, "ANOS", 64, AMARELO)
        flor(d, 820, 1250, T, 0.5, aberta=0.0)
    else:
        k = min(1, (t - 2.6) / 1.0)
        flor(d, 540, 1270, T, 0.75, aberta=k)
        p = pop((t - 2.6) / 0.4)
        rotulo(d, 540, 560, "SÓ 1 OU 2 DIAS", int(70 * max(0.3, p)), AMARELO)


def c_cta(d, img, t, T):
    g_flor(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="FEDE!", titulo_y=400, desenho=g_flor, fundo=((40, 70, 50), (15, 30, 20)),
         fala="Essa flor tem três metros e fede a carne podre! E o último fato é o pior."),
    dict(tipo="fato", titulo="FLOR-CADÁVER", desenho=c_sumatra, fundo=((60, 120, 90), (25, 60, 40)),
         fala="É a flor-cadáver, da ilha de Sumatra. Segue a Maia, que piora: o fedor atrai moscas e besouros de carniça."),
    dict(tipo="fato", titulo="ESQUENTA", desenho=c_esquenta, fundo=((150, 60, 40), (80, 25, 20)),
         fala="Pra espalhar o cheiro, ela esquenta sozinha, quase na temperatura do corpo humano."),
    dict(tipo="fato", titulo="RARIDADE", desenho=c_rara, fundo=((70, 50, 110), (30, 20, 60)),
         fala="E o pior: ela pode levar anos pra florir, e a flor aberta dura só um ou dois dias."),
    dict(tipo="cta", titulo="FEDE!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 70, 50), (15, 30, 20)),
         fala="Segue a Maia: amanhã tem mais Bichos Insanos. Porque essa flor..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "flor_cadaver.mp4"))
