"""Formigas: 20 quatrilhões de agricultoras e engenheiras."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, terra, brilhos, O

MARROM = (120, 55, 30)


def formiga(d, x, y, s, T, cor=MARROM, carga=None):
    p = math.sin(T * 12) * 6 * s
    for k in (-1, 0, 1):
        d.line([(x + k * 22 * s, y), (x + k * 30 * s - 10 * s, y + 38 * s + p * k)], fill=O, width=int(5 * s) + 1)
        d.line([(x + k * 22 * s, y), (x + k * 30 * s + 10 * s, y - 38 * s - p * k)], fill=O, width=int(5 * s) + 1)
    for (dx, r) in ((-42, 20), (0, 15), (40, 18)):
        d.ellipse([x + dx * s - r * s, y - r * s, x + dx * s + r * s, y + r * s], fill=cor, outline=O, width=int(3 * s) + 1)
    d.line([(x + 52 * s, y - 10 * s), (x + 75 * s, y - 35 * s)], fill=O, width=int(4 * s) + 1)
    if carga:
        d.ellipse([x - 30 * s, y - 95 * s, x + 30 * s, y - 25 * s], fill=carga, outline=O, width=int(4 * s) + 1)


def c_numero(d, img, t, T):
    terra(d, 540, 760, 230, T)
    rng = np.random.default_rng(3)
    for i in range(int(40 * ease(t / 2))):
        a = rng.uniform(0, 6.28); r = rng.uniform(240, 420)
        formiga(d, 540 + math.cos(a + T * 0.2) * r, 760 + math.sin(a + T * 0.2) * r * 0.9, 0.35, T + i)
    if t > 1.2: rotulo(d, 540, 1170, "20 QUATRILHÕES", 80, AMARELO)


def c_forca(d, img, t, T):
    formiga(d, 540, 880, 4.0, T, carga=(120, 200, 90))
    if t > 1: rotulo(d, 540, 1150, "ATÉ 50x O PRÓPRIO PESO", 54, AMARELO)


def c_fungos(d, img, t, T):
    # folha cortada levada até o "jardim" de fungos
    for i in range(4):
        x = 100 + ((t * 120 + i * 260) % 900)
        formiga(d, x, 680, 1.4, T + i, carga=(80, 180, 80))
    d.ellipse([280, 900, 800, 1150], fill=(110, 70, 40), outline=O, width=7)
    for k in range(14):
        x, y = 330 + (k % 7) * 70, 960 + (k // 7) * 80
        d.ellipse([x - 26, y - 22, x + 26, y + 22], fill=(245, 240, 220), outline=O, width=3)
    if t > 1.5: rotulo(d, 540, 860, "HORTA DE FUNGOS", 50, AMARELO)


def c_ponte(d, img, t, T):
    d.rectangle([0, 900, 380, 1250], fill=(110, 80, 50)); d.rectangle([700, 900, 1080, 1250], fill=(110, 80, 50))
    n = int(8 * ease(t / 2.5))
    for i in range(n):
        x = 390 + i * 40
        formiga(d, x, 905 + math.sin(i * 0.4) * 30, 0.5, T + i)
    if t > 2.5:
        for i in range(3): formiga(d, 100 + ((t * 160 + i * 300) % 900), 840, 0.5, T + i)
        rotulo(d, 540, 1150, "PONTE VIVA", 70, AMARELO)


def c_respira(d, img, t, T):
    formiga(d, 540, 760, 4.8, T)
    for k in range(5):
        x = 340 + k * 100; r = 14 + 8 * math.sin(T * 4 + k)
        d.ellipse([x - r, 800 - r, x + r, 800 + r], outline=CIANO, width=7)
    if t > 1.2: rotulo(d, 540, 1100, "SEM PULMÃO", 64, AMARELO)


def c_rainha(d, img, t, T):
    # coroa + formiga grande
    formiga(d, 540, 840, 4.2, T, cor=(150, 70, 40))
    d.polygon([(440, 700), (470, 610), (510, 660), (540, 590), (570, 660), (610, 610), (640, 700)], fill=AMARELO, outline=O)
    contador(d, 540, 1120, 28, t, 2, 110, " ANOS", AMARELO)


def g_form(d, img, t, T):
    for i in range(6):
        formiga(d, 150 + ((t * 140 + i * 170) % 900), 700 + (i % 2) * 140, 0.9, T + i, carga=(90, 190, 90) if i % 2 else None)
    brilhos(d, 540, 760, 400, T, 6)


TERRA = ((150, 105, 60), (80, 50, 25))
CENAS = [
    dict(tipo="gancho", titulo="AS DONAS DO PLANETA", desenho=g_form, fundo=((120, 190, 110), (60, 120, 60)),
         fala="Pra cada pessoa no mundo, existem uns dois milhões e meio de formigas. E elas fazem coisas que parecem de outro mundo."),
    dict(tipo="fato", titulo="20 QUATRILHÕES", desenho=c_numero, fundo=((20, 20, 50), (5, 5, 20)), estrelas=True,
         fala="Um estudo de dois mil e vinte e dois estimou que existem uns vinte quatrilhões de formigas na Terra. É um dois seguido de dezesseis zeros!"),
    dict(tipo="fato", titulo="SUPER FORÇA", desenho=c_forca, fundo=((150, 210, 255), (90, 160, 90)),
         fala="E elas são fortíssimas pro tamanho: algumas carregam de dez a cinquenta vezes o próprio peso."),
    dict(tipo="fato", titulo="AGRICULTORAS", desenho=c_fungos, fundo=TERRA,
         fala="As formigas cortadeiras não comem as folhas que carregam. Elas usam as folhas pra cultivar um fungo, e comem o fungo. Elas fazem agricultura há milhões de anos!"),
    dict(tipo="fato", titulo="ENGENHEIRAS", desenho=c_ponte, fundo=((140, 200, 240), (80, 140, 200)),
         fala="Algumas espécies usam o próprio corpo pra construir pontes e jangadas vivas, pra colônia inteira atravessar buracos ou até enchentes."),
    dict(tipo="fato", titulo="RESPIRAM PELO CORPO", desenho=c_respira, fundo=((60, 40, 30), (25, 15, 10)),
         fala="Elas nem têm pulmão! O ar entra por buraquinhos espalhados pelo corpo e vai direto pra dentro, por tubinhos."),
    dict(tipo="fato", titulo="RAINHA DE LONGA VIDA", desenho=c_rainha, fundo=((90, 30, 80), (35, 10, 35)),
         fala="E o mais bizarro: enquanto muitas operárias vivem só alguns meses, uma rainha de formiga-preta-de-jardim chegou a viver uns vinte e oito anos em laboratório!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Qual fato foi o mais doido?",
         fala="Qual desses fatos sobre as formigas foi o mais doido pra você? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "formigas.mp4"))
