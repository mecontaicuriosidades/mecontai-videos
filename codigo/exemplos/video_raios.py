"""Raios: mais quentes que o Sol, e o Brasil é campeão."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sol, termometro, brilhos, O


def nuvem(d, cx, cy, s, cor=(90, 95, 120)):
    for dx, dy, r in ((-120, 10, 80), (-40, -40, 100), (60, -20, 95), (140, 20, 70), (0, 30, 90)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=cor, outline=O, width=6)
    for dx, dy, r in ((-120, 10, 74), (-40, -40, 94), (60, -20, 89), (140, 20, 64), (0, 30, 84)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=cor)


def raio(d, x, y0, y1, T, seed=0, cor=(255, 245, 140)):
    rng = np.random.default_rng(seed + int(T * 6))
    pts, y, xx = [], y0, x
    while y < y1:
        pts.append((xx, y)); y += rng.uniform(40, 80); xx += rng.uniform(-50, 50)
    pts.append((xx, y1))
    d.line(pts, fill=(255, 255, 255), width=18); d.line(pts, fill=cor, width=9)


def piscando(T, f=1.3):
    return (T * f) % 1 < 0.18


def c_temp(d, img, t, T):
    termometro(d, 260, 1150, ease(t / 2), cor=(255, 230, 80), h=600)
    sol(d, 760, 640, 110, T)
    contador(d, 520, 1000, 30000, t, 2, 90, " °C", AMARELO)
    if t > 2.5: rotulo(d, 700, 860, "5x O SOL!", 64, (255, 140, 60))


def c_trovao(d, img, t, T):
    nuvem(d, 540, 560, 1.1)
    if piscando(T): raio(d, 540, 620, 1050, T, 1)
    for k in range(3):
        r = 80 + ((T * 200 + k * 90) % 300)
        d.arc([540 - r, 1050 - r, 540 + r, 1050 + r], 200, 340, fill=CIANO, width=8)
    if t > 1.5: rotulo(d, 540, 1170, "AR EXPLODINDO", 60, AMARELO)


def c_contar(d, img, t, T):
    nuvem(d, 300, 560, 0.8)
    if t < 0.6: raio(d, 300, 610, 1000, T, 2)
    n = min(9, int(t * 1.5))
    rotulo(d, 760, 720, f"{n}s", 130, AMARELO)
    if t > 2.5: rotulo(d, 640, 1000, "÷ 3 = DISTÂNCIA EM KM", 52, CIANO)


def c_brasil(d, img, t, T):
    d.polygon([(520, 520), (720, 580), (820, 720), (760, 920), (640, 1080), (540, 1040), (470, 880), (380, 760), (420, 620)],
              fill=(60, 170, 80), outline=O)
    rng = np.random.default_rng(int(T * 4))
    for i in range(5):
        x, y = rng.uniform(420, 760), rng.uniform(600, 1000)
        d.polygon([(x, y - 40), (x - 16, y + 4), (x + 2, y + 4), (x - 8, y + 42), (x + 20, y - 8), (x + 2, y - 8)], fill=AMARELO, outline=O)
    if t > 1.5: rotulo(d, 540, 1160, "CAMPEÃO MUNDIAL", 64, AMARELO)


def c_predio(d, img, t, T):
    nuvem(d, 540, 500, 1.0)
    d.rectangle([460, 760, 620, 1250], fill=(150, 160, 180), outline=O, width=7)
    d.rectangle([500, 640, 580, 760], fill=(150, 160, 180), outline=O, width=7)
    d.line([(540, 560), (540, 640)], fill=O, width=8)
    for k in range(10):
        for j in range(2): d.rectangle([480 + j * 80, 790 + k * 42, 520 + j * 80, 815 + k * 42], fill=(255, 230, 120))
    if piscando(T, 1.6): raio(d, 540, 540, 560, T, 3); raio(d, 545, 550, 640, T, 4)
    if t > 1.5: rotulo(d, 820, 760, "~20x\nPOR ANO".split("\n")[0], 70, AMARELO)
    if t > 1.8: rotulo(d, 820, 840, "POR ANO", 46, AMARELO)


def g_raio(d, img, t, T):
    nuvem(d, 560, 540, 1.2)
    if piscando(T, 1.0): raio(d, 520, 600, 1150, T, 5)
    brilhos(d, 560, 760, 420, T, 6, (255, 245, 140))


TEMP = ((30, 30, 60), (10, 10, 25))
CENAS = [
    dict(tipo="gancho", titulo="MAIS QUENTE QUE O SOL", desenho=g_raio, fundo=TEMP, estrelas=True,
         fala="Existe uma coisa na Terra mais quente que a superfície do Sol, e cai do céu milhões de vezes por ano aqui no Brasil!"),
    dict(tipo="fato", titulo="30 MIL GRAUS", desenho=c_temp, fundo=((60, 20, 60), (20, 5, 25)),
         fala="É o raio! Ele pode aquecer o ar a uns trinta mil graus. A superfície do Sol tem uns cinco mil e quinhentos. Ou seja, o raio é umas cinco vezes mais quente!"),
    dict(tipo="fato", titulo="O QUE É O TROVÃO?", desenho=c_trovao, fundo=TEMP, estrelas=True,
         fala="E o trovão é o barulho desse calor: o ar em volta do raio esquenta tão rápido que se expande de uma vez, como uma explosão."),
    dict(tipo="fato", titulo="CALCULE A DISTÂNCIA", desenho=c_contar, fundo=((40, 50, 90), (15, 20, 40)),
         fala="Dica de ouro: viu o clarão, conte os segundos até ouvir o trovão e divida por três. O resultado é mais ou menos a distância do raio em quilômetros!"),
    dict(tipo="fato", titulo="BRASIL CAMPEÃO DE RAIOS", desenho=c_brasil, fundo=((20, 40, 90), (8, 15, 40)),
         fala="E o Brasil é o país com mais raios do mundo, segundo o INPE: são dezenas de milhões por ano, por causa do clima quente e úmido e do tamanho do país."),
    dict(tipo="fato", titulo="CAI SIM DUAS VEZES!", desenho=c_predio, fundo=TEMP, estrelas=True,
         fala="E o mais bizarro: aquele ditado de que raio não cai duas vezes no mesmo lugar é mentira! O Empire State, em Nova York, é atingido umas vinte vezes por ano."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Tem medo de trovão?",
         fala="E você, tem medo de trovão ou acha bonito? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "raios.mp4"))
