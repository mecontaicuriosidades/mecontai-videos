"""Relâmpago do Catatumbo, Parte 2 (LUGARES MORTAIS #5). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, sol, O
from video_catatumbo_p1 import etiqueta, selo, nuvem, raio, lago, palafita, flash, RAIO, RAIO2, AGUA, MORRO

NEVE = (240, 245, 255)


def g_apagou(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    lago(d, 1050, T, 0.0)
    nuvem(d, 600, 700, 0.95, cor=(55, 55, 80))
    # raio "desligado": contorno tracejado e um X
    for i in range(6):
        y = 790 + i * 45
        x = 560 + 40 * math.sin(i * 2.1)
        d.line([(x, y), (x + 20, y + 22)], fill=(120, 120, 150), width=8)
    k = pop(min(1, (t % 2.0) / 0.5)) if t < 2.0 else 1
    d.line([(470, 790 - 0), (680, 1010)], fill=(230, 60, 70), width=int(22 * k) + 1)
    d.line([(680, 790), (470, 1010)], fill=(230, 60, 70), width=int(22 * k) + 1)
    palafita(d, 860, 1060, 0.8, cor=(120, 80, 60))
    rotulo(d, 860, 1210, "EM 2010", 44, AMARELO)


def montanhas(d, base=1100):
    d.polygon([(0, base), (120, 700), (260, 860), (380, 620), (520, base)], fill=MORRO, outline=O)
    for px, py in ((120, 700), (380, 620)):
        d.polygon([(px - 40, py + 70), (px, py), (px + 40, py + 70)], fill=NEVE)


def c_porque(d, img, t, T):
    selo(d)
    montanhas(d, 1050)
    lago(d, 1050, T, 0.0)
    d.rectangle([0, 1050, 520, 1320], fill=(60, 110, 60))
    rotulo(d, 260, 1110, "ANDES", 46, (255, 255, 255))
    # vento frio descendo
    k = (T * 0.8) % 1
    seta(d, 330 + 140 * k, 720 + 150 * k, 470 + 140 * k, 860 + 150 * k, (140, 210, 255), 12)
    rotulo(d, 300, 560, "VENTO FRIO", 44, (140, 210, 255))
    # ar quente subindo do lago
    for i in range(3):
        f = (T * 0.6 + i / 3) % 1
        y = 1030 - f * 330
        x = 700 + i * 110
        d.arc([x - 30, y - 30, x + 30, y + 30], 200, 340, fill=(255, 150, 90), width=8)
    rotulo(d, 820, 1120, "AR QUENTE", 44, (255, 150, 90))
    nuvem(d, 700, 640, 0.7, brilho=flash(T, 0.45))
    if flash(T, 0.45):
        raio(d, 680, 700, 900, int(T * 2), 9)


def c_2010(d, img, t, T):
    selo(d)
    # calendário com meses JAN–ABR riscados
    meses = ["JAN", "FEV", "MAR", "ABR"]
    for i, m in enumerate(meses):
        x = 175 + i * 245
        d.rounded_rectangle([x - 100, 560, x + 100, 780], 20, fill=(250, 250, 250), outline=O, width=6)
        d.rectangle([x - 100, 560, x + 100, 610], fill=(220, 60, 70), outline=O, width=6)
        if t > 0.4 + i * 0.45:
            d.line([(x - 70, 620), (x + 70, 770)], fill=(230, 60, 70), width=10)
        rotulo(d, x, 690, m, 50, (255, 255, 255))
    rotulo(d, 540, 850, "2010", 70, AMARELO, traduzir=False)
    # lago escuro, sem raio
    lago(d, 1050, T, 0.0)
    nuvem(d, 540, 960, 0.6, cor=(50, 50, 70))
    rotulo(d, 540, 1170, "NENHUM RAIO", 54, (255, 255, 255))


def c_seca(d, img, t, T):
    selo(d)
    sol(d, 260, 640, 110, T)
    rotulo(d, 260, 820, "EL NIÑO", 50, AMARELO)
    # chão rachado
    d.rectangle([0, 980, 1080, 1320], fill=(170, 120, 70))
    for i in range(7):
        x = 80 + i * 150
        d.line([(x, 990), (x + 40, 1080), (x - 20, 1160), (x + 30, 1260)], fill=(90, 55, 30), width=6)
    rotulo(d, 270, 930, "SECA", 52, (255, 200, 120))
    # depois: os raios voltaram
    if t > 2.6:
        k = pop(min(1, (t - 2.6) / 0.5))
        nuvem(d, 760, 640, 0.75 * k, brilho=flash(T, 0.4))
        raio(d, 740, 700, 930, int(T * 2), 12)
        rotulo(d, 760, 960, "VOLTOU!", int(56 * k) + 1, RAIO)


def c_cta(d, img, t, T):
    g_apagou(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="APAGOU!", titulo_y=400, desenho=g_apagou, fundo=((30, 30, 60), (10, 10, 25)),
         fala="Esse lago que leva raio quase toda noite... um dia ficou no escuro! E o motivo é ainda mais estranho."),
    dict(tipo="fato", titulo="O SEGREDO", desenho=c_porque, fundo=((40, 50, 95), (15, 20, 45)),
         fala="Segue pra mais lugar mortal: o ar quente e úmido do lago encontra o vento frio que desce dos Andes, e vira tempestade."),
    dict(tipo="fato", titulo="EM 2010", desenho=c_2010, fundo=((40, 40, 70), (15, 15, 35)),
         fala="Mas em dois mil e dez, de janeiro a abril, os raios simplesmente pararam."),
    dict(tipo="fato", titulo="A CULPA", desenho=c_seca, fundo=((120, 80, 50), (50, 30, 20)),
         fala="O culpado provável foi o El Niño, que trouxe seca: sem umidade, não tem tempestade. Depois, os raios voltaram."),
    dict(tipo="cta", titulo="APAGOU!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 30, 90), (10, 10, 35)),
         fala="Segue pra ver o próximo Lugares Mortais amanhã. Porque esse lago..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "catatumbo_p2.mp4"))
