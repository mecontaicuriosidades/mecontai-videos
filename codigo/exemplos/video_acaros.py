"""Ácaros Demodex: bichinhos que moram nos poros do rosto. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, sorriso, brilhos, seta, O

PELE = (250, 205, 175); PELE2 = (230, 170, 140); ACARO = (235, 225, 200); ACARO2 = (200, 185, 150)
ROSA = (255, 120, 170); VERDE = (150, 230, 110); OLEO = (255, 215, 80)


def acaro(d, x, y, s, T, ang=0.0, fase=0.0):
    """Ácaro Demodex de desenho: corpo de minhoca listrada, 8 perninhas na frente."""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    # perninhas (4 pares, perto da cabeça)
    for i in range(4):
        u = 30 - i * 14
        mov = math.sin(T * 12 + i + fase) * 6
        for sv in (-1, 1):
            d.line([P(u, sv * 12), P(u + mov, sv * 30)], fill=O, width=max(2, int(4 * s)))
    # corpo comprido
    pts = [P(45, 0), P(36, -16), P(0, -18), P(-60, -13), P(-95, -6), P(-105, 0), P(-95, 6), P(-60, 13), P(0, 18), P(36, 16)]
    d.polygon(pts, fill=ACARO, outline=O)
    for k in range(5):
        u = -10 - k * 17
        d.line([P(u, -15 + k * 1.5), P(u, 15 - k * 1.5)], fill=ACARO2, width=max(2, int(3 * s)))
    hx, hy = P(36, 0)
    r = 4.5 * s
    d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=O)


def rosto(d, cx, cy, r, T, dormindo=False):
    d.ellipse([cx - r, cy - r * 1.15, cx + r, cy + r * 1.15], fill=PELE, outline=O, width=8)
    if dormindo:
        for sx in (-1, 1):
            ex = cx + sx * r * 0.35
            d.arc([ex - r * 0.16, cy - r * 0.2, ex + r * 0.16, cy + r * 0.05], 20, 160, fill=O, width=7)
    else:
        olhos(d, cx, cy - r * 0.1, T, esp=r * 0.7, r=r * 0.13)
    d.polygon([(cx, cy + r * 0.05), (cx - r * 0.1, cy + r * 0.3), (cx + r * 0.08, cy + r * 0.3)], fill=PELE2)
    sorriso(d, cx, cy + r * 0.48, r * 0.28)


def poro(d, x, y, s=1.0):
    d.ellipse([x - 14 * s, y - 9 * s, x + 14 * s, y + 9 * s], fill=PELE2, outline=(150, 100, 80), width=3)


# ---------------- cenas ----------------
def g_poros(d, img, t, T):
    # lupa gigante sobre um nariz: ácaros saindo dos poros já no 1º quadro
    cx, cy, R = 560, 790, 330
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=PELE, outline=O, width=14)
    for i, (px, py) in enumerate([(430, 650), (640, 620), (560, 800), (400, 900), (720, 870), (560, 1000), (760, 720)]):
        poro(d, px, py, 1.6)
        sai = 0.5 + 0.5 * math.sin(T * 2.2 + i * 1.3)
        acaro(d, px + 10, py - 50 * sai, 1.0, T, ang=-1.57 + 0.3 * math.sin(T + i), fase=i)
    # cabo da lupa
    d.line([(cx + R * 0.72, cy + R * 0.72), (cx + R * 1.05, cy + R * 1.2)], fill=(90, 60, 40), width=50)
    d.ellipse([cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10], outline=(200, 210, 230), width=10)
    if t > 0.8:
        rotulo(d, 560, 1210, "NO SEU ROSTO", 60, AMARELO)


def c_todos(d, img, t, T):
    cores = [(250, 205, 175), (200, 150, 110), (150, 100, 70), (240, 190, 160), (120, 80, 55), (225, 175, 130)]
    for i in range(6):
        x, y = 230 + (i % 3) * 310, 620 + (i // 3) * 330
        r = 110
        d.ellipse([x - r, y - r * 1.1, x + r, y + r * 1.1], fill=cores[i], outline=O, width=6)
        olhos(d, x, y - 15, T + i, esp=70, r=13)
        sorriso(d, x, y + 45, 30)
        if t > 0.4 + i * 0.25:
            acaro(d, x + 55, y + 70, 0.55, T, ang=-0.6, fase=i)
    if t > 2.2:
        rotulo(d, 540, 1230, "0,3 mm", 70, VERDE)


def c_oleo(d, img, t, T):
    # corte da pele: folículo com ácaros de cabeça pra baixo comendo óleo
    d.rectangle([90, 560, 990, 1250], fill=PELE2, outline=O, width=8)
    d.rectangle([90, 560, 990, 640], fill=PELE, outline=O, width=8)
    # folículo
    d.polygon([(470, 560), (610, 560), (590, 1130), (490, 1130)], fill=(250, 225, 200), outline=O)
    d.line([(540, 400), (540, 1150)], fill=(70, 45, 30), width=18)  # pelo
    d.ellipse([440, 1090, 640, 1200], fill=(255, 235, 150), outline=O, width=6)  # glândula de óleo
    for i in range(5):
        y = 1080 - ((T * 90 + i * 70) % 380)
        d.ellipse([515 + (i % 2) * 40, y - 12, 540 + (i % 2) * 40, y + 12], fill=OLEO, outline=O, width=3)
    for i, (x, y) in enumerate([(505, 800), (575, 880), (505, 960)]):
        acaro(d, x, y + math.sin(T * 3 + i) * 8, 0.75, T, ang=1.57, fase=i)
    if t > 1.0:
        rotulo(d, 790, 1050, "ÓLEO = COMIDA", 46, AMARELO)
        seta(d, 760, 1080, 650, 1130, AMARELO, 10)


def c_noite(d, img, t, T):
    # lua, rosto dormindo e dois ácaros se encontrando com coraçõezinhos
    d.ellipse([780, 470, 940, 630], fill=(250, 245, 210), outline=O, width=6)
    d.ellipse([740, 450, 880, 590], fill=(30, 25, 70))
    rosto(d, 400, 860, 240, T, dormindo=True)
    for i in range(3):
        y = 560 - ((T * 60 + i * 50) % 150)
        rotulo(d, 600 + i * 40, y, "z", 50 + i * 10, (200, 200, 255), traduzir=False)
    k = ease(t / 1.5)
    acaro(d, 250 + 90 * k, 1000, 0.9, T, ang=0.0)
    acaro(d, 560 - 90 * k, 1000, 0.9, T, ang=math.pi, fase=2)
    if t > 1.5:
        for i in range(3):
            hx = 400 + (i - 1) * 50; hy = 920 - ((T * 70 + i * 40) % 140)
            d.ellipse([hx - 16, hy - 10, hx, hy + 6], fill=ROSA); d.ellipse([hx - 2, hy - 10, hx + 14, hy + 6], fill=ROSA)
            d.polygon([(hx - 16, hy), (hx + 14, hy), (hx - 1, hy + 18)], fill=ROSA)
    if t > 2.0:
        rotulo(d, 790, 1180, "TODA NOITE", 56, AMARELO)


def c_mae(d, img, t, T):
    # mãe abraçando bebê, ácaros "mudando de casa"
    rosto(d, 400, 760, 190, T)
    d.pieslice([140, 900, 660, 1400], 180, 360, fill=(230, 90, 120), outline=O, width=7)
    rosto(d, 690, 900, 105, T + 1)
    k = (t * 0.6) % 1
    acaro(d, 520 + 130 * k, 820 + 60 * k, 0.6, T, ang=0.4)
    if t > 1.0:
        brilhos(d, 690, 900, 170, T, n=6, cor=ROSA)
        rotulo(d, 740, 1150, "DESDE BEBÊ", 52, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="BICHOS NA CARA", desenho=g_poros, fundo=((150, 40, 90), (50, 10, 35)),
         fala="Agora mesmo, tem bichinhos morando nos poros do seu rosto. E de noite, eles saem da toca!"),
    dict(tipo="fato", titulo="QUASE TODO MUNDO", desenho=c_todos, fundo=((40, 110, 90), (10, 45, 35)),
         fala="São os ácaros Demodex. Quase todo adulto tem, e cada um mede só um terço de milímetro."),
    dict(tipo="fato", titulo="COMEM SUA PELE", desenho=c_oleo, fundo=((150, 100, 40), (60, 35, 10)),
         fala="Eles vivem de cabeça pra baixo dentro dos poros, comendo a oleosidade da sua pele. E cada um tem oito perninhas."),
    dict(tipo="fato", titulo="ENCONTRO NOTURNO", desenho=c_noite, fundo=((30, 25, 90), (8, 5, 35)),
         fala="E à noite, enquanto você dorme, eles saem pra andar e acasalar na sua cara."),
    dict(tipo="fato", titulo="PRESENTE DE MÃE", desenho=c_mae, fundo=((170, 70, 110), (70, 20, 50)),
         fala="E sabe de quem você pegou? Quase sempre da sua própria mãe, logo depois que você nasceu!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Vai lavar o rosto agora?",
         fala="Comenta: vai lavar o rosto agora? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "acaros.mp4"))
