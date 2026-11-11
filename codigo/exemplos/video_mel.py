"""O mel praticamente nunca estraga (e o trabalho absurdo das abelhas)."""
import math, sys
import numpy as np
from motor import render, pop, ease, fnt, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, terra, seta, brilhos, O

MEL = (245, 170, 30)


def pote(d, cx, cy, s, T, nivel=1.0, rosto=True):
    d.rounded_rectangle([cx - 150 * s, cy - 170 * s, cx + 150 * s, cy + 170 * s], int(60 * s), fill=(255, 245, 220), outline=O, width=8)
    hh = 300 * s * nivel
    d.rounded_rectangle([cx - 135 * s, cy + 155 * s - hh, cx + 135 * s, cy + 155 * s], int(50 * s), fill=MEL)
    d.rounded_rectangle([cx - 165 * s, cy - 215 * s, cx + 165 * s, cy - 160 * s], int(20 * s), fill=(200, 80, 60), outline=O, width=7)
    if rosto:
        olhos(d, cx, cy + 10 * s, T, 80 * s, 20 * s); sorriso(d, cx, cy + 60 * s, 30 * s)


def abelha(d, x, y, s, T):
    asa = math.sin(T * 30) * 0.4
    for sx in (-1, 1):
        d.ellipse([x + sx * 10 * s - 30 * s, y - 70 * s - asa * 20 * s, x + sx * 10 * s + 30 * s, y - 10 * s], fill=(220, 240, 255), outline=O, width=4)
    d.ellipse([x - 60 * s, y - 40 * s, x + 60 * s, y + 40 * s], fill=AMARELO, outline=O, width=6)
    for k in (-1, 0.2):
        d.line([(x + k * 30 * s, y - 38 * s), (x + k * 30 * s, y + 38 * s)], fill=O, width=int(14 * s))
    d.ellipse([x + 40 * s, y - 30 * s, x + 90 * s, y + 20 * s], fill=O)
    d.ellipse([x + 60 * s, y - 18 * s, x + 74 * s, y - 4 * s], fill="white")


def c_tumba(d, img, t, T):
    # pirâmide + pote antigo
    d.polygon([(140, 1000), (540, 520), (940, 1000)], fill=(225, 180, 100), outline=O)
    for k in range(6): d.line([(140 + k * 67, 1000 - k * 80), (940 - k * 67, 1000 - k * 80)], fill=(180, 135, 70), width=5)
    if t > 1.0:
        s = pop((t - 1.0) / 0.5)
        pote(d, 540, 1080, 0.45 * max(s, .05), T)
    if t > 2.2: rotulo(d, 540, 460, "MILHARES DE ANOS", 54, AMARELO)


def c_agua(d, img, t, T):
    pote(d, 540, 780, 1.1, T)
    if t > 1.0:
        d.rounded_rectangle([110, 1060, 500, 1240], 30, fill=(15, 20, 50), outline=CIANO, width=6)
        rotulo(d, 305, 1110, "ÁGUA", 44, CIANO); contador(d, 305, 1190, 17, t - 1, 1.2, 64, "%")
    if t > 2.0:
        d.rounded_rectangle([580, 1060, 970, 1240], 30, fill=(15, 20, 50), outline=AMARELO, width=6)
        rotulo(d, 775, 1110, "AÇÚCAR", 44, AMARELO); contador(d, 775, 1190, 80, t - 2, 1.2, 64, "%")


def c_bacteria(d, img, t, T):
    pote(d, 540, 760, 1.0, T, rosto=False)
    rng = np.random.default_rng(4)
    for i in range(7):
        a = i / 7 * 2 * math.pi + T * 0.5
        r = 330 - ease((t - 0.5) / 2) * 60 if t > 0.5 else 330
        x, y = 540 + math.cos(a) * r, 760 + math.sin(a) * r * 0.9
        d.ellipse([x - 34, y - 22, x + 34, y + 22], fill=(120, 200, 90), outline=O, width=5)
        if t > 2: d.line([(x - 26, y - 18), (x + 26, y + 18)], fill=(230, 40, 40), width=8)
    if t > 1.5: rotulo(d, 540, 1200, "ÁCIDO + POUCA ÁGUA", 54, AMARELO)


