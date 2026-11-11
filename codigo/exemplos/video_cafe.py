"""Café: das cabras dançantes ao Brasil campeão."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, brilhos, seta, O

CAFE = (100, 55, 30)


def xicara(d, cx, cy, s, T, rosto=True):
    for k in range(3):  # vapor
        x = cx - 40 * s + k * 40 * s
        pts = [(x + math.sin(T * 3 + j * 0.8 + k) * 12 * s, cy - 130 * s - j * 18 * s) for j in range(7)]
        d.line(pts, fill=(240, 240, 250), width=int(8 * s) + 1)
    d.rounded_rectangle([cx - 120 * s, cy - 110 * s, cx + 120 * s, cy + 90 * s], int(50 * s), fill="white", outline=O, width=7)
    d.ellipse([cx - 110 * s, cy - 125 * s, cx + 110 * s, cy - 85 * s], fill=CAFE, outline=O, width=5)
    d.arc([cx + 90 * s, cy - 70 * s, cx + 180 * s, cy + 30 * s], 270, 90, fill=O, width=int(14 * s))
    if rosto:
        olhos(d, cx, cy - 20 * s, T, 70 * s, 16 * s); sorriso(d, cx, cy + 25 * s, 25 * s)


def cabra(d, x, y, s, T):
    pulo = abs(math.sin(T * 4)) * 60 * s
    y -= pulo
    d.ellipse([x - 110 * s, y - 60 * s, x + 110 * s, y + 50 * s], fill=(245, 245, 240), outline=O, width=6)
    for k in (-70, -30, 30, 70):
        d.line([(x + k * s, y + 40 * s), (x + k * s + math.sin(T * 8 + k) * 15 * s, y + 120 * s)], fill=O, width=int(12 * s))
    d.ellipse([x + 80 * s, y - 120 * s, x + 170 * s, y - 30 * s], fill=(245, 245, 240), outline=O, width=6)
    d.ellipse([x + 130 * s, y - 95 * s, x + 145 * s, y - 80 * s], fill=O)
    d.arc([x + 70 * s, y - 170 * s, x + 130 * s, y - 100 * s], 180, 330, fill=(150, 120, 80), width=int(10 * s))


def c_cabras(d, img, t, T):
    for i in range(3): cabra(d, 220 + i * 320, 900, 0.75, T + i)
    if t > 1.5: rotulo(d, 540, 1150, "CABRAS AGITADAS!", 60, AMARELO)


def c_cereja(d, img, t, T):
    # galho com cerejas vermelhas; uma se abre mostrando 2 grãos
    d.line([(100, 650), (980, 700)], fill=(90, 60, 30), width=24)
    for i in range(6):
        x = 180 + i * 140
        d.ellipse([x - 45, 700, x + 45, 790], fill=(200, 30, 40), outline=O, width=5)
    if t > 1.2:
        s = pop((t - 1.2) / 0.5)
        for dx in (-50, 50):
            d.ellipse([540 + dx - 45 * s, 960 - 65 * s, 540 + dx + 45 * s, 960 + 65 * s], fill=(190, 160, 90), outline=O, width=5)
            d.line([(540 + dx, 900), (540 + dx, 1020)], fill=O, width=5)
        rotulo(d, 540, 1120, "CAFÉ É SEMENTE", 60, AMARELO)


def c_brasil(d, img, t, T):
    # mapa estilizado + saca de café
    d.polygon([(520, 500), (720, 560), (820, 700), (760, 900), (640, 1080), (540, 1040), (470, 880), (380, 760), (420, 600)],
              fill=(60, 170, 80), outline=O)
    for i in range(int(12 * ease(t / 2))):
        x, y = 520 + (i % 4) * 50, 760 + (i // 4) * 50
        d.ellipse([x - 16, y - 22, x + 16, y + 22], fill=CAFE, outline=O, width=3)
    if t > 1.5: rotulo(d, 540, 1170, "MAIOR PRODUTOR DO MUNDO", 52, AMARELO)


def c_adenosina(d, img, t, T):
    # cérebro com "chaves" (adenosina) bloqueadas pela cafeína
    d.ellipse([290, 520, 790, 900], fill=(250, 170, 190), outline=O, width=8)
    for k in range(5): d.arc([330 + k * 60, 560, 480 + k * 60, 860], 60, 300, fill=(220, 120, 150), width=6)
    for i in range(4):
        x = 360 + i * 120
        d.rectangle([x - 22, 910, x + 22, 960], fill=(150, 150, 170), outline=O, width=4)
        if t > 1 + i * 0.3:
            d.ellipse([x - 24, 960, x + 24, 1008], fill=CAFE, outline=O, width=4)
    if t > 2.2: rotulo(d, 540, 1120, "BLOQUEIA O CANSAÇO", 58, AMARELO)


def c_descafe(d, img, t, T):
    xicara(d, 540, 820, 1.4, T)
    if t > 1.0:
        d.rounded_rectangle([300, 1060, 780, 1150], 30, fill=(15, 20, 50), outline=AMARELO, width=6)
        rotulo(d, 540, 1105, "DESCAFEINADO", 46, AMARELO)
    if t > 2.0: rotulo(d, 540, 1210, "AINDA TEM UM POUQUINHO!", 44, (255, 140, 120))


def g_cafe(d, img, t, T):
    xicara(d, 600, 820, 1.5, T)
    brilhos(d, 600, 760, 330, T, 8)


CENAS = [
    dict(tipo="gancho", titulo="O SEGREDO DO CAFÉ", desenho=g_cafe, fundo=((90, 50, 25), (35, 18, 8)),
         fala="O café que você toma todo dia tem uma história que começou com cabras dançando! E no final eu te conto um segredo sobre o descafeinado."),
    dict(tipo="fato", titulo="AS CABRAS DE KALDI", desenho=c_cabras, fundo=((140, 200, 120), (70, 140, 70)),
         fala="Diz a lenda que um pastor da Etiópia, chamado Kaldi, percebeu que suas cabras ficavam agitadas, quase dançando, depois de comer umas frutinhas vermelhas. Eram frutos de café!"),
    dict(tipo="fato", titulo="É UMA SEMENTE", desenho=c_cereja, fundo=((250, 210, 170), (210, 150, 110)),
         fala="O grão de café, na verdade, é a semente de uma fruta vermelha parecida com uma cereja. Cada fruta tem, normalmente, duas sementes."),
    dict(tipo="fato", titulo="BRASIL CAMPEÃO", desenho=c_brasil, fundo=((40, 90, 160), (15, 40, 90)),
         fala="E o Brasil é o maior produtor de café do mundo, há mais de cento e cinquenta anos. Uma boa parte do café do planeta sai daqui!"),
    dict(tipo="fato", titulo="COMO ELE TE ACORDA", desenho=c_adenosina, fundo=((60, 30, 70), (25, 10, 30)),
         fala="Sabe como ele te acorda? Ao longo do dia, o cérebro acumula uma substância que dá sono, a adenosina. A cafeína se encaixa no lugar dela e bloqueia o sinal de cansaço."),
    dict(tipo="fato", titulo="O SEGREDO DO DESCAFEINADO", desenho=c_descafe, fundo=((120, 70, 40), (50, 25, 12)),
         fala="E o mais curioso: o café descafeinado não é zero cafeína! A maior parte é removida, mas sempre sobra um pouquinho em cada xícara."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Quantos cafés por dia?",
         fala="E aí, quantas xícaras de café você toma por dia? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "cafe.mp4"))
