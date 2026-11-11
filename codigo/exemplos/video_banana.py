"""A banana é radioativa (e é uma baga, e a bananeira é uma erva)."""
import math, sys
import numpy as np
from motor import render, pop, ease, fnt, AMARELO, CIANO
from desenhos import rotulo, atomo, brilhos, olhos, sorriso, contador, O


def banana(d, cx, cy, s, T, rosto=True, ang=0):
    pts_out, pts_in = [], []
    for i in range(31):
        a = math.pi * (0.15 + 0.7 * i / 30)
        pts_out.append((cx + math.cos(a + ang) * 260 * s, cy + math.sin(a + ang) * 200 * s - 120 * s))
        pts_in.append((cx + math.cos(a + ang) * 200 * s, cy + math.sin(a + ang) * 130 * s - 120 * s))
    poly = pts_out + pts_in[::-1]
    d.polygon(poly, fill=(255, 220, 50))
    d.line(poly + [poly[0]], fill=O, width=int(8 * s) + 2)
    tip = pts_out[0]
    d.rectangle([tip[0] - 14 * s, tip[1] - 20 * s, tip[0] + 14 * s, tip[1] + 6 * s], fill=(110, 80, 30))
    if rosto:
        mx, my = pts_out[15]
        olhos(d, mx, my - 70 * s, T, esp=70 * s, r=16 * s)
        sorriso(d, mx, my - 35 * s, 22 * s)


def c_potassio(d, img, t, T):
    banana(d, 540, 900, 1.5, T)
    if t > 1.0:
        s = pop((t - 1.0) / 0.4)
        d.rounded_rectangle([390, 1060, 690, 1200], 24, fill=(255, 255, 255), outline=O, width=7)
        rotulo(d, 540, 1105, "K", int(70 * max(s, .1)), (130, 60, 200))
        rotulo(d, 540, 1170, "POTÁSSIO", 32)


def c_radioativo(d, img, t, T):
    banana(d, 540, 880, 1.3, T)
    for i, (x, y) in enumerate([(260, 620), (820, 640), (300, 1060), (800, 1080)]):
        if t > 0.6 + i * 0.3: atomo(d, x, y, 80, T + i)
    if t > 2.0: rotulo(d, 540, 1220, "POTÁSSIO-40", 60, (120, 255, 120))


