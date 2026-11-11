"""A Lua está fugindo da Terra."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, terra, seta, brilhos, planeta, O

LUA = (215, 215, 225)


def lua(d, cx, cy, r, T, rosto=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LUA, outline=O, width=7)
    rng = np.random.default_rng(6)
    for i in range(7):
        a, rr = rng.uniform(0, 6.28), rng.uniform(0.1, 0.6)
        x, y, s = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr, r * rng.uniform(0.08, 0.18)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(180, 180, 195), outline=(140, 140, 155), width=3)
    if rosto:
        olhos(d, cx, cy - r * 0.1, T, r * 0.7, r * 0.13); sorriso(d, cx, cy + r * 0.3, r * 0.25)


def c_afasta(d, img, t, T):
    terra(d, 240, 760, 150, T)
    x = 700 + ease(t / 3) * 180
    lua(d, x, 760, 70, T)
    seta(d, 820, 900, 980, 900, AMARELO, 12)
    if t > 1: rotulo(d, 600, 1100, "+3,8 cm POR ANO", 70, AMARELO)


def c_unha(d, img, t, T):
    # dedo com unha crescendo
    d.rounded_rectangle([420, 520, 660, 1100], 110, fill=(252, 214, 188), outline=O, width=8)
    h = 120 + ease(t / 3) * 60
    d.rounded_rectangle([450, 520, 630, 520 + h], 50, fill=(255, 235, 235), outline=O, width=6)
    if t > 1.2: rotulo(d, 540, 1170, "MESMA VELOCIDADE DA UNHA", 46, AMARELO)


def c_face(d, img, t, T):
    terra(d, 540, 780, 150, T)
    a = T * 0.8
    x, y = 540 + math.cos(a) * 340, 780 + math.sin(a) * 300
    lua(d, x, y, 70, T, rosto=False)
    # "rosto" sempre virado pra Terra
    ex, ey = x - math.cos(a) * 25, y - math.sin(a) * 25
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=O)
    if t > 1.2: rotulo(d, 540, 1180, "SEMPRE A MESMA FACE", 58, AMARELO)


def c_pegadas(d, img, t, T):
    d.rectangle([0, 900, 1080, 1250], fill=(170, 170, 180))
    for k in range(int(8 * ease(t / 2.5))):
        x, y = 160 + k * 105, 1020 + (k % 2) * 60
        d.rounded_rectangle([x - 26, y - 50, x + 26, y + 50], 26, fill=(120, 120, 135))
        for j in range(4): d.line([(x - 20, y - 40 + j * 25), (x + 20, y - 40 + j * 25)], fill=(95, 95, 110), width=5)
    terra(d, 850, 600, 90, T)
    if t > 2: rotulo(d, 420, 700, "SEM VENTO,\nSEM CHUVA".split("\n")[0], 50, AMARELO)
    if t > 2.3: rotulo(d, 420, 770, "SEM CHUVA", 50, AMARELO)


def c_colisao(d, img, t, T):
    k = ease(t / 2)
    terra(d, 420, 780, 180, T, rosto=False)
    x = 1000 - k * 440
    planeta(d, x, 640, 110, (200, 110, 70), None, T, rosto=False)
    if t > 2:
        brilhos(d, 560, 700, 120 + (t - 2) * 120, T, 12, (255, 160, 60))
        rotulo(d, 540, 1150, "THEIA + TERRA = LUA", 60, AMARELO)


def c_dia(d, img, t, T):
    # relógio com 24h e "antigamente" menos
    d.ellipse([340, 520, 740, 920], fill="white", outline=O, width=9)
    a = T * 2
    d.line([(540, 720), (540 + math.cos(a) * 150, 720 + math.sin(a) * 150)], fill=O, width=10)
    d.line([(540, 720), (540 + math.cos(a / 12) * 100, 720 + math.sin(a / 12) * 100)], fill=(225, 50, 60), width=12)
    if t > 1: rotulo(d, 540, 1040, "DINOSSAUROS: DIA MAIS CURTO", 46, AMARELO)
    if t > 2: rotulo(d, 540, 1120, "~23,5 HORAS", 70, CIANO)


def g_lua(d, img, t, T):
    lua(d, 620, 740, 230, T)
    rotulo(d, 860, 520, "TCHAU!", 60, AMARELO)


ESP = ((10, 10, 40), (3, 3, 15))
CENAS = [
    dict(tipo="gancho", titulo="A LUA ESTÁ FUGINDO", desenho=g_lua, fundo=ESP, estrelas=True,
         fala="A Lua está indo embora! Todo ano ela se afasta um pouquinho da Terra. E isso já mudou até a duração do seu dia."),
    dict(tipo="fato", titulo="3,8 CM POR ANO", desenho=c_afasta, fundo=ESP, estrelas=True,
         fala="Graças aos espelhos que os astronautas deixaram lá, cientistas medem com laser que a Lua se afasta uns três vírgula oito centímetros por ano."),
    dict(tipo="fato", titulo="NA VELOCIDADE DA UNHA", desenho=c_unha, fundo=((60, 50, 110), (25, 20, 60)),
         fala="É mais ou menos a velocidade com que a sua unha cresce. Devagar, mas sem parar há bilhões de anos."),
    dict(tipo="fato", titulo="SEMPRE A MESMA FACE", desenho=c_face, fundo=ESP, estrelas=True,
         fala="E a gente sempre vê o mesmo lado da Lua. Ela gira em volta de si mesma no mesmo tempo em que dá a volta na Terra, então sempre mostra a mesma face."),
    dict(tipo="fato", titulo="PEGADAS ETERNAS", desenho=c_pegadas, fundo=ESP, estrelas=True,
         fala="Como lá não tem vento nem chuva, as pegadas dos astronautas da Apollo podem durar milhões de anos do jeitinho que ficaram."),
    dict(tipo="fato", titulo="NASCEU DE UMA BATIDA", desenho=c_colisao, fundo=ESP, estrelas=True,
         fala="A explicação mais aceita é que a Lua nasceu de uma batida gigante: um planeta do tamanho de Marte, chamado Theia, se chocou com a Terra jovem, e os destroços formaram a Lua."),
    dict(tipo="fato", titulo="O DIA JÁ FOI MENOR", desenho=c_dia, fundo=((80, 40, 20), (30, 15, 8)),
         fala="E o mais bizarro: a Lua freia a rotação da Terra pelas marés. Na época dos dinossauros, um dia durava mais ou menos vinte e três horas e meia!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Você iria pra Lua?",
         fala="Se tivesse uma passagem de graça, você iria pra Lua? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lua.mp4"))
