"""Caño Cristales, Colômbia (LUGARES MORTAIS #2). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, O

SERIE = "LUGARES MORTAIS #2"
VERM = (225, 40, 70); AMAR = (250, 205, 50); VERDE = (70, 175, 90); AZUL = (60, 150, 230); PRETO = (45, 40, 55)
PEDRA = (95, 85, 90); MATA = (40, 110, 60); MATA2 = (25, 80, 45)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def margens(d, y0, y1):
    d.rectangle([0, y0, 1080, y1], fill=MATA2)
    for i in range(9):
        x = i * 135 + 40
        d.ellipse([x - 90, y0 - 70, x + 90, y0 + 60], fill=MATA, outline=O, width=5)


def rio(d, y0, y1, T, cores=(VERM, AMAR, VERDE, AZUL, VERM, PRETO, AMAR)):
    """Rio em perspectiva com faixas de cor ondulando."""
    d.rectangle([0, y0, 1080, y1], fill=AZUL)
    n = len(cores)
    for k, cor in enumerate(cores):
        yy = y0 + (y1 - y0) * k / n
        hh = (y1 - y0) / n
        pts = []
        for x in range(0, 1101, 40):
            pts.append((x, yy + math.sin(x / 110 + T * 2 + k) * 14))
        for x in range(1100, -1, -40):
            pts.append((x, yy + hh + math.sin(x / 110 + T * 2 + k + 1) * 14))
        d.polygon(pts, fill=cor)
    # pedras pretas e brilho da água
    for i in range(6):
        x = (i * 190 + 70) % 1080
        y = y0 + 40 + (i * 97) % (y1 - y0 - 80)
        d.ellipse([x - 55, y - 25, x + 55, y + 25], fill=PRETO, outline=O, width=4)
    for i in range(10):
        x = (i * 113 + T * 140) % 1180 - 50
        y = y0 + 20 + (i * 61) % (y1 - y0 - 40)
        d.line([(x, y), (x + 60, y)], fill=(255, 255, 255, 170), width=6)


def g_rio(d, img, t, T):
    etiqueta(d)
    margens(d, 650, 1300)
    rio(d, 750, 1200, T)
    # arco-íris derretendo
    for k, cor in enumerate((VERM, AMAR, VERDE, AZUL)):
        r = 330 - k * 34
        d.arc([540 - r, 650 - r * 0.25, 540 + r, 650 + r * 0.25], 180, 360, fill=cor, width=30)
        for j in range(3):
            x = 540 - r + 15 + j * (2 * r - 30) / 2
            gota = 30 + 25 * abs(math.sin(T * 2 + k + j))
            d.line([(x, 650), (x, 650 + gota)], fill=cor, width=18)
    rotulo(d, 820, 1230, "RIO ARCO-ÍRIS", 60, AMARELO)


def planta(d, x, y, s, T):
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * 0.28 + 0.12 * math.sin(T * 2.5 + i)
        x2, y2 = x + math.cos(a) * 140 * s, y + math.sin(a) * 140 * s
        d.line([(x, y), (x2, y2)], fill=VERM, width=int(18 * s))
        d.ellipse([x2 - 16 * s, y2 - 16 * s, x2 + 16 * s, y2 + 16 * s], fill=(250, 90, 120), outline=O, width=3)


def c_planta(d, img, t, T):
    selo(d)
    # água vista de lado
    d.rectangle([0, 560, 1080, 1260], fill=(90, 170, 225, 200))
    for i in range(8):
        x = (i * 150 + T * 90) % 1200 - 60
        d.ellipse([x, 600 + (i * 37) % 120, x + 22, 622 + (i * 37) % 120], outline="white", width=4)
    # pedras do fundo com a planta
    for k, (px, pw) in enumerate(((220, 260), (560, 300), (900, 240))):
        d.ellipse([px - pw / 2, 1050, px + pw / 2, 1260], fill=PEDRA, outline=O, width=6)
        for j in range(3):
            planta(d, px - pw / 3 + j * pw / 3, 1080, 0.9, T + k)
    if t > 0.8:
        rotulo(d, 540, 820, "É UMA PLANTA!", 76, "white")


def calendario(d, x, y, T, t):
    meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    for i, m in enumerate(meses):
        cx = x + (i % 4) * 190
        cy = y + (i // 4) * 120
        ativo = 5 <= i <= 10
        cor = VERM if ativo and t > 0.6 + (i - 5) * 0.15 else (150, 150, 170)
        d.rounded_rectangle([cx - 80, cy - 45, cx + 80, cy + 45], 18, fill=cor, outline=O, width=5)
        rotulo(d, cx, cy, m, 40, "white")


def protetor(d, x, y, T):
    d.rounded_rectangle([x - 60, y - 130, x + 60, y + 110], 30, fill=(255, 245, 210), outline=O, width=6)
    d.rectangle([x - 40, y - 175, x + 40, y - 130], fill=(250, 140, 40), outline=O, width=5)
    d.ellipse([x - 35, y - 60, x + 35, y + 10], fill=AMAR, outline=O, width=4)
    d.line([(x - 120, y - 170), (x + 120, y + 150)], fill=(230, 30, 40), width=22)


def c_meses(d, img, t, T):
    selo(d)
    calendario(d, 255, 560, T, t)
    if t > 2.6:
        protetor(d, 540, 1100, T)
        rotulo(d, 820, 1180, "PROIBIDO", 50, AMARELO)


def c_guerrilha(d, img, t, T):
    selo(d)
    margens(d, 820, 1300)
    rio(d, 940, 1260, T)
    # cerca / placa de fechado
    for i in range(7):
        x = 120 + i * 140
        d.rectangle([x - 12, 760, x + 12, 960], fill=(150, 110, 70), outline=O, width=4)
    d.line([(100, 800), (980, 800)], fill=(150, 110, 70), width=14)
    d.line([(100, 900), (980, 900)], fill=(150, 110, 70), width=14)
    k = pop(t / 0.5)
    d.rounded_rectangle([540 - 260 * k, 560, 540 + 260 * k, 720], 20, fill=(200, 40, 40), outline=O, width=6)
    if k > 0.8:
        rotulo(d, 540, 640, "FECHADO", 80, "white")
    if t > 2.8:
        s = pop((t - 2.8) / 0.4)
        rotulo(d, 820, 1210, "ATÉ 2009", int(80 * s) + 1, AMARELO)


def c_cta(d, img, t, T):
    g_rio(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="5 CORES", titulo_y=400, desenho=g_rio, fundo=((120, 200, 240), (60, 140, 210)),
         fala="Esse rio tem cinco cores e parece um arco-íris derretido! E o último fato é o pior."),
    dict(tipo="fato", titulo="COLÔMBIA", desenho=c_planta, fundo=((120, 200, 240), (60, 140, 210)),
         fala="É o Caño Cristales, na Colômbia. Segue a Maia, que piora: o vermelho é uma planta grudada nas pedras do fundo."),
    dict(tipo="fato", titulo="SÓ ÀS VEZES", desenho=c_meses, fundo=((70, 60, 110), (30, 25, 60)),
         fala="O show só dura alguns meses por ano. E é proibido entrar na água com protetor solar, porque faz mal à planta."),
    dict(tipo="fato", titulo="GUERRILHA", desenho=c_guerrilha, fundo=((90, 90, 110), (40, 40, 60)),
         fala="E o pior: por anos a guerrilha dominou a região, e o rio ficou fechado pra turistas até 2009."),
    dict(tipo="cta", titulo="5 CORES", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((120, 200, 240), (60, 140, 210)),
         fala="Segue a Maia: amanhã tem mais Lugares Mortais. Porque esse rio..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "cano_cristales.mp4"))
