"""Peixe-pedra: o peixe mais venenoso do mundo parece uma pedra. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

ROCHA = (125, 110, 95); ROCHA2 = (95, 80, 70); ALGA = (90, 150, 80); AREIA = (235, 210, 150)
ESPINHO = (240, 235, 220); PELE_PE = (240, 190, 160); VERMELHO = (230, 50, 50)


def areia(d, y=1050):
    d.rectangle([0, y, 1080, 1260], fill=AREIA)
    for i in range(14):
        x = 40 + i * 78
        d.arc([x - 30, y + 30 + (i % 3) * 40, x + 30, y + 60 + (i % 3) * 40], 200, 340, fill=(210, 180, 120), width=4)


def peixe_pedra(d, cx, cy, s, T, espinhos=0.0, olho=True, algas=True):
    """Corpo achatado e encaroçado, boca virada pra cima, espinhos que levantam."""
    if espinhos > 0:
        for k in range(13):
            x = cx - 180 * s + k * 30 * s
            h = (40 + 30 * math.sin(k * 0.9)) * s * espinhos
            d.polygon([(x - 7 * s, cy - 80 * s), (x + 7 * s, cy - 80 * s), (x, cy - 80 * s - h)], fill=ESPINHO, outline=O)
    pts = []
    for i in range(36):
        a = i / 36 * 2 * math.pi
        r = 1 + 0.08 * math.sin(a * 7) + 0.05 * math.sin(a * 13)
        pts.append((cx + math.cos(a) * 240 * s * r, cy + math.sin(a) * 110 * s * r))
    d.polygon(pts, fill=ROCHA, outline=O)
    d.line(pts + [pts[0]], fill=O, width=max(4, int(7 * s)))
    for (fx, fy, r) in [(-120, -20, 28), (-30, 30, 22), (70, -30, 30), (150, 30, 20), (-170, 40, 18), (20, -60, 16)]:
        d.ellipse([cx + (fx - r) * s, cy + (fy - r) * s, cx + (fx + r) * s, cy + (fy + r) * s], fill=ROCHA2, outline=O, width=3)
    if algas:
        for k in range(5):
            x = cx - 160 * s + k * 80 * s
            pts2 = [(x + math.sin(T * 2 + k + j * 0.8) * 10 * s, cy - 90 * s - j * 18 * s) for j in range(5)]
            d.line(pts2, fill=ALGA, width=max(4, int(9 * s)), joint="curve")
    d.arc([cx + 120 * s, cy - 50 * s, cx + 240 * s, cy + 10 * s], 200, 340, fill=O, width=max(4, int(7 * s)))  # boca
    if olho:
        for ox in (110, 170):
            d.ellipse([cx + (ox - 18) * s, cy - 75 * s, cx + (ox + 18) * s, cy - 39 * s], fill=(250, 240, 120), outline=O, width=3)
            d.ellipse([cx + (ox - 6) * s, cy - 65 * s, cx + (ox + 6) * s, cy - 49 * s], fill=O)


def pe(d, x, y, s):
    d.rounded_rectangle([x - 70 * s, y - 360 * s, x + 50 * s, y], int(40 * s), fill=PELE_PE, outline=O, width=6)
    d.rounded_rectangle([x - 90 * s, y - 70 * s, x + 170 * s, y + 30 * s], int(45 * s), fill=PELE_PE, outline=O, width=6)
    for k in range(5):
        d.ellipse([x + 110 * s - k * 30 * s, y - 85 * s, x + 150 * s - k * 30 * s, y - 50 * s], fill=PELE_PE, outline=O, width=3)


# ---------------- cenas ----------------
def g_pisada(d, img, t, T):
    areia(d)
    peixe_pedra(d, 640, 1000, 1.05, T, espinhos=min(1, t / 0.4))
    desce = ease(t / 0.9)
    pe(d, 600, 520 + 330 * desce, 1.0)
    if t > 0.7:
        for k in range(8):  # estrelinhas de dor
            a = k / 8 * 2 * math.pi + T
            d.line([(600 + math.cos(a) * 120, 830 + math.sin(a) * 60), (600 + math.cos(a) * 190, 830 + math.sin(a) * 100)],
                   fill=VERMELHO, width=8)
        rotulo(d, 860, 600, "AI!", 90, VERMELHO)


def c_disfarce(d, img, t, T):
    areia(d)
    for (x, y, s) in [(230, 1000, 0.55), (850, 990, 0.6)]:  # pedras de verdade
        d.ellipse([x - 140 * s * 1.6, y - 80 * s * 1.6, x + 140 * s * 1.6, y + 80 * s * 1.6], fill=(140, 130, 120), outline=O, width=6)
    peixe_pedra(d, 540, 990, 0.7, T, olho=(T % 2.2) > 1.1)
    if t > 1.2:
        seta(d, 540, 700, 540, 870, cor=AMARELO, w=12)
        rotulo(d, 540, 650, "É UM PEIXE!", 60, AMARELO)


def c_espinhos(d, img, t, T):
    peixe_pedra(d, 540, 900, 1.25, T, espinhos=ease(t / 1.0), algas=False)
    if t > 0.9:
        for k in range(3):  # gotas de veneno
            x = 380 + k * 140
            y = 640 + ((T * 120 + k * 50) % 120)
            d.polygon([(x, y - 22), (x - 14, y + 4), (x + 14, y + 4)], fill=(150, 230, 90), outline=O)
            d.ellipse([x - 14, y - 6, x + 14, y + 18], fill=(150, 230, 90), outline=O, width=3)
    rotulo(d, 540, 1170, "13 ESPINHOS", 64, ESPINHO)


def c_dor(d, img, t, T):
    # medidor de dor estourando
    x0, y0 = 160, 760
    d.rounded_rectangle([x0, y0, x0 + 760, y0 + 110], 50, fill=(240, 240, 240), outline=O, width=7)
    k = ease(t / 1.6)
    w = int(740 * min(1, k * 1.05))
    for i in range(0, w, 20):
        u = i / 740
        cor = (int(80 + 175 * u), int(220 - 190 * u), 60)
        d.rectangle([x0 + 10 + i, y0 + 12, x0 + 10 + min(i + 20, w), y0 + 98], fill=cor)
    rotulo(d, x0 + 40, y0 + 170, "0", 50)
    rotulo(d, x0 + 720, y0 + 170, "10", 50, VERMELHO)
    if k > 0.95:
        tremor = math.sin(T * 40) * 8
        rotulo(d, 540 + tremor, 620, "DOR MÁXIMA", 70, VERMELHO)
        pe(d, 540, 1200, 0.55)
        d.ellipse([560, 1130, 660, 1210], fill=(240, 120, 110), outline=O, width=4)  # inchaço


def c_agua(d, img, t, T):
    # balde de água quente com o pé dentro
    cx, cy = 520, 980
    d.ellipse([cx - 230, cy - 240, cx + 230, cy - 160], fill=(140, 200, 250), outline=O, width=6)
    pe(d, cx - 20, cy + 20, 1.0)
    d.polygon([(cx - 230, cy - 200), (cx + 230, cy - 200), (cx + 180, cy + 180), (cx - 180, cy + 180)], fill=(80, 140, 220, 190), outline=O)
    for i in range(4):  # vapor
        x = cx - 150 + i * 100
        pts = [(x + math.sin(T * 3 + j * 0.8 + i) * 16, cy - 260 - j * 30) for j in range(8)]
        d.line(pts, fill=(255, 255, 255, 200), width=12, joint="curve")
    d.rounded_rectangle([830, 620, 900, 1000], 30, fill=(240, 240, 240), outline=O, width=6)  # termômetro
    nivel = 0.7 * ease(t / 1.5)
    d.rectangle([848, 980 - 340 * nivel, 882, 980], fill=VERMELHO)
    d.ellipse([815, 970, 915, 1070], fill=VERMELHO, outline=O, width=6)
    rotulo(d, 860, 560, "QUENTE", 52, (255, 160, 120))


CENAS = [
    dict(tipo="gancho", titulo="PEDRA VENENOSA", desenho=g_pisada, fundo=((40, 150, 170), (10, 50, 80)),
         fala="Essa pedra é o peixe mais venenoso do mundo, e dá pra pisar nele sem ver. E o socorro é muito estranho."),
    dict(tipo="fato", titulo="DISFARCE PERFEITO", desenho=c_disfarce, fundo=((50, 120, 160), (15, 40, 70)),
         fala="É o peixe-pedra. Ele fica parado no fundo do mar raso, cheio de algas, igualzinho a uma pedra."),
    dict(tipo="fato", titulo="AGULHAS NAS COSTAS", desenho=c_espinhos, fundo=((90, 60, 130), (30, 20, 60)),
         fala="Nas costas ele tem treze espinhos. Quando alguém pisa, eles injetam o veneno direto no pé."),
    dict(tipo="fato", titulo="DOR NÍVEL 10", desenho=c_dor, fundo=((170, 60, 50), (60, 20, 20)),
         fala="A dor é descrita como uma das piores que existem, e o pé incha rapidinho."),
    dict(tipo="fato", titulo="O SOCORRO", desenho=c_agua, fundo=((60, 110, 90), (20, 40, 35)),
         fala="E o socorro estranho? Água bem quente, sem queimar, porque o calor quebra o veneno. E ainda existe soro."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você pisaria nessa pedra?",
         fala="Comenta: você já pisou em alguma coisa no mar? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "peixe_pedra.mp4"))
