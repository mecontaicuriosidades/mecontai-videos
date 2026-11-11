"""Tubarões: mais velhos que as árvores."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, seta, brilhos, O

CINZA = (120, 150, 175)


def tubarao(d, cx, cy, s, T, cor=CINZA, boca=False):
    sw = math.sin(T * 4) * 10 * s
    corpo = [(cx - 260 * s, cy + sw * 0.3), (cx - 120 * s, cy - 80 * s), (cx + 160 * s, cy - 70 * s),
             (cx + 280 * s, cy), (cx + 160 * s, cy + 60 * s), (cx - 120 * s, cy + 60 * s)]
    d.polygon(corpo, fill=cor, outline=O)
    d.line(corpo + [corpo[0]], fill=O, width=int(7 * s) + 1)
    d.polygon([(cx - 240 * s, cy), (cx - 360 * s, cy - 110 * s + sw), (cx - 330 * s, cy + sw * 0.5), (cx - 360 * s, cy + 100 * s + sw)], fill=cor, outline=O)
    d.polygon([(cx - 20 * s, cy - 75 * s), (cx + 40 * s, cy - 190 * s), (cx + 90 * s, cy - 72 * s)], fill=cor, outline=O)
    d.polygon([(cx - 120 * s, cy + 30 * s), (cx + 120 * s, cy + 30 * s), (cx + 160 * s, cy + 58 * s), (cx - 120 * s, cy + 58 * s)], fill=(235, 240, 245))
    d.ellipse([cx + 150 * s, cy - 35 * s, cx + 185 * s, cy], fill=O)
    for k in range(3): d.arc([cx + 40 * s + k * 25 * s, cy - 40 * s, cx + 70 * s + k * 25 * s, cy + 20 * s], 100, 260, fill=O, width=int(5 * s) + 1)
    if boca:
        for k in range(6):
            x = cx + 150 * s + k * 18 * s
            d.polygon([(x, cy + 20 * s), (x + 9 * s, cy + 40 * s), (x + 18 * s, cy + 20 * s)], fill="white", outline=O)


def c_idade(d, img, t, T):
    tubarao(d, 560, 640, 1.1, T)
    # linha do tempo
    d.line([(120, 1080), (960, 1080)], fill="white", width=8)
    for x, txt, cor, ti in ((200, "TUBARÃO\n450 mi", AMARELO, 0.8), (520, "ÁRVORES\n~380 mi", (120, 220, 120), 1.6), (880, "HOJE", CIANO, 2.3)):
        if t > ti:
            d.ellipse([x - 18, 1062, x + 18, 1098], fill=cor, outline=O, width=4)
            for i, l in enumerate(txt.split("\n")): rotulo(d, x, 1140 + i * 50, l, 38, cor)


def c_cartilagem(d, img, t, T):
    tubarao(d, 540, 700, 1.2, T, cor=(160, 185, 205))
    # "esqueleto" flexível
    for k in range(9):
        x = 300 + k * 55
        y = 700 + math.sin(T * 4 + k * 0.6) * 18
        d.rounded_rectangle([x - 18, y - 28, x + 18, y + 28], 10, fill=(170, 220, 255), outline=O, width=4)
    if t > 1.5: rotulo(d, 540, 1100, "SEM UM OSSO SEQUER", 56, AMARELO)


def c_dentes(d, img, t, T):
    tubarao(d, 480, 680, 1.4, T, boca=True)
    rng = np.random.default_rng(2)
    for i in range(int(18 * ease(t / 2))):
        x, y = rng.uniform(160, 940), 900 + rng.uniform(0, 160) + (T * 60 + i * 30) % 120
        d.polygon([(x, y), (x + 22, y + 40), (x - 22, y + 40)], fill="white", outline=O)
    if t > 1: contador(d, 540, 1170, 30000, t - 1, 2, 90, "", AMARELO)
    if t > 1: rotulo(d, 540, 1245, "DENTES NA VIDA (ATÉ)", 40)


def c_eletrico(d, img, t, T):
    tubarao(d, 380, 700, 0.9, T)
    # peixinho escondido na areia com "sinal elétrico"
    d.rectangle([0, 1000, 1080, 1250], fill=(225, 200, 140))
    fx = 800
    d.ellipse([fx - 60, 960, fx + 60, 1010], fill=(255, 170, 60), outline=O, width=5)
    for k in range(4):
        r = 60 + ((T * 90 + k * 40) % 160)
        d.arc([fx - r, 985 - r, fx + r, 985 + r], 200, 340, fill=AMARELO, width=6)
    if t > 1.5: rotulo(d, 540, 1180, "SENTE ELETRICIDADE!", 56, AMARELO)


def c_nadar(d, img, t, T):
    x = 100 + (t * 180) % 900
    tubarao(d, x, 700, 0.9, T)
    for k in range(6):
        bx = x - 200 - k * 60
        d.line([(bx, 680 + k * 6), (bx - 40, 680 + k * 6)], fill=(200, 235, 255), width=6)
    if t > 1.2: rotulo(d, 540, 1100, "ÁGUA ENTRA PELA BOCA", 54, CIANO)
    if t > 2.2: rotulo(d, 540, 1180, "PARAR = SEM AR", 54, (255, 120, 120))


def c_groenlandia(d, img, t, T):
    for k in range(6):  # gelo
        d.polygon([(k * 200 - 40, 520), (k * 200 + 60, 440), (k * 200 + 160, 520)], fill=(230, 245, 255), outline=O)
    tubarao(d, 540, 820, 1.25, T * 0.4, cor=(95, 105, 115))
    contador(d, 540, 1150, 400, t, 2.5, 110, " ANOS", AMARELO)


def g_tub(d, img, t, T):
    tubarao(d, 560, 760, 1.25, T, boca=True)
    brilhos(d, 560, 760, 420, T, 8, CIANO)


MAR = ((30, 110, 190), (8, 35, 90))
CENAS = [
    dict(tipo="gancho", titulo="MAIS VELHOS QUE AS ÁRVORES", desenho=g_tub, fundo=MAR,
         fala="Os tubarões já existiam antes das árvores! E o último fato sobre eles parece mentira, mas é ciência."),
    dict(tipo="fato", titulo="450 MILHÕES DE ANOS", desenho=c_idade, fundo=MAR,
         fala="Os primeiros tubarões surgiram há uns quatrocentos e cinquenta milhões de anos. As primeiras árvores só apareceram dezenas de milhões de anos depois."),
    dict(tipo="fato", titulo="NÃO TÊM OSSOS", desenho=c_cartilagem, fundo=((20, 80, 150), (5, 25, 70)),
         fala="E o esqueleto deles não tem nenhum osso! É todo feito de cartilagem, o mesmo material da ponta do seu nariz. Isso deixa o tubarão leve e flexível."),
    dict(tipo="fato", titulo="DENTES INFINITOS", desenho=c_dentes, fundo=((40, 90, 160), (10, 30, 80)),
         fala="Os dentes ficam em fileiras, e quando um cai, outro já vem atrás pra ocupar o lugar. Alguns tubarões trocam dezenas de milhares de dentes ao longo da vida."),
    dict(tipo="fato", titulo="UM SEXTO SENTIDO", desenho=c_eletrico, fundo=((30, 120, 170), (10, 50, 90)),
         fala="Eles têm um sentido que a gente não tem: pequenos poros no focinho que captam a eletricidade dos músculos de outros animais. Dá pra achar um peixe escondido na areia!"),
    dict(tipo="fato", titulo="ALGUNS NÃO PODEM PARAR", desenho=c_nadar, fundo=MAR,
         fala="Alguns tubarões, como o tubarão-branco, precisam nadar quase o tempo todo, porque é o movimento que faz a água passar pelas brânquias."),
    dict(tipo="fato", titulo="O VERTEBRADO MAIS LONGEVO", desenho=c_groenlandia, fundo=((60, 90, 120), (15, 25, 45)),
         fala="E o mais bizarro: o tubarão-da-Groenlândia pode viver uns quatrocentos anos. Tem tubarão nadando hoje que já era vivo quando o Brasil ainda era colônia de Portugal!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Medo ou fascínio?",
         fala="E você, tubarão te dá medo ou fascínio? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "tubarao.mp4"))
