"""Vênus: um dia mais longo que um ano, gira ao contrário e é um inferno."""
import math, sys
from motor import render, pop, ease, fnt, AMARELO, CIANO
from desenhos import rotulo, planeta, sol, terra, termometro, seta, contador, O

VENUS = (235, 190, 110); VENUS2 = (210, 150, 80)


def c_vizinha(d, img, t, T):
    sol(d, 160, 760, 90, T)
    planeta(d, 520, 760, 85, VENUS, VENUS2, T)
    terra(d, 860, 760, 90, T)
    if t > 1.0:
        rotulo(d, 520, 900, "VÊNUS", 46, AMARELO); rotulo(d, 860, 900, "TERRA", 46, CIANO)
    if t > 2.0: rotulo(d, 690, 1100, "QUASE DO MESMO TAMANHO", 50)


def c_dia_ano(d, img, t, T):
    planeta(d, 540, 760, 170, VENUS, VENUS2, T * 0.05)
    # órbita girando rápido x rotação lenta
    a = T * 1.2
    d.arc([140, 360, 940, 1160], 0, 360, fill=(255, 255, 255), width=4)
    x, y = 540 + math.cos(a) * 400, 760 + math.sin(a) * 400
    d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=AMARELO, outline=O, width=4)
    if t > 1.0:
        d.rounded_rectangle([90, 1060, 520, 1240], 30, fill=(15, 20, 50), outline=AMARELO, width=6)
        rotulo(d, 305, 1110, "1 DIA", 44, AMARELO); contador(d, 305, 1185, 243, t - 1, 1.5, 54, " DIAS")
    if t > 2.2:
        d.rounded_rectangle([560, 1060, 990, 1240], 30, fill=(15, 20, 50), outline=CIANO, width=6)
        rotulo(d, 775, 1110, "1 ANO", 44, CIANO); contador(d, 775, 1185, 225, t - 2.2, 1.5, 54, " DIAS")


def c_contrario(d, img, t, T):
    # horizonte de Vênus, sol nascendo a oeste
    d.rectangle([0, 1000, 1080, 1250], fill=(170, 110, 60))
    k = ease(t / 4)
    sol(d, 200 + 0 * k, 1000 - 300 * k, 90, T, rosto=True)
    rotulo(d, 200, 1100, "OESTE", 50, AMARELO)
    rotulo(d, 880, 1100, "LESTE", 50)
    if t > 1.5: seta(d, 880, 720, 500, 600, AMARELO)


def c_quente(d, img, t, T):
    termometro(d, 300, 1130, ease(t / 2.5), h=560)
    contador(d, 700, 700, 465, t, 2.5, 110, "°C", (255, 110, 60))
    if t > 2.5: rotulo(d, 700, 860, "DERRETE CHUMBO!", 50, AMARELO)
    if t > 3.5: rotulo(d, 700, 1000, "MAIS QUENTE QUE MERCÚRIO", 34)


def c_estufa(d, img, t, T):
    planeta(d, 540, 800, 220, VENUS, VENUS2, T)
    # nuvens grossas e raios presos
    for i in range(14):
        a = i / 14 * 2 * math.pi + T * 0.2
        x, y = 540 + math.cos(a) * 290, 800 + math.sin(a) * 290
        d.ellipse([x - 60, y - 40, x + 60, y + 40], fill=(240, 220, 150), outline=O, width=4)
    for i in range(3):
        b = (T * 1.5 + i * 0.33) % 1
        ang = 0.6 + i * 0.9
        r1 = 230 + b * 50
        d.line([(540 + math.cos(ang) * 230, 800 + math.sin(ang) * 230),
                (540 + math.cos(ang) * r1, 800 + math.sin(ang) * r1)], fill=(255, 80, 40), width=12)
    if t > 1.5: rotulo(d, 540, 1200, "CO₂ PRENDE O CALOR".replace("₂", "2"), 50, AMARELO)


def c_pressao(d, img, t, T):
    # mergulhador a 900 m
    for k in range(10):
        y = 460 + k * 80
        d.rectangle([0, y, 1080, y + 80], fill=(20, 70 - k * 5, 150 - k * 10))
    y = 520 + ease(t / 3) * 500
    d.ellipse([500, y - 50, 580, y + 30], fill=(255, 200, 60), outline=O, width=5)
    d.rounded_rectangle([490, y + 20, 590, y + 140], 30, fill=(240, 120, 40), outline=O, width=5)
    contador(d, 820, 1080, 900, t, 3, 80, " m")
    if t > 2.5: rotulo(d, 300, 700, "90x A PRESSÃO", 56, AMARELO)


def g_venus(d, img, t, T):
    planeta(d, 560, 820, 260, VENUS, VENUS2, T)
    k = (t * 0.25) % 1
    sol(d, 140 + 0 * k, 1150 - 300 * k, 70, T)
    rotulo(d, 860, 560, "?", 140, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="O PLANETA MAIS ESTRANHO", desenho=g_venus, fundo=((25, 15, 60), (8, 5, 28)),
         fala="Existe um planeta onde um dia dura mais que um ano inteiro, e o Sol nasce do lado errado. E ele é o nosso vizinho!"),
    dict(tipo="fato", titulo="CONHEÇA VÊNUS", desenho=c_vizinha, fundo=((20, 15, 50), (5, 5, 25)), estrelas=True,
         fala="Esse é Vênus, o segundo planeta a partir do Sol. Ele é quase do mesmo tamanho da Terra, por isso é chamado de planeta irmão."),
    dict(tipo="fato", titulo="UM DIA MAIOR QUE UM ANO", desenho=c_dia_ano, fundo=((30, 20, 70), (8, 5, 30)), estrelas=True,
         fala="Mas ele gira muito devagar: leva duzentos e quarenta e três dias terrestres pra dar uma volta em si mesmo. E só duzentos e vinte e cinco pra dar a volta no Sol. Ou seja, o dia é mais longo que o ano!"),
    dict(tipo="fato", titulo="GIRA AO CONTRÁRIO", desenho=c_contrario, fundo=((240, 170, 90), (190, 110, 60)),
         fala="E ele gira ao contrário da maioria dos planetas. Lá, o Sol nasce no oeste e se põe no leste."),
    dict(tipo="fato", titulo="UM FORNO DE 465°C", desenho=c_quente, fundo=((120, 30, 20), (40, 10, 10)),
         fala="Vênus é o planeta mais quente do Sistema Solar, com uns quatrocentos e sessenta e cinco graus. Quente o bastante pra derreter chumbo, e mais quente até que Mercúrio, que fica mais perto do Sol."),
    dict(tipo="fato", titulo="EFEITO ESTUFA EXTREMO", desenho=c_estufa, fundo=((60, 30, 20), (20, 10, 10)), estrelas=True,
         fala="O motivo é a atmosfera, cheia de gás carbônico e nuvens de ácido. Ela prende o calor do Sol e funciona como um efeito estufa fora de controle."),
    dict(tipo="fato", titulo="ESMAGA QUALQUER UM", desenho=c_pressao, fundo=((20, 70, 150), (5, 15, 50)),
         fala="E o mais bizarro: a pressão lá é umas noventa vezes a da Terra. É como estar a novecentos metros de profundidade no oceano. As sondas que pousaram lá funcionaram, no máximo, umas duas horas antes de serem destruídas."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Você visitaria Vênus?",
         fala="E aí, você teria coragem de visitar Vênus? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e amanhã tem mais. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "venus.mp4"))
