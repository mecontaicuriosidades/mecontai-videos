"""Por que o céu é azul e o pôr do sol é laranja (e em Marte é ao contrário)."""
import math, sys
import numpy as np
from motor import render, pop, ease, fnt, AMARELO, CIANO
from desenhos import sol, terra, rotulo, seta, planeta, O

CORES = [(255, 60, 60), (255, 150, 40), (255, 230, 60), (80, 210, 90), (60, 140, 255), (150, 80, 230)]


def c_luz_branca(d, img, t, T):
    sol(d, 230, 620, 120, T)
    # feixe branco que se abre em arco-íris
    for i, c in enumerate(CORES):
        if t > 1.2 + i * 0.15:
            s = ease((t - 1.2 - i * 0.15) / 0.6)
            y1 = 520 + i * 45
            d.line([(560, 620), (560 + 420 * s, y1 + (y1 - 620) * 0.6 * s)], fill=c, width=26)
    d.line([(360, 620), (560, 620)], fill="white", width=30)
    d.polygon([(560, 540), (700, 760), (420, 760)], fill=(200, 230, 255), outline=O)
    if t > 2.5: rotulo(d, 540, 1150, "LUZ BRANCA = TODAS AS CORES", 50)


def c_espalha(d, img, t, T):
    # moléculas de ar batendo na luz: azul se espalha pra todo lado
    rng = np.random.default_rng(3)
    for i in range(22):
        x, y = rng.uniform(100, 980), rng.uniform(470, 1050)
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(230, 240, 255), outline=O, width=4)
        if t > 1 and i % 2 == 0:
            for k in range(6):
                a = k * math.pi / 3 + T * 2
                L = 30 + 25 * ((T * 2 + i) % 1)
                d.line([(x + math.cos(a) * 22, y + math.sin(a) * 22), (x + math.cos(a) * L, y + math.sin(a) * L)],
                       fill=(70, 150, 255), width=6)
    # raio vermelho passa reto
    xr = (t * 400) % 1100
    d.line([(xr - 200, 760), (xr, 760)], fill=(255, 70, 60), width=18)
    rotulo(d, 540, 1150, "O AZUL QUICA PRA TODO LADO", 50)


def c_violeta(d, img, t, T):
    # olho humano mais sensível ao azul
    d.ellipse([290, 560, 790, 860], fill="white", outline=O, width=9)
    d.ellipse([440, 610, 640, 810], fill=(60, 140, 255), outline=O, width=6)
    d.ellipse([500, 670, 580, 750], fill=O)
    d.ellipse([515, 680, 540, 705], fill="white")
    if t > 1.0:
        s = pop((t - 1.0) / 0.4)
        d.rounded_rectangle([170, 960, 500, 1060], 30, fill=(150, 80, 230))
        rotulo(d, 335, 1010, "VIOLETA", int(50 * max(s, .1)))
        d.rounded_rectangle([580, 960, 910, 1060], 30, fill=(60, 140, 255))
        rotulo(d, 745, 1010, "AZUL!", int(50 * max(s, .1)))


def c_por_do_sol(d, img, t, T):
    k = ease(t / 4)
    terra(d, 540, 1600, 760, T, rosto=False)
    sy = 560 + k * 380
    sol(d, 540, sy, 110, T, cor=(255, int(200 - 90 * k), 40))
    # caminho longo pela atmosfera
    d.arc([-200, 900, 1280, 2300], 200, 340, fill=(255, 255, 255), width=6)
    if t > 1.5: rotulo(d, 540, 1210, "CAMINHO MAIS LONGO", 52, AMARELO)


def c_marte(d, img, t, T):
    planeta(d, 540, 1650, 800, (200, 90, 50), (170, 70, 40), T, rosto=False)
    sol(d, 540, 760, 70, T, cor=(200, 230, 255), rosto=False)
    r = 230 + 15 * math.sin(T * 2)
    d.ellipse([540 - r, 760 - r, 540 + r, 760 + r], outline=(90, 160, 255), width=26)
    if t > 1.5: rotulo(d, 540, 1150, "PÔR DO SOL AZUL EM MARTE!", 52, CIANO)


CENAS = [
    dict(tipo="gancho", titulo="POR QUE O CÉU É AZUL?",
         fala="Você já parou pra pensar por que o céu é azul, e não roxo ou verde? E no final eu te conto onde o pôr do sol é azul!"),
    dict(tipo="fato", titulo="A LUZ DO SOL É BRANCA", desenho=c_luz_branca, fundo=((20, 30, 70), (10, 15, 40)), estrelas=True,
         fala="Primeiro: a luz do Sol parece branca, mas ela é uma mistura de todas as cores do arco-íris, do vermelho até o violeta."),
    dict(tipo="fato", titulo="O AR ESPALHA O AZUL", desenho=c_espalha, fundo=((90, 170, 255), (40, 100, 210)),
         fala="Quando essa luz entra na atmosfera, ela bate nas moléculas de ar. As cores de onda curta, como o azul, se espalham muito mais pra todos os lados. Por isso o azul chega de todas as direções do céu."),
    dict(tipo="fato", titulo="E POR QUE NÃO VIOLETA?", desenho=c_violeta, fundo=((40, 60, 140), (15, 25, 70)),
         fala="Mas o violeta se espalha ainda mais! Só que a luz do Sol tem menos violeta, e os nossos olhos são bem mais sensíveis ao azul. Resultado: a gente vê o céu azul."),
    dict(tipo="fato", titulo="E O PÔR DO SOL LARANJA?", desenho=c_por_do_sol, fundo=((255, 140, 60), (120, 40, 90)),
         fala="No fim da tarde, a luz do Sol atravessa muito mais atmosfera até chegar em você. No caminho, o azul vai se espalhando e ficando pra trás, e sobram o laranja e o vermelho."),
    dict(tipo="fato", titulo="EM MARTE É AO CONTRÁRIO", desenho=c_marte, fundo=((200, 140, 100), (90, 50, 40)),
         fala="E o mais bizarro: em Marte é o contrário! O céu de dia é meio alaranjado, por causa da poeira, e o pôr do sol fica azul. A sonda da NASA já fotografou isso."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Você já sabia disso?",
         fala="E aí, você já sabia por que o céu é azul? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e amanhã tem mais curiosidade. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "ceu.mp4"))