def c_abelhas(d, img, t, T):
    for i in range(5):
        x = (T * 120 + i * 230) % 1300 - 110
        y = 620 + math.sin(T * 3 + i) * 80 + (i % 2) * 220
        abelha(d, x, y, 0.8, T + i)
    # gotinha de 1/12 colher
    if t > 1.2:
        s = pop((t - 1.2) / 0.5)
        d.ellipse([500 - 40 * s, 1080 - 40 * s, 580 + 40 * s, 1160 + 40 * s], fill=MEL, outline=O, width=6)
        rotulo(d, 540, 1230, "1/12 DE COLHER DE CHÁ", 46, AMARELO)


def c_voltas(d, img, t, T):
    terra(d, 540, 780, 220, T)
    for k in range(2):
        a = T * 2 + k * math.pi
        r = 290 + k * 50
        x, y = 540 + math.cos(a) * r, 780 + math.sin(a) * r * 0.5
        d.arc([540 - r, 780 - r * 0.5, 540 + r, 780 + r * 0.5], 0, 360, fill=(255, 230, 120), width=4)
        abelha(d, x, y, 0.45, T)
    if t > 1.5: rotulo(d, 540, 1170, "2 VOLTAS NA TERRA", 60, AMARELO)
    if t > 2.5: rotulo(d, 540, 1240, "PRA MEIO QUILO DE MEL", 40)


def g_mel(d, img, t, T):
    pote(d, 600, 820, 1.2, T)
    brilhos(d, 600, 820, 330, T, 10)


def c_cristal(d, img, t, T):
    pote(d, 540, 800, 1.1, T)
    rng = np.random.default_rng(8)
    k = ease(t / 2)
    for i in range(int(140 * k)):
        x, y = rng.uniform(400, 680), rng.uniform(640, 960)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 245, 215))
    if t > 2.5: rotulo(d, 540, 1170, "SÓ CRISTALIZOU!", 60, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="A COMIDA QUE NÃO ESTRAGA", desenho=g_mel, fundo=((60, 35, 15), (25, 12, 5)),
         fala="Existe uma comida que praticamente nunca estraga. Já encontraram potes dela com milhares de anos! E ela tá aí na sua cozinha."),
    dict(tipo="fato", titulo="É O MEL!", desenho=c_tumba, fundo=((255, 200, 120), (230, 140, 70)),
         fala="É o mel! Arqueólogos acharam potes de mel em tumbas do antigo Egito, com milhares de anos, e o mel ainda estava bem conservado."),
    dict(tipo="fato", titulo="QUASE SEM ÁGUA", desenho=c_agua, fundo=((90, 50, 20), (40, 20, 10)),
         fala="O segredo é que o mel tem pouquíssima água, uns dezessete por cento, e muito açúcar. Sem água, quase nenhum micróbio consegue crescer."),
    dict(tipo="fato", titulo="UMA ARMADURA NATURAL", desenho=c_bacteria, fundo=((40, 90, 60), (15, 40, 25)),
         fala="Além disso, ele é ácido, e as abelhas colocam uma enzima que produz um pouquinho de água oxigenada. É uma armadura completa contra bactérias!"),
    dict(tipo="fato", titulo="TRABALHO DE UMA VIDA", desenho=c_abelhas, fundo=((150, 210, 255), (100, 190, 120)),
         fala="Agora olha o esforço: uma abelha operária produz, na vida inteira, só um doze avos de uma colher de chá de mel."),
    dict(tipo="fato", titulo="UMA VIAGEM ABSURDA", desenho=c_voltas, fundo=((20, 20, 60), (5, 5, 25)), estrelas=True,
         fala="E o mais bizarro: pra fazer meio quilo de mel, as abelhas de uma colmeia voam, somando tudo, uma distância de umas duas voltas ao redor da Terra!"),
    dict(tipo="fato", titulo="DICA DA MAIA", desenho=c_cristal, fundo=((255, 190, 90), (220, 120, 50)),
         fala="Ah, e se o seu mel ficar durinho e esbranquiçado, não jogue fora! Ele só cristalizou. Um banho-maria leve resolve."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Você joga mel cristalizado fora?",
         fala="Confessa: você já jogou mel cristalizado fora? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e amanhã tem mais curiosidade. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "mel.mp4"))
