"""Pirâmides do Egito: Cleópatra está mais perto de nós."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, sol, seta, brilhos, O

AREIA = (235, 195, 120)


def piramide(d, cx, base_y, w, h, cor=AREIA, branca=False):
    c = (245, 245, 235) if branca else cor
    d.polygon([(cx - w / 2, base_y), (cx, base_y - h), (cx + w / 2, base_y)], fill=c, outline=O)
    d.polygon([(cx, base_y - h), (cx + w / 2, base_y), (cx + w * 0.1, base_y)], fill=tuple(int(v * 0.85) for v in c))
    d.line([(cx - w / 2, base_y), (cx, base_y - h), (cx + w / 2, base_y), (cx - w / 2, base_y)], fill=O, width=7)
    if not branca:
        for k in range(1, 8):
            y = base_y - h * k / 8
            ww = w / 2 * (1 - k / 8)
            d.line([(cx - ww, y), (cx + ww, y)], fill=(190, 150, 80), width=4)


def c_altura(d, img, t, T):
    d.rectangle([0, 1050, 1080, 1250], fill=AREIA)
    piramide(d, 540, 1060, 760, 520 * ease(t / 1.5 + 0.2))
    if t > 1.5: rotulo(d, 540, 1140, "146 METROS", 70, AMARELO)
    if t > 2.3: rotulo(d, 540, 1220, "MAIS ALTA POR ~3.800 ANOS", 44)


def c_blocos(d, img, t, T):
    for i in range(int(36 * ease(t / 2.5))):
        x, y = 180 + (i % 9) * 82, 1060 - (i // 9) * 70
        d.rectangle([x, y, x + 76, y + 64], fill=AREIA, outline=O, width=4)
    if t > 1: contador(d, 540, 560, 2300000, t - 1, 2, 100, "", AMARELO)
    if t > 1: rotulo(d, 540, 650, "BLOCOS DE PEDRA", 46)


def c_linha(d, img, t, T):
    d.line([(100, 860), (980, 860)], fill="white", width=8)
    pts = [(140, "PIRÂMIDE", "2560 a.C.", AREIA, 0.5), (640, "CLEÓPATRA", "69 a.C.", (255, 120, 180), 1.5), (940, "LUA", "1969", CIANO, 2.5)]
    for x, n, a, c, ti in pts:
        if t > ti:
            d.ellipse([x - 22, 838, x + 22, 882], fill=c, outline=O, width=5)
            rotulo(d, x, 780, n, 40, c); rotulo(d, x, 940, a, 36)
    if t > 3: rotulo(d, 790, 1080, "MAIS PERTO!", 56, AMARELO)


def c_trabalhadores(d, img, t, T):
    d.rectangle([0, 1050, 1080, 1250], fill=AREIA)
    piramide(d, 760, 1060, 460, 300)
    for i in range(4):
        x = 120 + i * 120 + (t * 30) % 40
        d.ellipse([x - 22, 880, x + 22, 924], fill=(200, 140, 90), outline=O, width=4)
        d.rounded_rectangle([x - 26, 924, x + 26, 1010], 12, fill="white", outline=O, width=4)
        d.line([(x, 1010), (x, 1050)], fill=O, width=8)
    d.rectangle([90, 820, 560, 870], fill=AREIA, outline=O, width=4)
    if t > 1.5: rotulo(d, 540, 640, "PAGOS, NÃO ESCRAVOS", 54, AMARELO)


def c_branca(d, img, t, T):
    sol(d, 900, 640, 75, T)
    d.rectangle([0, 1050, 1080, 1250], fill=AREIA)
    piramide(d, 480, 1060, 680, 470, branca=True)
    brilhos(d, 480, 800, 300, T, 8, (255, 255, 255))
    if t > 1.5: rotulo(d, 540, 1150, "BRANCA E BRILHANTE", 58, AMARELO)


def g_pir(d, img, t, T):
    sol(d, 900, 680, 70, T)
    d.rectangle([0, 1050, 1080, 1250], fill=AREIA)
    piramide(d, 620, 1060, 620, 440)
    piramide(d, 300, 1060, 380, 260)


DESERTO = ((255, 190, 110), (240, 140, 80))
CENAS = [
    dict(tipo="gancho", titulo="CLEÓPATRA ESTÁ MAIS PERTO DE NÓS", desenho=g_pir, fundo=DESERTO,
         fala="A Cleópatra viveu mais perto do dia em que o homem pisou na Lua do que da construção das pirâmides. Calma, que eu te mostro a conta!"),
    dict(tipo="fato", titulo="A GRANDE PIRÂMIDE", desenho=c_altura, fundo=DESERTO,
         fala="A Grande Pirâmide de Gizé tinha uns cento e quarenta e seis metros de altura quando ficou pronta. Ela foi a construção mais alta feita pelo homem por uns três mil e oitocentos anos!"),
    dict(tipo="fato", titulo="MILHÕES DE BLOCOS", desenho=c_blocos, fundo=((200, 150, 90), (140, 95, 50)),
         fala="Ela foi feita com uns dois milhões e trezentos mil blocos de pedra. Muitos pesam mais de duas toneladas, o peso de um carro grande."),
    dict(tipo="fato", titulo="A CONTA DA CLEÓPATRA", desenho=c_linha, fundo=((40, 40, 90), (15, 15, 45)), estrelas=True,
         fala="Agora a conta: a pirâmide ficou pronta por volta de dois mil quinhentos e sessenta antes de Cristo. Cleópatra nasceu em sessenta e nove antes de Cristo. São uns dois mil e quinhentos anos de distância. Da Cleópatra até a chegada à Lua, em mil novecentos e sessenta e nove, são uns dois mil e quarenta. Ou seja, ela está mais perto de nós!"),
    dict(tipo="fato", titulo="QUEM CONSTRUIU?", desenho=c_trabalhadores, fundo=DESERTO,
         fala="E não foram escravos, como nos filmes. Arqueólogos acharam as vilas dos trabalhadores, com padarias e até túmulos deles. Eram equipes organizadas e alimentadas."),
    dict(tipo="fato", titulo="ELA ERA BRANCA!", desenho=c_branca, fundo=((140, 200, 255), (250, 210, 150)),
         fala="E o mais bizarro: a pirâmide não era dessa cor de areia. Ela era coberta de calcário branco polido, que brilhava no sol do deserto!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Já sabia da Cleópatra?",
         fala="Você já sabia dessa da Cleópatra? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "piramides.mp4"))
