"""Peixe-barril, Parte 2 (BICHOS INSANOS #8). Importa desenhos de video_peixe_barril_p1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_peixe_barril_p1 import peixe_barril, particulas, etiqueta as _etq, VERDE, VIDRO, MAR1, MAR2, CORPO, CORPO2

ROXO1 = (40, 15, 70); ROXO2 = (10, 4, 25); TENT = (255, 140, 200); REDE = (200, 190, 160)


def etiqueta(d):
    _etq(d, "P2")


def g_anos(d, img, t, T):
    etiqueta(d)
    particulas(d, T)
    # calendário girando 1939 -> 2009 por cima de um peixe "escondido"
    peixe_barril(d, 620, 960, 1.15, T, giro=0.5 + 0.5 * math.sin(T * 1.5))
    rotulo(d, 250, 620, "1939", 64, (255, 255, 255), traduzir=False)


def c_giro(d, img, t, T):
    particulas(d, T, 16)
    g = 0.5 - 0.5 * math.cos(t * 2.2)
    peixe_barril(d, 500, 1000, 1.4, T, giro=g)
    # presa acima (silhueta) e seta mostrando o giro
    d.ellipse([760, 560, 860, 600], fill=(20, 20, 30), outline=(200, 230, 255), width=3)
    rotulo(d, 810, 650, "COMIDA", 40, (255, 255, 255))
    rotulo(d, 270, 620, "CIMA", 46, VERDE)
    rotulo(d, 900, 940, "FRENTE", 46, VERDE)
    d.arc([380, 600, 760, 980], 270, 350, fill=AMARELO, width=10)


def sifonoforo(d, x0, T, y0=470):
    # corrente de "sinos" com tentáculos venenosos pendurados
    for i in range(5):
        y = y0 + i * 50
        d.ellipse([x0 - 26, y, x0 + 26, y + 44], fill=(255, 170, 210), outline=O, width=4)
    for k in range(6):
        x = x0 - 220 + k * 90
        pts = [(x + 12 * math.sin(T * 2 + j * 0.7 + k), 720 + j * 40) for j in range(10)]
        d.line([(x0, 700), pts[0]], fill=TENT, width=4)
        d.line(pts, fill=TENT, width=5)
        for (px, py) in pts[2::3]:
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(255, 220, 120), outline=O, width=2)


def c_ladrao(d, img, t, T):
    sifonoforo(d, 600, T)
    peixe_barril(d, 430, 1120, 0.95, T, giro=0.2)
    rotulo(d, 830, 1060, "VENENO", 44, TENT)
    k = pop(min(1, max(0, t - 1.0) / 0.5))
    if k > 0.05:
        rotulo(d, 330, 820, "CAPACETE!", int(52 * k) + 1, AMARELO)
        seta(d, 330, 860, 420, 940, AMARELO, 9)


def c_rede(d, img, t, T):
    # esquerda: rede/1939 e peixe sem cúpula; direita: robô submarino filmando o peixe inteiro
    d.line([(540, 470), (540, 1240)], fill=(255, 255, 255), width=4)
    for i in range(7):
        d.line([(60 + i * 65, 560), (60 + i * 65, 900)], fill=REDE, width=4)
        d.line([(50, 560 + i * 55), (480, 560 + i * 55)], fill=REDE, width=4)
    peixe_barril(d, 280, 1060, 0.7, T, brilho=False, cupula=False)
    rotulo(d, 300, 960, "SEM CÚPULA", 38, (255, 120, 120))
    rotulo(d, 270, 1180, "1939", 60, (255, 255, 255), traduzir=False)
    # robô submarino
    x, y = 810, 650 + 10 * math.sin(T * 2)
    d.rounded_rectangle([x - 130, y - 70, x + 130, y + 70], 30, fill=(250, 200, 40), outline=O, width=6)
    d.ellipse([x - 150, y - 30, x - 90, y + 30], fill=(40, 40, 60), outline=O, width=5)
    d.polygon([(x - 150, y), (x - 330, y + 220), (x - 60, y + 260)], fill=(255, 255, 200))
    peixe_barril(d, 790, 1000, 0.55, T, brilho=False)
    rotulo(d, 800, 1180, "ROBÔ SUBMARINO", 40, CIANO)


def c_cta(d, img, t, T):
    etiqueta(d)
    particulas(d, T)
    peixe_barril(d, 600, 920, 1.2, T, giro=0.5 + 0.5 * math.sin(T * 1.5))


CENAS = [
    dict(tipo="gancho", titulo="70 ANOS!", titulo_y=400, desenho=g_anos, fundo=(MAR1, MAR2),
         fala="Por setenta anos, ninguém viu a cabeça transparente do peixe-barril!"),
    dict(tipo="fato", titulo="OLHOS GIRAM", desenho=c_giro, fundo=((12, 45, 80), MAR2),
         fala="Os olhos-tubo giram: pra cima, pra achar comida, e pra frente, pra comer."),
    dict(tipo="fato", titulo="CAPACETE", desenho=c_ladrao, fundo=(ROXO1, ROXO2),
         fala="Cientistas acham que ele rouba comida de tentáculos venenosos, e a cabeça vira capacete. Genial!"),
    dict(tipo="fato", titulo="O SEGREDO", desenho=c_rede, fundo=((15, 35, 75), MAR2),
         fala="E o segredo: as redes destruíam a cúpula. Só com robôs submarinos viram a cabeça inteira."),
    dict(tipo="cta", titulo="70 ANOS!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. E pensar que..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "peixe_barril_p2.mp4"))
