"""Lago Nyos, Parte 2 (LUGARES MORTAIS #4). Formato v3 (25–35 s). Usa desenhos da Parte 1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, O
from video_nyos_p1 import etiqueta, selo, casinha, nuvem_gas, MORRO, MORRO2, LAGO, LAGO2, NEVOA

MAGMA = (240, 90, 30); MAGMA2 = (255, 170, 40); FUNDO_ESC = (15, 35, 70); VERMELHO = (190, 50, 40)


def corte_lago(d, T, y0=820, bolhas=1.0):
    """Lago em corte: água em cima, camada escura cheia de gás no fundo, magma embaixo."""
    d.polygon([(0, y0 - 40), (140, y0), (940, y0), (1080, y0 - 40), (1080, 1920), (0, 1920)], fill=MORRO2, outline=O)
    d.polygon([(140, y0), (940, y0), (820, y0 + 460), (260, y0 + 460)], fill=LAGO, outline=O)
    d.polygon([(200, y0 + 260), (880, y0 + 260), (820, y0 + 460), (260, y0 + 460)], fill=FUNDO_ESC)
    for i in range(14):
        x = 270 + (i * 47) % 540
        y = y0 + 290 + (i * 37) % 150 + 6 * math.sin(T * 4 + i)
        r = 10 + (i % 3) * 5
        d.ellipse([x - r, y - r, x + r, y + r], outline=(200, 240, 255), width=4)
    # magma
    for i in range(5):
        x = 200 + i * 170
        r = 70 + 10 * math.sin(T * 2 + i)
        d.ellipse([x - r, 1480 - r * 0.5, x + r, 1480 + r * 0.5], fill=MAGMA)
    d.rectangle([0, 1520, 1080, 1920], fill=MAGMA)
    d.ellipse([440, 1500, 640, 1560], fill=MAGMA2)


def g_bomba(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    corte_lago(d, T, 820)
    # placa de perigo
    a = 1 + 0.06 * math.sin(T * 6)
    x, y = 860, 640
    d.polygon([(x, y - 90 * a), (x - 80 * a, y + 50 * a), (x + 80 * a, y + 50 * a)], fill=AMARELO, outline=O, width=6)
    rotulo(d, x, y + 5, "!", 80, (20, 20, 20), traduzir=False)
    rotulo(d, 540, 1170, "GÁS", 56, "white")


def garrafa(d, x, y, T, abre):
    trem = 10 * math.sin(T * 30) if abre < 0.05 else 0
    x += trem
    d.rounded_rectangle([x - 70, y - 220, x + 70, y + 120], 40, fill=(110, 200, 120), outline=O, width=5)
    d.rectangle([x - 30, y - 300, x + 30, y - 210], fill=(110, 200, 120), outline=O, width=5)
    for i in range(6):
        f = (T * 0.8 + i / 6) % 1
        d.ellipse([x - 40 + i * 14 - 6, y + 90 - f * 280 - 6, x - 40 + i * 14 + 6, y + 90 - f * 280 + 6], fill="white")
    if abre > 0:
        d.rectangle([x - 36, y - 330 - 200 * abre, x + 36, y - 300 - 200 * abre], fill=(220, 50, 50), outline=O, width=4)
        for i in range(5):
            r = 40 + 25 * i * abre
            d.ellipse([x - r, y - 330 - 90 * i * abre - r * 0.5, x + r, y - 330 - 90 * i * abre + r * 0.5], fill=(240, 250, 255, 200))
    else:
        d.rectangle([x - 36, y - 330, x + 36, y - 300], fill=(220, 50, 50), outline=O, width=4)


def c_refri(d, img, t, T):
    selo(d)
    if t < 2.4:
        corte_lago(d, T, 820)
        seta(d, 540, 1470, 540, 1150, MAGMA2)
        rotulo(d, 540, 1640, "MAGMA", 60, "white")
        return
    abre = ease((t - 3.2) / 0.8) if t > 3.2 else 0
    garrafa(d, 540, 1150, T, abre)
    rotulo(d, 820, 1100, "TAMPADO", 50, AMARELO)


def c_vermelho(d, img, t, T):
    selo(d)
    k = ease((t - 0.6) / 2.2) if t > 0.6 else 0
    cor = tuple(int(a + (b - a) * k) for a, b in zip(LAGO, VERMELHO))
    cor2 = tuple(int(a * 0.7 + (b * 0.7 - a * 0.7) * k) for a, b in zip(LAGO2, VERMELHO))
    d.polygon([(-50, 1920), (-50, 900), (250, 760), (420, 1010), (660, 1010), (830, 760), (1130, 900), (1130, 1920)], fill=MORRO, outline=O)
    d.ellipse([200, 960, 880, 1180], fill=cor, outline=O, width=5)
    d.ellipse([280, 990, 800, 1140], fill=cor2)
    for i in range(5):  # água do fundo subindo
        f = (T * 0.5 + i / 5) % 1
        x = 320 + i * 110
        d.ellipse([x - 14, 1150 - f * 140 - 14, x + 14, 1150 - f * 140 + 14], fill=(200, 80, 60))
    if t > 1.8:
        rotulo(d, 540, 1350, "FERRO", 80, AMARELO)


def c_canos(d, img, t, T):
    selo(d)
    corte_lago(d, T, 900, 0.5)
    # cano do fundo até a superfície
    d.rectangle([515, 760, 565, 1340], fill=(170, 170, 185), outline=O, width=4)
    d.rectangle([470, 880, 610, 920], fill=(120, 120, 135), outline=O, width=4)  # balsa
    # chafariz
    h = 260 + 40 * math.sin(T * 5)
    for i in range(9):
        ang = -math.pi / 2 + (i - 4) * 0.12
        for j in range(6):
            f = (T * 1.5 + j / 6) % 1
            px = 540 + math.cos(ang) * h * 1.2 * f
            py = 760 + math.sin(ang) * h * 2.0 * f + 260 * f * f
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(200, 235, 255))
    if t > 1.2:
        rotulo(d, 830, 1100, "DESDE 2001", 54, AMARELO)


def c_cta(d, img, t, T):
    g_bomba(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="BOMBA VIVA", titulo_y=400, desenho=g_bomba, fundo=((30, 50, 100), (10, 20, 50)), estrelas=True,
         fala="Esse lago matou mil e setecentas pessoas... e ainda guarda gás no fundo! E a solução é bizarra."),
    dict(tipo="fato", titulo="REFRIGERANTE", desenho=c_refri, fundo=((60, 100, 150), (20, 40, 80)),
         fala="Segue pra mais lugar mortal: o gás sobe do magma e fica preso na água do fundo, como num refrigerante tampado."),
    dict(tipo="fato", titulo="LAGO VERMELHO", desenho=c_vermelho, fundo=((120, 70, 90), (50, 25, 45)),
         fala="Na noite da tragédia, a água do fundo subiu de uma vez, e o lago ficou vermelho, por causa do ferro."),
    dict(tipo="fato", titulo="A SOLUÇÃO", desenho=c_canos, fundo=((50, 110, 160), (20, 50, 90)),
         fala="A solução: desde 2001, canos puxam a água lá do fundo e o gás escapa aos poucos, num chafariz gigante."),
    dict(tipo="cta", titulo="BOMBA VIVA", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((30, 50, 100), (10, 20, 50)), estrelas=True,
         fala="Segue pra ver o próximo Lugares Mortais amanhã. Porque esse lago..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "nyos_p2.mp4"))