def c_dose(d, img, t, T):
    # 1 raio-X = ~200 bananas
    d.rounded_rectangle([110, 520, 470, 900], 30, fill=(20, 30, 50), outline=CIANO, width=8)
    for k in range(5):  # costelas
        d.arc([180, 580 + k * 50, 400, 680 + k * 50], 200, 340, fill=(220, 230, 255), width=10)
    rotulo(d, 290, 960, "1 RAIO-X", 52)
    rotulo(d, 540, 720, "=", 120, AMARELO)
    rng = np.random.default_rng(1)
    for i in range(int(40 * ease(t / 2.5))):
        x, y = 640 + (i % 8) * 46, 520 + (i // 8) * 80
        banana(d, x + 40, y + 70, 0.18, T, rosto=False)
    if t > 1: contador(d, 790, 960, 200, t - 1, 1.5, 70, " BANANAS")


def c_porto(d, img, t, T):
    # caminhão passando por detector que apita
    x = -300 + t * 260
    d.rectangle([0, 1000, 1080, 1030], fill=(80, 80, 90))
    d.rounded_rectangle([x, 760, x + 420, 990], 16, fill=(240, 240, 245), outline=O, width=7)
    for k in range(4): banana(d, x + 70 + k * 95, 950, 0.25, T, rosto=False)
    d.rounded_rectangle([x + 420, 820, x + 560, 990], 20, fill=(230, 70, 60), outline=O, width=7)
    for wx in (x + 80, x + 330, x + 490):
        d.ellipse([wx - 40, 960, wx + 40, 1040], fill=O)
    d.rectangle([700, 640, 740, 1000], fill=(160, 160, 170), outline=O, width=5)
    d.rectangle([980, 640, 1020, 1000], fill=(160, 160, 170), outline=O, width=5)
    d.rectangle([700, 620, 1020, 660], fill=(160, 160, 170), outline=O, width=5)
    if x + 560 > 720:
        alerta = int(T * 4) % 2 == 0
        d.ellipse([830, 550, 890, 610], fill=(255, 50, 50) if alerta else (120, 30, 30), outline=O, width=5)
        if alerta: rotulo(d, 540, 1170, "BIP! BIP! BIP!", 64, AMARELO)


def c_corpo(d, img, t, T):
    # boneco simples brilhando
    d.ellipse([440, 500, 640, 700], fill=(252, 214, 188), outline=O, width=8)
    olhos(d, 540, 590, T, 70, 18); sorriso(d, 540, 640, 30)
    d.rounded_rectangle([420, 700, 660, 1020], 60, fill=(35, 210, 225), outline=O, width=8)
    for sx in (-1, 1):
        d.line([(540 + sx * 110, 740), (540 + sx * 220, 900)], fill=O, width=40)
        d.line([(540 + sx * 70, 1010), (540 + sx * 90, 1180)], fill=O, width=44)
    if t > 1.0: brilhos(d, 540, 820, 330, T, 10, (120, 255, 120))


def c_baga(d, img, t, T):
    banana(d, 330, 880, 0.9, T)
    # morango
    mx, my = 790, 820
    d.polygon([(mx - 110, my - 60), (mx + 110, my - 60), (mx, my + 150)], fill=(235, 50, 70))
    d.ellipse([mx - 110, my - 120, mx + 110, my + 20], fill=(235, 50, 70))
    for k in range(10): d.ellipse([mx - 70 + (k % 4) * 45, my - 70 + (k // 4) * 50, mx - 62 + (k % 4) * 45, my - 58 + (k // 4) * 50], fill=(255, 230, 120))
    d.polygon([(mx - 70, my - 110), (mx, my - 160), (mx + 70, my - 110), (mx, my - 90)], fill=(60, 170, 70))
    if t > 0.8: rotulo(d, 330, 1080, "BAGA ✔".replace("✔", "SIM"), 54, (120, 255, 120))
    if t > 1.8: rotulo(d, 790, 1080, "BAGA? NÃO!", 54, (255, 120, 120))


def c_erva(d, img, t, T):
    # bananeira: "tronco" feito de folhas enroladas
    d.rounded_rectangle([480, 640, 600, 1150], 50, fill=(110, 170, 70), outline=O, width=8)
    for k in range(6):
        d.line([(490, 700 + k * 80), (590, 670 + k * 80)], fill=(80, 130, 50), width=8)
    for k, a in enumerate((-2.4, -1.9, -1.2, -0.7)):
        x1, y1 = 540 + math.cos(a + math.sin(T + k) * 0.05) * 330, 640 + math.sin(a) * 200
        d.polygon([(540, 640), (x1, y1), (x1 + 40, y1 + 90)], fill=(70, 180, 80), outline=O)
    if t > 1.2: rotulo(d, 540, 1215, "UMA ERVA GIGANTE", 58, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="A BANANA É RADIOATIVA?",
         fala="Você sabia que a banana que você comeu hoje é levemente radioativa? Calma, eu explico! E o último fato vai mudar o jeito que você vê a banana."),
    dict(tipo="fato", titulo="TUDO POR CAUSA DO POTÁSSIO", desenho=c_potassio, fundo=((255, 190, 60), (230, 110, 40)),
         fala="A banana é famosa por ter muito potássio, um mineral importante pro coração e pros músculos."),
    dict(tipo="fato", titulo="UM POUQUINHO RADIOATIVO", desenho=c_radioativo, fundo=((30, 50, 40), (10, 20, 15)), estrelas=True,
         fala="Só que uma partezinha minúscula de todo potássio da natureza é radioativa: o potássio quarenta. Então, sim, toda banana emite um pouquinho de radiação."),
    dict(tipo="fato", titulo="É PERIGOSO?", desenho=c_dose, fundo=((30, 45, 90), (12, 20, 50)),
         fala="Mas relaxa: é tão pouco que você precisaria comer umas duzentas bananas pra receber a mesma dose de um único raio-X do peito."),
    dict(tipo="fato", titulo="DETECTOR APITANDO", desenho=c_porto, fundo=((120, 180, 230), (70, 120, 180)),
         fala="Mesmo assim, já aconteceu de caminhões cheios de bananas fazerem apitar detectores de radiação em portos e fronteiras!"),
    dict(tipo="fato", titulo="VOCÊ TAMBÉM É!", desenho=c_corpo, fundo=((40, 30, 80), (15, 10, 40)), estrelas=True,
         fala="E tem mais: o seu corpo também tem potássio quarenta. Ou seja, você também é um pouquinho radioativo, e isso é totalmente normal."),
    dict(tipo="fato", titulo="BANANA É BAGA. MORANGO NÃO!", desenho=c_baga, fundo=((255, 150, 170), (200, 80, 120)),
         fala="Pra botânica, a banana é uma baga, igual à uva. Já o morango, que parece uma frutinha vermelha, não é baga de verdade!"),
    dict(tipo="fato", titulo="BANANEIRA NÃO É ÁRVORE", desenho=c_erva, fundo=((150, 210, 255), (80, 160, 120)),
         fala="E o mais bizarro: a bananeira nem é uma árvore! Ela não tem tronco de madeira. É uma erva gigante, feita de folhas enroladas."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Qual fato te surpreendeu mais?",
         fala="Qual desses fatos te surpreendeu mais? Me conta nos comentários!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "banana.mp4"))
