"""Água: o gelo que salvou a vida na Terra."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, terra, seta, brilhos, O

AZ = (70, 160, 240)


def gota(d, cx, cy, r, T, rosto=True, cor=AZ):
    d.polygon([(cx, cy - r * 1.8), (cx - r * 0.85, cy - r * 0.3), (cx + r * 0.85, cy - r * 0.3)], fill=cor)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor, outline=O, width=7)
    d.line([(cx - r * 0.85, cy - r * 0.45), (cx, cy - r * 1.8), (cx + r * 0.85, cy - r * 0.45)], fill=O, width=7)
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.25, cy - r * 0.2], fill=(220, 240, 255))
    if rosto:
        olhos(d, cx, cy, T, r * 0.7, r * 0.15); sorriso(d, cx, cy + r * 0.4, r * 0.25)


def cubo_gelo(d, cx, cy, s):
    d.rounded_rectangle([cx - 70 * s, cy - 70 * s, cx + 70 * s, cy + 70 * s], int(20 * s), fill=(220, 245, 255), outline=O, width=6)
    d.line([(cx - 40 * s, cy - 40 * s), (cx - 10 * s, cy - 50 * s)], fill="white", width=8)


def c_flutua(d, img, t, T):
    d.rounded_rectangle([280, 560, 800, 1100], 30, outline=O, width=9, fill=(235, 245, 255))
    d.rectangle([292, 760, 788, 1088], fill=AZ)
    cubo_gelo(d, 540, 760 + math.sin(T * 2) * 10, 1.1)
    if t > 1.5: rotulo(d, 540, 1170, "GELO É MAIS LEVE", 60, AMARELO)


def c_lago(d, img, t, T):
    d.rectangle([140, 600, 940, 1100], fill=(40, 110, 200), outline=O, width=8)
    d.rectangle([140, 600, 940, 680], fill=(220, 245, 255), outline=O, width=6)
    for i in range(3):
        x = 260 + ((T * 90 + i * 250) % 640)
        y = 850 + i * 70
        d.ellipse([x - 50, y - 22, x + 50, y + 22], fill=(255, 160, 60), outline=O, width=4)
        d.polygon([(x - 48, y), (x - 90, y - 26), (x - 90, y + 26)], fill=(255, 160, 60), outline=O)
    if t > 1.5: rotulo(d, 540, 1180, "PEIXES VIVOS EMBAIXO", 56, AMARELO)


def c_salgada(d, img, t, T):
    terra(d, 540, 760, 260, T)
    # barra de 100 gotas: 97 salgadas, 3 doces
    for i in range(20):
        x = 120 + i * 44
        cor = (60, 120, 210) if i < 19 else (120, 220, 255)
        d.ellipse([x - 18, 1080 - 18, x + 18, 1080 + 18], fill=cor, outline=O, width=3)
    if t > 1: rotulo(d, 540, 1170, "97% SALGADA", 66, AMARELO)


def c_gelo_doce(d, img, t, T):
    for k in range(5):  # geleiras
        d.polygon([(100 + k * 190, 1050), (190 + k * 190, 650 + (k % 2) * 80), (290 + k * 190, 1050)], fill=(225, 245, 255), outline=O)
    if t > 1: rotulo(d, 540, 1170, "~2/3 DA ÁGUA DOCE: GELO", 52, AMARELO)


def c_dino(d, img, t, T):
    # gota passando por dinossauro -> nuvem -> copo
    d.ellipse([140, 760, 420, 920], fill=(110, 180, 90), outline=O, width=7)
    d.line([(380, 800), (460, 640)], fill=O, width=46); d.line([(380, 800), (460, 640)], fill=(110, 180, 90), width=34)
    d.ellipse([430, 590, 520, 670], fill=(110, 180, 90), outline=O, width=6)
    a = (t * 0.6) % 1
    gx, gy = 480 + a * 400, 700 - math.sin(a * math.pi) * 250
    gota(d, gx, gy, 40, T)
    d.rounded_rectangle([820, 880, 940, 1060], 16, fill=(230, 245, 255), outline=O, width=6)
    d.rectangle([830, 940, 930, 1050], fill=AZ)
    if t > 2: rotulo(d, 540, 1170, "ÁGUA RECICLADA HÁ BILHÕES DE ANOS", 40, AMARELO)


def c_corpo(d, img, t, T):
    d.ellipse([440, 470, 640, 670], fill=(252, 214, 188), outline=O, width=8)
    olhos(d, 540, 560, T, 70, 18)
    d.rounded_rectangle([420, 670, 660, 1050], 60, fill=(240, 240, 245), outline=O, width=8)
    h = 380 * 0.6 * ease(t / 2)
    d.rounded_rectangle([430, 1040 - h, 650, 1040], 50, fill=AZ)
    contador(d, 820, 760, 60, t, 2, 100, "%", AMARELO)


def g_agua(d, img, t, T):
    gota(d, 560, 760, 190, T)
    brilhos(d, 560, 700, 360, T, 8, CIANO)


CENAS = [
    dict(tipo="gancho", titulo="A ÁGUA É ESTRANHA", desenho=g_agua, fundo=((40, 110, 200), (10, 40, 100)),
         fala="A água parece a coisa mais comum do mundo, mas ela é estranhíssima! E uma das manias dela salvou a vida na Terra."),
    dict(tipo="fato", titulo="O GELO FLUTUA", desenho=c_flutua, fundo=((160, 210, 255), (90, 150, 230)),
         fala="Quase todas as substâncias ficam mais densas quando viram sólido. A água faz o contrário: quando congela, ela se expande. Por isso o gelo flutua."),
    dict(tipo="fato", titulo="ISSO SALVOU A VIDA", desenho=c_lago, fundo=((200, 230, 255), (140, 190, 240)),
         fala="E isso é crucial: no inverno, os lagos congelam por cima, e o gelo funciona como uma tampa que protege a água lá embaixo. Se o gelo afundasse, muitos lagos congelariam inteiros."),
    dict(tipo="fato", titulo="QUASE TODA SALGADA", desenho=c_salgada, fundo=((15, 30, 80), (5, 10, 35)), estrelas=True,
         fala="E de toda a água da Terra, uns noventa e sete por cento estão nos oceanos, salgada. Sobra só uns três por cento de água doce."),
    dict(tipo="fato", titulo="A DOCE ESTÁ CONGELADA", desenho=c_gelo_doce, fundo=((180, 220, 255), (120, 170, 230)),
         fala="E dessa pouca água doce, cerca de dois terços estão congelados em geleiras e nas calotas polares!"),
    dict(tipo="fato", titulo="VOCÊ É ÁGUA", desenho=c_corpo, fundo=((60, 140, 200), (20, 60, 120)),
         fala="O corpo de um adulto é feito de uns sessenta por cento de água. É ela que leva os nutrientes e controla a temperatura do corpo."),
    dict(tipo="fato", titulo="ÁGUA DE DINOSSAURO", desenho=c_dino, fundo=((140, 200, 140), (80, 140, 90)),
         fala="E o mais bizarro: a água da Terra vem sendo reciclada há bilhões de anos, evaporando, chovendo e correndo pros rios. Então as moléculas do seu copo podem já ter passado por um dinossauro!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Quantos copos por dia?",
         fala="Seja sincero: quantos copos de água você bebeu hoje? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "agua.mp4"))
