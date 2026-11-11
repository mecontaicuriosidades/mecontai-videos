"""Coração humano: o motor que nunca descansa."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, terra, seta, brilhos, O

VERM = (225, 45, 70)


def coracao(d, cx, cy, r, T, bate=True, rosto=True, cor=VERM):
    k = 1 + (0.08 * max(0, math.sin(T * 7.5)) if bate else 0)
    r *= k
    d.ellipse([cx - r, cy - r * 0.9, cx + r * 0.05, cy + r * 0.15], fill=cor, outline=O, width=7)
    d.ellipse([cx - r * 0.05, cy - r * 0.9, cx + r, cy + r * 0.15], fill=cor, outline=O, width=7)
    d.polygon([(cx - r * 0.97, cy - r * 0.25), (cx + r * 0.97, cy - r * 0.25), (cx, cy + r * 1.05)], fill=cor)
    d.line([(cx - r * 0.97, cy - r * 0.2), (cx, cy + r * 1.05), (cx + r * 0.97, cy - r * 0.2)], fill=O, width=7)
    d.rectangle([cx - r * 0.75, cy - r * 0.45, cx + r * 0.75, cy - r * 0.15], fill=cor)
    if rosto:
        olhos(d, cx, cy - r * 0.3, T, r * 0.6, r * 0.13); sorriso(d, cx, cy + r * 0.1, r * 0.22)


def ecg(d, y, T, cor=(120, 255, 140)):
    pts = []
    for x in range(60, 1020, 6):
        f = ((x / 300) - T * 1.2) % 1
        v = -120 if 0.48 < f < 0.5 else (60 if 0.5 < f < 0.52 else (-20 if 0.3 < f < 0.36 else 0))
        pts.append((x, y + v))
    d.line(pts, fill=cor, width=7)


def c_batidas(d, img, t, T):
    coracao(d, 540, 650, 200, T)
    ecg(d, 1000, T)
    contador(d, 540, 1170, 100000, t, 2.5, 96, "", AMARELO)
    rotulo(d, 540, 1245, "BATIDAS POR DIA", 40)


def c_litros(d, img, t, T):
    # caixa d'água enchendo
    d.rounded_rectangle([300, 520, 780, 1050], 40, fill=(230, 240, 255), outline=O, width=8)
    h = 500 * ease(t / 3)
    d.rounded_rectangle([315, 1035 - h, 765, 1035], 30, fill=VERM)
    coracao(d, 540, 400 + 0 * t, 60, T, rosto=False) if False else None
    contador(d, 540, 1170, 7000, t, 3, 96, " L", AMARELO)
    rotulo(d, 540, 1245, "DE SANGUE POR DIA", 40)


def c_vasos(d, img, t, T):
    terra(d, 540, 760, 230, T)
    for k in range(int(1 + 2 * ease(t / 3))):
        r = 290 + k * 45
        d.arc([540 - r, 760 - r * 0.45, 540 + r, 760 + r * 0.45], 0, 360, fill=VERM, width=12)
    if t > 1: rotulo(d, 540, 1120, "100 MIL KM", 90, AMARELO)
    if t > 2: rotulo(d, 540, 1210, "MAIS DE 2 VOLTAS NA TERRA", 44)


def c_eletrico(d, img, t, T):
    coracao(d, 540, 680, 190, T)
    for k in range(3):
        a = T * 3 + k * 2.1
        x, y = 540 + math.cos(a) * 270, 680 + math.sin(a) * 230
        d.polygon([(x, y - 40), (x - 18, y + 5), (x + 2, y + 5), (x - 10, y + 45), (x + 22, y - 8), (x + 2, y - 8)], fill=AMARELO, outline=O)
    if t > 1.5: rotulo(d, 540, 1120, "TEM ELETRICIDADE PRÓPRIA", 52, AMARELO)


def c_baleia(d, img, t, T):
    # coração de baleia-azul x humano
    coracao(d, 400, 760, 300, T * 0.3, rosto=True, cor=(70, 110, 200))
    coracao(d, 860, 1000, 45, T)
    rotulo(d, 400, 1170, "BALEIA-AZUL", 50, CIANO)
    rotulo(d, 860, 1090, "VOCÊ", 40, AMARELO)


def c_punho(d, img, t, T):
    coracao(d, 380, 750, 150, T)
    rotulo(d, 540, 750, "=", 110, AMARELO)
    # punho
    d.rounded_rectangle([640, 620, 900, 880], 70, fill=(252, 214, 188), outline=O, width=8)
    for k in range(4): d.line([(660 + k * 60, 650), (660 + k * 60, 750)], fill=O, width=6)
    if t > 1.2: rotulo(d, 540, 1100, "DO TAMANHO DO SEU PUNHO", 50)


def g_cor(d, img, t, T):
    coracao(d, 600, 760, 230, T)
    ecg(d, 1130, T)


CENAS = [
    dict(tipo="gancho", titulo="O MOTOR QUE NUNCA PARA", desenho=g_cor, fundo=((70, 10, 30), (25, 5, 15)),
         fala="Tem um órgão no seu corpo que trabalha sem parar desde antes de você nascer. E ele dá conta de um trabalho absurdo, olha só!"),
    dict(tipo="fato", titulo="DO TAMANHO DE UM PUNHO", desenho=c_punho, fundo=((255, 150, 160), (210, 80, 110)),
         fala="O coração de um adulto tem mais ou menos o tamanho de uma mão fechada e pesa uns trezentos gramas."),
    dict(tipo="fato", titulo="100 MIL BATIDAS POR DIA", desenho=c_batidas, fundo=((20, 20, 40), (5, 5, 15)), estrelas=True,
         fala="Mesmo pequeno, ele bate umas cem mil vezes por dia. Em uma vida inteira, passa de dois bilhões e meio de batidas!"),
    dict(tipo="fato", titulo="UMA CAIXA D'ÁGUA DE SANGUE", desenho=c_litros, fundo=((90, 20, 40), (40, 8, 20)),
         fala="E em cada dia, ele bombeia uns sete mil litros de sangue. É o suficiente pra encher várias caixas d'água!"),
    dict(tipo="fato", titulo="CAMINHO GIGANTE", desenho=c_vasos, fundo=((15, 20, 60), (5, 5, 25)), estrelas=True,
         fala="Esse sangue corre por uma rede de vasos que, se fosse esticada, teria cerca de cem mil quilômetros. Dá mais de duas voltas ao redor da Terra!"),
    dict(tipo="fato", titulo="ELETRICIDADE PRÓPRIA", desenho=c_eletrico, fundo=((40, 10, 60), (15, 5, 30)),
         fala="E o mais bizarro: o coração tem o próprio sistema elétrico. Ele não depende do cérebro pra bater. Por isso, num transplante, ele volta a bater no corpo de outra pessoa."),
    dict(tipo="fato", titulo="E O DA BALEIA-AZUL?", desenho=c_baleia, fundo=((30, 90, 170), (10, 35, 80)),
         fala="E só pra comparar: o coração de uma baleia-azul pesa uns cento e oitenta quilos, mais do que duas pessoas adultas juntas!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Qual número te assustou mais?",
         fala="Qual desses números te assustou mais? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "coracao.mp4"))
