"""Kawah Ijen, Indonésia (LUGARES MORTAIS #3). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, termometro, O

SERIE = "LUGARES MORTAIS #3"
ROCHA = (70, 60, 75); ROCHA2 = (45, 38, 52)
AZUL1 = (60, 140, 255); AZUL2 = (140, 220, 255); AZUL3 = (230, 250, 255)
TURQ = (70, 210, 200); TURQ2 = (40, 160, 165); ENXOFRE = (250, 215, 40); ENXOFRE2 = (210, 170, 20)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def chama_azul(d, x, base, h, T, i=0, w=60):
    """Chama azul tremulando (3 camadas)."""
    for cor, k in ((AZUL1, 1.0), (AZUL2, 0.68), (AZUL3, 0.35)):
        hh = h * k * (0.85 + 0.15 * math.sin(T * 9 + i * 1.7))
        ww = w * k
        sw = 18 * k * math.sin(T * 7 + i)
        d.polygon([(x - ww, base), (x - ww * 0.6, base - hh * 0.45), (x + sw, base - hh),
                   (x + ww * 0.6, base - hh * 0.5), (x + ww, base)], fill=cor)


def vulcao(d, T, y_topo=720):
    d.polygon([(-60, 1250), (300, y_topo), (780, y_topo), (1140, 1250)], fill=ROCHA, outline=O)
    d.polygon([(330, y_topo + 20), (750, y_topo + 20), (700, y_topo + 90), (380, y_topo + 90)], fill=ROCHA2)
    for i in range(4):  # rachaduras
        x = 180 + i * 230
        d.line([(x, 1250), (x + 40, 1130), (x + 10, 1060)], fill=ROCHA2, width=8)


def g_fogo(d, img, t, T):
    etiqueta(d)
    vulcao(d, T, 760)
    # rio de chama azul descendo a encosta
    for i in range(9):
        x = 230 + i * 80
        base = 1130 - abs(i - 4) * 25
        chama_azul(d, x, base, 220 + 60 * (i % 3), T, i)
    # fumaça
    for i in range(3):
        y = 740 - ((T * 40 + i * 40) % 110)
        d.ellipse([480 + i * 50 - 60, y - 40, 480 + i * 50 + 60, y + 40], fill=(200, 200, 220, 120))


def mapa_indonesia(d, T):
    ilhas = [[(110, 760), (360, 700), (420, 760), (250, 830), (120, 820)],
             [(380, 900), (700, 880), (760, 930), (420, 960)],
             [(620, 720), (800, 700), (820, 800), (650, 820)],
             [(850, 780), (980, 760), (1000, 840), (870, 860)]]
    for il in ilhas:
        d.polygon(il, fill=(140, 190, 110), outline=O, width=5)
    rotulo(d, 540, 640, "INDONÉSIA", 56, "white")
    x, y = 720, 915
    a = 34 + 8 * math.sin(T * 4)
    d.ellipse([x - a, y - a, x + a, y + a], outline=AMARELO, width=7)
    rotulo(d, 720, 1010, "JAVA", 44, AMARELO)


def c_gas(d, img, t, T):
    selo(d)
    if t < 1.8:
        mapa_indonesia(d, T)
        return
    # rachadura soltando gás amarelo que vira chama azul
    d.rectangle([0, 1080, 1080, 1250], fill=ROCHA)
    d.polygon([(380, 1080), (440, 1080), (420, 1250), (400, 1250)], fill=ROCHA2)
    for i in range(6):
        fase = (T * 0.8 + i / 6) % 1
        y = 1070 - fase * 260
        r = 22 + 30 * fase
        d.ellipse([410 - r + 30 * math.sin(T * 3 + i), y - r, 410 + r + 30 * math.sin(T * 3 + i), y + r],
                  fill=(240, 230, 120, int(200 * (1 - fase))))
    chama_azul(d, 410, 830, 260, T, 0, 90)
    rotulo(d, 410, 520, "ENXOFRE", 50, ENXOFRE)
    k = ease((t - 2.0) / 1.5)
    termometro(d, 820, 1180, 0.25 + 0.7 * k, cor=AZUL1, h=520)
    rotulo(d, 820, 590, "600 °C", 62, AMARELO)


def c_lago(d, img, t, T):
    selo(d)
    # cratera com lago turquesa visto de cima/lado
    d.polygon([(0, 700), (1080, 700), (1080, 1250), (0, 1250)], fill=ROCHA)
    d.ellipse([90, 760, 990, 1180], fill=TURQ, outline=O, width=6)
    d.ellipse([170, 800, 910, 1120], fill=TURQ2)
    for i in range(6):
        fase = (T * 0.5 + i / 6) % 1
        x = 220 + i * 120
        y = 1060 - fase * 200
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(220, 255, 250), width=4)
    # escala de pH
    k = ease(t / 2.0)
    for i in range(8):
        cor = (230 - i * 10, 60 + i * 22, 60 + i * 15)
        d.rectangle([140 + i * 100, 560, 230 + i * 100, 640], fill=cor, outline=O, width=3)
    rotulo(d, 185, 680, "0", 40, "white")
    rotulo(d, 885, 680, "7", 40, "white")
    xm = 900 - (900 - 175) * k
    d.polygon([(xm, 555), (xm - 24, 515), (xm + 24, 515)], fill=AMARELO, outline=O)
    if t > 1.6:
        rotulo(d, 540, 960, "ÁCIDO!", 90, "white")


def mineiro(d, x, y, T, k):
    """Mineiro carregando dois cestos de enxofre numa vara."""
    bal = 8 * math.sin(T * 5)
    d.line([(x - 22, y + 150), (x - 30 + bal, y + 260)], fill=(70, 60, 50), width=22)  # pernas
    d.line([(x + 22, y + 150), (x + 30 - bal, y + 260)], fill=(70, 60, 50), width=22)
    d.rounded_rectangle([x - 50, y + 10, x + 50, y + 160], 30, fill=(90, 120, 160), outline=O, width=5)
    d.ellipse([x - 40, y - 70, x + 40, y + 10], fill=(200, 150, 110), outline=O, width=5)
    d.rectangle([x - 40, y - 30, x + 40, y], fill=(230, 230, 230))  # pano no rosto
    d.line([(x - 260, y + 20), (x + 260, y + 20)], fill=(150, 110, 60), width=14)  # vara
    for sx in (-1, 1):
        cx = x + sx * 220
        d.line([(cx - 60, y + 20), (cx - 70, y + 110)], fill=O, width=4)
        d.line([(cx + 60, y + 20), (cx + 70, y + 110)], fill=O, width=4)
        d.rounded_rectangle([cx - 90, y + 110, cx + 90, y + 210], 20, fill=(150, 110, 60), outline=O, width=5)
        for j in range(4):
            bx = cx - 60 + j * 40
            d.polygon([(bx - 26, y + 115), (bx, y + 60 - (j % 2) * 20), (bx + 26, y + 115)], fill=ENXOFRE, outline=ENXOFRE2)


def c_mineiros(d, img, t, T):
    selo(d)
    # encosta subindo
    d.polygon([(0, 1250), (1080, 820), (1080, 1250)], fill=ROCHA)
    s = min(1, t / 3.5)
    x = 300 + 260 * s
    y = 880 - 110 * s
    mineiro(d, x, y, T, s)
    if t > 1.3:
        p = pop((t - 1.3) / 0.4)
        rotulo(d, 540, 560, "ATÉ 90 KG", int(84 * max(0.3, p)), AMARELO)


def c_cta(d, img, t, T):
    g_fogo(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="FOGO AZUL", titulo_y=400, desenho=g_fogo, fundo=((20, 25, 60), (5, 8, 25)),
         fala="Esse vulcão solta fogo azul! E o último fato é o pior."),
    dict(tipo="fato", titulo="O GÁS", desenho=c_gas, fundo=((30, 40, 90), (10, 15, 45)), estrelas=True,
         fala="É o Kawah Ijen, na Indonésia. Segue a Maia, que piora: o azul é gás de enxofre pegando fogo, a até seiscentos graus."),
    dict(tipo="fato", titulo="LAGO ÁCIDO", desenho=c_lago, fundo=((90, 110, 140), (40, 50, 80)),
         fala="Na cratera tem o maior lago muito ácido do mundo, quase tão ácido quanto ácido de bateria."),
    dict(tipo="fato", titulo="MINEIROS", desenho=c_mineiros, fundo=((120, 90, 130), (60, 40, 70)),
         fala="E mesmo assim, mineiros descem lá pra tirar enxofre e sobem carregando até noventa quilos nas costas."),
    dict(tipo="cta", titulo="FOGO AZUL", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((20, 25, 60), (5, 8, 25)),
         fala="Segue a Maia: amanhã tem mais Lugares Mortais. Porque esse vulcão..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "kawah_ijen.mp4"))
