"""Gatos: miam só pra gente."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, brilhos, O

LARANJA = (245, 150, 60)


def gato(d, cx, cy, s, T, cor=LARANJA, dormindo=False, boca=False):
    d.ellipse([cx - 170 * s, cy + 40 * s, cx + 170 * s, cy + 300 * s], fill=cor, outline=O, width=7)
    cauda = [(cx + 150 * s + math.sin(T * 2 + k * 0.5) * 20 * s * k / 6, cy + 260 * s - k * 40 * s) for k in range(7)]
    d.line([(cx + 150 * s, cy + 260 * s)] + cauda, fill=O, width=int(40 * s) + 6)
    d.line([(cx + 150 * s, cy + 260 * s)] + cauda, fill=cor, width=int(40 * s))
    for sx in (-1, 1):
        d.polygon([(cx + sx * 60 * s, cy - 120 * s), (cx + sx * 150 * s, cy - 210 * s + math.sin(T * 3) * 6 * s), (cx + sx * 150 * s, cy - 60 * s)], fill=cor, outline=O)
    d.ellipse([cx - 160 * s, cy - 160 * s, cx + 160 * s, cy + 110 * s], fill=cor, outline=O, width=7)
    if dormindo:
        for sx in (-1, 1): d.arc([cx + sx * 60 * s - 30 * s, cy - 50 * s, cx + sx * 60 * s + 30 * s, cy - 10 * s], 20, 160, fill=O, width=7)
    else:
        for sx in (-1, 1):
            ex = cx + sx * 60 * s
            d.ellipse([ex - 32 * s, cy - 70 * s, ex + 32 * s, cy - 5 * s], fill=(160, 220, 90), outline=O, width=5)
            d.ellipse([ex - 8 * s, cy - 65 * s, ex + 8 * s, cy - 10 * s], fill=O)
    d.polygon([(cx - 14 * s, cy + 15 * s), (cx + 14 * s, cy + 15 * s), (cx, cy + 32 * s)], fill=(250, 130, 150))
    if boca: d.ellipse([cx - 25 * s, cy + 40 * s, cx + 25 * s, cy + 80 * s], fill=(150, 40, 60), outline=O, width=4)
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            d.line([(cx + sx * 40 * s, cy + 30 * s + k * 12 * s), (cx + sx * 200 * s, cy + 15 * s + k * 30 * s)], fill=O, width=4)


def c_miau(d, img, t, T):
    gato(d, 380, 760, 0.9, T, boca=int(T * 2) % 2 == 0)
    d.ellipse([700, 600, 900, 800], fill=(252, 214, 188), outline=O, width=7)
    olhos(d, 800, 690, T, 60, 15)
    if int(T * 2) % 2 == 0: rotulo(d, 560, 560, "MIAU!", 70, AMARELO)
    if t > 1.5: rotulo(d, 540, 1170, "É PRA VOCÊ!", 60, AMARELO)


def c_ronrona(d, img, t, T):
    gato(d, 540, 760, 1.1, T, dormindo=True)
    for k in range(4):
        r = 260 + ((T * 120 + k * 60) % 240)
        d.arc([540 - r, 900 - r, 540 + r, 900 + r], 200, 340, fill=CIANO, width=6)
    if t > 1: rotulo(d, 540, 1170, "25 A 150 Hz", 70, AMARELO)


def c_doce(d, img, t, T):
    gato(d, 360, 820, 0.8, T)
    # bolo
    d.rounded_rectangle([680, 760, 960, 960], 20, fill=(250, 220, 180), outline=O, width=6)
    d.rectangle([680, 760, 960, 810], fill=(255, 150, 180))
    d.ellipse([800, 700, 840, 760], fill=(230, 40, 60), outline=O, width=4)
    if t > 1:
        d.line([(680, 700), (960, 980)], fill=(230, 40, 40), width=14)
    if t > 1.6: rotulo(d, 540, 1170, "NÃO SENTE DOCE", 64, AMARELO)


def c_sono(d, img, t, T):
    gato(d, 540, 800, 1.0, T, cor=(130, 130, 140), dormindo=True)
    for k in range(3):
        y = 600 - ((T * 60 + k * 50) % 150)
        rotulo(d, 720 + k * 40, y, "Z", 50 + k * 10, CIANO)
    contador(d, 540, 1170, 16, t, 2, 100, " h/dia", AMARELO)


def c_orelha(d, img, t, T):
    gato(d, 540, 820, 1.1, T, cor=(240, 240, 235))
    if t > 1: rotulo(d, 540, 520, "32 MÚSCULOS", 64, AMARELO)
    if t > 1.8: rotulo(d, 540, 600, "EM CADA ORELHA", 44)


def g_gato(d, img, t, T):
    gato(d, 600, 760, 1.15, T, boca=int(T * 2) % 2 == 0)
    brilhos(d, 600, 760, 380, T, 8)


CASA = ((255, 200, 160), (220, 140, 110))
CENAS = [
    dict(tipo="gancho", titulo="O SEGREDO DO MIAU", desenho=g_gato, fundo=CASA,
         fala="Seu gato mia pra você de um jeito que ele quase nunca mia pra outro gato! E no final tem um fato que vai te fazer olhar diferente pras orelhas dele."),
    dict(tipo="fato", titulo="O MIAU É PRA GENTE", desenho=c_miau, fundo=((200, 230, 255), (150, 190, 240)),
         fala="Gatos adultos quase não miam entre si. Eles se comunicam mais com cheiros, olhares e o corpo. O miado ficou como um jeito de conversar com os humanos!"),
    dict(tipo="fato", titulo="O RONRONAR", desenho=c_ronrona, fundo=((90, 60, 120), (40, 25, 60)),
         fala="O ronronar vibra mais ou menos entre vinte e cinco e cento e cinquenta hertz. Pesquisadores estudam se essa vibração ajuda até na recuperação de ossos e músculos."),
    dict(tipo="fato", titulo="NÃO SENTE O DOCE", desenho=c_doce, fundo=((255, 230, 200), (240, 180, 150)),
         fala="E gato não sente o gosto doce! Um gene ligado a esse sabor não funciona nos felinos. Por isso eles não ligam pra bolo, só pro cheirinho de carne."),
    dict(tipo="fato", titulo="CAMPEÕES DO SONO", desenho=c_sono, fundo=((30, 30, 70), (10, 10, 30)), estrelas=True,
         fala="Eles dormem, em média, de doze a dezesseis horas por dia. São caçadores que economizam energia pra dar o bote na hora certa."),
    dict(tipo="fato", titulo="ORELHAS DE RADAR", desenho=c_orelha, fundo=((150, 210, 160), (90, 150, 110)),
         fala="E o mais bizarro: cada orelha do gato tem uns trinta e dois músculos. Elas giram de forma independente, como dois radares procurando o menor barulhinho!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Seu gato mia muito?",
         fala="Seu gato é do tipo que mia o dia inteiro? Me conta o nome dele nos comentários!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "gatos.mp4"))
