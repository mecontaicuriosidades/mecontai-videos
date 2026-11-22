"""Peixe-carneiro / sheepshead (BICHOS INSANOS #7). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "BICHOS INSANOS #7"
PEIXE = (205, 210, 215); PEIXE2 = (150, 158, 168); LISTRA = (35, 35, 45); DENTE = (250, 248, 235)
GENGIVA = (220, 110, 120); AREIA = (225, 200, 140); CONCHA = (240, 220, 190)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def dentes_frente(d, cx, cy, s=1.0, abre=1.0):
    """Boca aberta com dentes quadrados tipo incisivos humanos."""
    h = 60 * s * abre
    d.rounded_rectangle([cx - 110 * s, cy - h - 30 * s, cx + 110 * s, cy + h + 30 * s], int(40 * s), fill=GENGIVA, outline=O, width=6)
    d.rectangle([cx - 90 * s, cy - h * 0.6, cx + 90 * s, cy + h * 0.6], fill=(90, 30, 40))
    for fila, y0, y1 in ((0, cy - h - 18 * s, cy - h * 0.3), (1, cy + h * 0.3, cy + h + 18 * s)):
        for i in range(4):
            x = cx - 88 * s + i * 44 * s
            d.rounded_rectangle([x, y0, x + 40 * s, y1], int(8 * s), fill=DENTE, outline=O, width=4)


def peixe(d, cx, cy, s=1.0, T=0.0, boca=1.0, olho=True):
    """Peixe-carneiro de lado, virado para a esquerda, com listras escuras verticais."""
    rabo = 12 * math.sin(T * 4)
    d.polygon([(cx + 230 * s, cy), (cx + 360 * s, cy - 110 * s + rabo), (cx + 340 * s, cy + rabo * 0.3), (cx + 360 * s, cy + 110 * s + rabo)],
              fill=PEIXE2, outline=O)
    # nadadeira de cima com espinhos
    d.polygon([(cx - 80 * s, cy - 150 * s), (cx - 40 * s, cy - 230 * s), (cx + 40 * s, cy - 215 * s), (cx + 120 * s, cy - 200 * s),
               (cx + 200 * s, cy - 120 * s)], fill=PEIXE2, outline=O)
    d.ellipse([cx - 260 * s, cy - 170 * s, cx + 260 * s, cy + 160 * s], fill=PEIXE, outline=O, width=6)
    for i in range(6):
        x = cx - 150 * s + i * 65 * s
        d.line([(x, cy - 150 * s + abs(i - 2.5) * 8 * s), (x + 10 * s, cy + 140 * s - abs(i - 2.5) * 8 * s)], fill=LISTRA, width=int(26 * s))
    d.ellipse([cx - 260 * s, cy - 170 * s, cx + 260 * s, cy + 160 * s], outline=O, width=6)
    # cabeça arredondada e olho
    if olho:
        d.ellipse([cx - 200 * s, cy - 110 * s, cx - 130 * s, cy - 40 * s], fill=(255, 255, 255), outline=O, width=5)
        d.ellipse([cx - 180 * s, cy - 90 * s, cx - 150 * s, cy - 60 * s], fill=O)
    # boca com dentes humanos na ponta
    dentes_frente(d, cx - 255 * s, cy + 40 * s, 0.55 * s, boca)


def bolhas(d, T, n=8):
    for i in range(n):
        f = (T * 0.25 + i * 0.13) % 1
        x = 120 + (i * 137) % 860 + 20 * math.sin(T + i)
        y = 1250 - f * 700
        r = 8 + (i % 3) * 5
        d.ellipse([x - r, y - r, x + r, y + r], outline=(200, 240, 255), width=3)


def g_dentes(d, img, t, T):
    etiqueta(d)
    bolhas(d, T, 7)
    abre = 0.75 + 0.25 * math.sin(T * 3)
    peixe(d, 640, 870, 1.0, T, abre)
    # dentes em destaque (lupa)
    d.ellipse([170, 560, 470, 860], fill=(30, 80, 120), outline=AMARELO, width=10)
    dentes_frente(d, 320, 710, 1.0, abre)
    d.line([(450, 840), (390, 790)], fill=AMARELO, width=16)
    rotulo(d, 700, 1090, "DENTES DE GENTE?", 46, AMARELO)


def c_onde(d, img, t, T):
    selo(d)
    # mapa do Atlântico com faixa do Canadá até o sul do Brasil
    d.polygon([(130, 520), (360, 520), (420, 700), (330, 780), (360, 860), (520, 900), (560, 1000), (520, 1150), (440, 1280), (390, 1280),
               (420, 1100), (360, 980), (250, 860), (180, 700)], fill=(90, 160, 90), outline=O)
    k = min(1, t / 2.0)
    d.line([(430, 560), (480, 760), (600, 920), (650, 1080), (560, 560 + 700 * k)][:2 + int(k * 3)], fill=AMARELO, width=14)
    rotulo(d, 290, 590, "CANADÁ", 40, (255, 255, 255))
    rotulo(d, 470, 1150, "BRASIL", 40, (255, 255, 255))
    peixe(d, 800, 850, 0.48, T, 0.8)
    rotulo(d, 800, 1010, "ATÉ 90 CM", 44, CIANO)


def c_molares(d, img, t, T):
    selo(d)
    # mandíbula vista de cima com molares em fileiras
    d.ellipse([200, 560, 880, 1160], fill=GENGIVA, outline=O, width=7)
    d.ellipse([330, 700, 750, 1160], fill=(90, 30, 40))
    for fila in range(3):
        for i in range(7):
            ang = math.pi * (0.1 + 0.8 * i / 6)
            r = 300 - fila * 45
            x = 540 - math.cos(ang) * r
            y = 980 - math.sin(ang) * r * 1.05
            d.ellipse([x - 26, y - 22, x + 26, y + 22], fill=DENTE, outline=O, width=4)
    # concha sendo esmagada
    k = (t % 1.4) / 1.4
    cx, cy = 540, 900
    if k < 0.6:
        d.polygon([(cx - 70, cy + 30), (cx, cy - 60), (cx + 70, cy + 30)], fill=CONCHA, outline=O)
        for j in range(3):
            d.line([(cx, cy - 55), (cx - 40 + j * 40, cy + 28)], fill=(180, 150, 110), width=4)
    else:
        for j in range(6):
            a = j * 1.05
            x = cx + math.cos(a) * 80 * (k - 0.5) * 2; y = cy + math.sin(a) * 60 * (k - 0.5) * 2
            d.polygon([(x - 18, y), (x, y - 16), (x + 18, y + 6)], fill=CONCHA, outline=O)
        rotulo(d, 540, 820, "CRAC!", 54, AMARELO)
    rotulo(d, 540, 1220, "CONCHAS E CRACAS", 48, (255, 255, 255))


def carneiro(d, cx, cy, s=1.0, T=0.0):
    for i in range(9):
        a = i * 0.7
        x = cx + math.cos(a) * 110 * s; y = cy + math.sin(a) * 70 * s
        d.ellipse([x - 60 * s, y - 60 * s, x + 60 * s, y + 60 * s], fill=(245, 245, 240), outline=O, width=4)
    d.ellipse([cx - 80 * s, cy - 70 * s, cx + 80 * s, cy + 70 * s], fill=(245, 245, 240))
    hx, hy = cx - 150 * s, cy - 30 * s
    d.ellipse([hx - 70 * s, hy - 60 * s, hx + 60 * s, hy + 80 * s], fill=(70, 60, 60), outline=O, width=5)
    d.ellipse([hx - 40 * s, hy - 30 * s, hx - 15 * s, hy - 5 * s], fill=(255, 255, 255))
    # boca com dentinhos
    d.rounded_rectangle([hx - 60 * s, hy + 40 * s, hx + 10 * s, hy + 70 * s], int(8 * s), fill=DENTE, outline=O, width=3)
    for i in range(3):
        x = hx - 50 * s + i * 20 * s
        d.line([(x + 10 * s, hy + 40 * s), (x + 10 * s, hy + 70 * s)], fill=O, width=3)
    for lx in (-50, 10, 60, 110):
        d.line([(cx + lx * s, cy + 60 * s), (cx + lx * s, cy + 150 * s)], fill=O, width=int(14 * s))


def c_nome(d, img, t, T):
    selo(d)
    carneiro(d, 760, 720, 0.9, T)
    peixe(d, 400, 1040, 0.62, T, 0.9)
    k = pop(min(1, t / 0.6))
    rotulo(d, 560, 880, "=", int(110 * k) + 1, AMARELO, traduzir=False)
    rotulo(d, 790, 1180, "DENTES PARECIDOS", 44, CIANO)


def c_cta(d, img, t, T):
    g_dentes(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="DENTES!", titulo_y=400, desenho=g_dentes, fundo=((30, 110, 150), (10, 45, 80)),
         fala="Esse peixe tem dentes de gente! E o último fato é o mais estranho."),
    dict(tipo="fato", titulo="PEIXE-CARNEIRO", desenho=c_onde, fundo=((30, 100, 140), (10, 45, 75)),
         fala="É o peixe-carneiro, que vive do Canadá até o sul do Brasil. Segue pra mais bicho insano: na frente, ele tem dentes quadradinhos iguais aos nossos."),
    dict(tipo="fato", titulo="MOLARES", desenho=c_molares, fundo=((40, 90, 120), (15, 40, 60)),
         fala="E lá atrás, fileiras de molares, pra triturar conchas e cracas."),
    dict(tipo="fato", titulo="O NOME", desenho=c_nome, fundo=((60, 120, 110), (20, 55, 50)),
         fala="E o nome vem justamente desses dentes: eles lembram os dentes de um carneiro."),
    dict(tipo="cta", titulo="DENTES!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((30, 110, 150), (10, 45, 80)),
         fala="Segue a Maia: amanhã tem mais Bichos Insanos. Porque esse peixe..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "peixe_carneiro.mp4"))
