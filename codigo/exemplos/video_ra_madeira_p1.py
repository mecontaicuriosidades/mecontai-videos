"""Rã-da-madeira, Parte 1 (BICHOS INSANOS #6). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "BICHOS INSANOS #6"
RA = (190, 135, 80); RA2 = (140, 95, 55); BARRIGA = (235, 215, 170); MASCARA = (70, 45, 30)
GELO = (190, 235, 255); GELO2 = (130, 200, 240); NEVE = (245, 250, 255)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def ra(d, cx, cy, s=1.0, gelo=0.0, T=0.0, olho_aberto=True):
    """Rã-da-madeira sentada, vista de frente/lado, com a 'máscara' escura atrás do olho.
    gelo de 0 a 1 cobre o corpo de azul-gelo e cristais."""
    def mix(c):
        return tuple(int(c[i] * (1 - gelo * 0.7) + GELO[i] * gelo * 0.7) for i in range(3))
    corpo, corpo2, barriga = mix(RA), mix(RA2), mix(BARRIGA)
    # patas traseiras dobradas
    for lado in (-1, 1):
        d.ellipse([cx + lado * 150 * s - 110 * s, cy + 10 * s, cx + lado * 150 * s + 110 * s, cy + 150 * s], fill=corpo2, outline=O, width=5)
        d.ellipse([cx + lado * 230 * s - 70 * s, cy + 120 * s, cx + lado * 230 * s + 70 * s, cy + 165 * s], fill=corpo, outline=O, width=4)
    # corpo
    d.ellipse([cx - 190 * s, cy - 160 * s, cx + 190 * s, cy + 150 * s], fill=corpo, outline=O, width=6)
    d.ellipse([cx - 110 * s, cy - 40 * s, cx + 110 * s, cy + 140 * s], fill=barriga)
    # patas dianteiras
    for lado in (-1, 1):
        x = cx + lado * 85 * s
        d.rounded_rectangle([x - 22 * s, cy + 40 * s, x + 22 * s, cy + 150 * s], int(20 * s), fill=corpo, outline=O, width=4)
        d.ellipse([x - 40 * s, cy + 135 * s, x + 40 * s, cy + 170 * s], fill=corpo, outline=O, width=4)
    # cabeça
    d.ellipse([cx - 170 * s, cy - 260 * s, cx + 170 * s, cy - 60 * s], fill=corpo, outline=O, width=6)
    # olhos com máscara
    for lado in (-1, 1):
        ex, ey = cx + lado * 95 * s, cy - 225 * s
        d.polygon([(ex, ey + 10 * s), (ex + lado * 110 * s, ey + 50 * s), (ex + lado * 70 * s, ey + 85 * s), (ex - lado * 10 * s, ey + 45 * s)],
                  fill=mix(MASCARA))
        d.ellipse([ex - 48 * s, ey - 48 * s, ex + 48 * s, ey + 48 * s], fill=corpo, outline=O, width=5)
        if olho_aberto:
            d.ellipse([ex - 30 * s, ey - 30 * s, ex + 30 * s, ey + 30 * s], fill=(255, 210, 90), outline=O, width=3)
            d.ellipse([ex - 22 * s, ey - 8 * s, ex + 22 * s, ey + 8 * s], fill=O)
        else:
            d.line([(ex - 30 * s, ey), (ex + 30 * s, ey)], fill=O, width=int(6 * s))
    # boca
    d.arc([cx - 90 * s, cy - 170 * s, cx + 90 * s, cy - 90 * s], 20, 160, fill=O, width=int(5 * s))
    # gelo por cima
    if gelo > 0.05:
        a = int(110 * gelo)
        d.ellipse([cx - 200 * s, cy - 170 * s, cx + 200 * s, cy + 160 * s], outline=GELO2 + (a + 100,), width=int(8 * s))
        for i in range(9):
            ang = i * 0.7 + 0.3
            x = cx + math.cos(ang) * 140 * s
            y = cy - 50 * s + math.sin(ang * 1.3) * 140 * s
            r = (14 + 6 * math.sin(T * 3 + i)) * s * gelo
            d.polygon([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)], fill=NEVE + (220,), outline=O)


def bloco_gelo(d, cx, cy, w, h):
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], 40, outline=(230, 250, 255), width=10)
    d.rounded_rectangle([cx - w + 14, cy - h + 14, cx + w - 14, cy + h - 14], 30, outline=GELO2, width=4)
    d.line([(cx - w + 40, cy - h + 40), (cx - w + 120, cy - h + 40)], fill=NEVE, width=10)
    d.line([(cx - w + 40, cy - h + 70), (cx - w + 80, cy - h + 70)], fill=NEVE, width=10)


def flocos(d, T, n=14, y0=600, y1=1300):
    for i in range(n):
        f = (T * 0.15 + i * 0.137) % 1
        x = (i * 173) % 1080 + 25 * math.sin(T + i)
        y = y0 + f * (y1 - y0)
        r = 7 + (i % 3) * 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=NEVE + (200,))


def g_congela(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    flocos(d, T, 16, 520, 1320)
    k = 0.5 + 0.5 * math.sin(T * 1.1)
    ra(d, 560, 1030, 1.15, gelo=k, T=T, olho_aberto=k < 0.5)
    bloco_gelo(d, 560, 950, 300, 300)
    rotulo(d, 880, 620, "-18 °C", 54, GELO)


def c_metade(d, img, t, T):
    selo(d)
    k = min(1, ease(t / 2.6))
    # rã grande, gelo subindo de baixo para cima
    ra(d, 540, 1020, 1.2, gelo=k * 0.8, T=T)
    nivel = 1230 - 330 * k
    y = 1225
    while y > nivel:
        d.line([(260, y), (820, y)], fill=GELO2, width=3)
        y -= 34
    d.line([(250, nivel), (830, nivel)], fill=NEVE, width=8)
    rotulo(d, 540, 560, "MAIS DA METADE", 58, GELO)
    rotulo(d, 540, 625, "VIRA GELO", 58, GELO)


def coracao(d, cx, cy, s, cor):
    d.ellipse([cx - 60 * s, cy - 50 * s, cx + 5 * s, cy + 15 * s], fill=cor, outline=O, width=4)
    d.ellipse([cx - 5 * s, cy - 50 * s, cx + 60 * s, cy + 15 * s], fill=cor, outline=O, width=4)
    d.polygon([(cx - 58 * s, cy - 5 * s), (cx + 58 * s, cy - 5 * s), (cx, cy + 75 * s)], fill=cor)
    d.line([(cx - 58 * s, cy - 5 * s), (cx, cy + 75 * s), (cx + 58 * s, cy - 5 * s)], fill=O, width=4)


def c_parou(d, img, t, T):
    selo(d)
    # monitor de batimento que fica reto
    d.rounded_rectangle([140, 600, 940, 900], 30, fill=(15, 30, 30), outline=O, width=8)
    pts = []
    for i in range(80):
        x = 170 + i * 9.5
        fase = x / 760 + T * 0.6
        amp = max(0, 1 - t / 2.2)
        y = 750
        if (fase * 3) % 1 < 0.08:
            y -= 110 * amp * math.sin(((fase * 3) % 1) / 0.08 * math.pi)
        pts.append((x, y))
    d.line(pts, fill=(80, 255, 140), width=7)
    coracao(d, 330, 1080, 1.4, (120, 160, 200) if t > 2.2 else (230, 60, 80))
    d.ellipse([560, 980, 860, 1180], fill=GELO + (140,), outline=O, width=5)
    rotulo(d, 710, 1080, "SEM AR", 50, NEVE)
    if t > 2.2:
        rotulo(d, 330, 1230, "PAROU", 48, AMARELO)


def c_alasca(d, img, t, T):
    selo(d)
    flocos(d, T, 20, 480, 1300)
    # chão de neve com folhas e a rã congelada embaixo
    d.rectangle([0, 980, 1080, 1320], fill=(230, 240, 250))
    d.polygon([(0, 980), (200, 950), (420, 990), (640, 945), (860, 985), (1080, 955), (1080, 990), (0, 990)], fill=NEVE)
    for i in range(8):
        x = 160 + i * 110
        d.ellipse([x - 40, 1080 + (i % 2) * 20, x + 40, 1110 + (i % 2) * 20], fill=(170, 110, 60), outline=O, width=3)
    ra(d, 540, 1160, 0.55, gelo=1.0, T=T, olho_aberto=False)
    # calendário de meses passando
    meses = min(7, int(t / 0.45) + 1)
    d.rounded_rectangle([140, 600, 460, 860], 24, fill=(250, 250, 250), outline=O, width=6)
    d.rectangle([140, 600, 460, 660], fill=(220, 60, 70), outline=O, width=6)
    rotulo(d, 300, 770, str(meses), 120, (40, 40, 60), traduzir=False)
    rotulo(d, 760, 660, "ATÉ 7 MESES", 54, AMARELO)
    rotulo(d, 760, 780, "-18 °C", 64, GELO)


def c_cta(d, img, t, T):
    g_congela(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="CONGELA!", titulo_y=400, desenho=g_congela, fundo=((40, 90, 140), (15, 35, 70)),
         fala="Essa rã congela inteira no inverno... e volta à vida! E o último fato é o pior."),
    dict(tipo="fato", titulo="RÃ-DA-MADEIRA", desenho=c_metade, fundo=((60, 120, 170), (20, 50, 90)),
         fala="É a rã-da-madeira, dos Estados Unidos e do Canadá. Segue a Maia, que piora: no frio, mais da metade do corpo dela vira gelo."),
    dict(tipo="fato", titulo="DESLIGADA", desenho=c_parou, fundo=((50, 50, 90), (20, 20, 45)),
         fala="O coração para de bater, e ela para de respirar."),
    dict(tipo="fato", titulo="NO ALASCA", desenho=c_alasca, fundo=((90, 120, 160), (40, 55, 90)),
         fala="No Alasca, ela fica assim por até sete meses, a dezoito graus abaixo de zero."),
    dict(tipo="cta", titulo="CONGELA!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 90, 140), (15, 35, 70)),
         fala="E como ela revive é o mais louco. Segue a Maia pra ver a parte dois às seis da tarde. Porque essa rã..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "ra_madeira_p1.mp4"))
