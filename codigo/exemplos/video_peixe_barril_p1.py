"""Peixe-barril / barreleye (Macropinna microstoma), Parte 1 (BICHOS INSANOS #8).
Formato v3 + ESTRATÉGIA DA SEMANA 23/11 (sem selo no meio, 20–28 s, fato chocante no 1º segundo)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "BICHOS INSANOS #8"
CORPO = (70, 60, 85); CORPO2 = (45, 38, 60); BARB = (110, 95, 120)
VIDRO = (170, 240, 255); VERDE = (90, 255, 120); VERDE2 = (30, 150, 70)
MAR1 = (8, 30, 70); MAR2 = (2, 8, 25)


def etiqueta(d, parte="P1"):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def particulas(d, T, n=26, y0=520, y1=1260):
    for i in range(n):
        x = (i * 173 + T * 18 * (1 + i % 3)) % 1080
        y = y0 + ((i * 97 - T * 25 * (1 + i % 2)) % (y1 - y0))
        r = 3 + i % 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 200, 230))


def tubo_olho(d, bx, by, ang, s=1.0):
    """Olho tubular: cilindro verde saindo de (bx,by) na direção ang (rad, 0=direita, -pi/2=cima)."""
    L, w = 95 * s, 26 * s
    ex, ey = bx + math.cos(ang) * L, by + math.sin(ang) * L
    nx, ny = -math.sin(ang) * w, math.cos(ang) * w
    d.polygon([(bx + nx, by + ny), (ex + nx, ey + ny), (ex - nx, ey - ny), (bx - nx, by - ny)], fill=VERDE2, outline=O)
    d.ellipse([ex - w * 1.15, ey - w * 1.15, ex + w * 1.15, ey + w * 1.15], fill=VERDE, outline=O, width=5)
    d.ellipse([ex - w * 0.45, ey - w * 0.45, ex + w * 0.15, ey + w * 0.15], fill=(230, 255, 230))


def peixe_barril(d, cx, cy, s=1.0, T=0.0, giro=0.0, narinas=True, brilho=True, cupula=True):
    """Corpo escuro, cúpula transparente (só contorno) e olhos-tubo dentro.
    giro=0 -> olhos para cima; giro=1 -> olhos para a frente (direita)."""
    bal = math.sin(T * 2.2) * 6 * s
    cy = cy + bal
    # cauda e nadadeiras
    d.polygon([(cx - 250 * s, cy), (cx - 360 * s, cy - 80 * s), (cx - 340 * s, cy + 90 * s)], fill=CORPO2, outline=O)
    aba = math.sin(T * 5) * 18 * s
    d.polygon([(cx - 40 * s, cy + 40 * s), (cx - 170 * s, cy + 150 * s + aba), (cx + 10 * s, cy + 90 * s)], fill=BARB, outline=O)
    d.polygon([(cx - 120 * s, cy - 60 * s), (cx - 200 * s, cy - 150 * s - aba), (cx - 60 * s, cy - 70 * s)], fill=BARB, outline=O)
    # corpo
    d.ellipse([cx - 270 * s, cy - 85 * s, cx + 170 * s, cy + 95 * s], fill=CORPO, outline=O, width=7)
    for k in range(4):
        xx = cx - 200 * s + k * 70 * s
        d.arc([xx - 30 * s, cy - 60 * s, xx + 30 * s, cy + 60 * s], 300, 60, fill=CORPO2, width=5)
    # boquinha e "narinas" (parecem olhos!)
    d.line([(cx + 150 * s, cy + 30 * s), (cx + 180 * s, cy + 35 * s)], fill=O, width=int(7 * s))
    if narinas:
        for dx in (0, 34):
            x, y = cx + (110 + dx) * s, cy - 10 * s
            d.ellipse([x - 13 * s, y - 13 * s, x + 13 * s, y + 13 * s], fill=(20, 20, 30), outline=(200, 200, 220), width=3)
    if not cupula:
        return
    # olhos-tubo dentro da cúpula
    ang = -math.pi / 2 + giro * (math.pi / 2 - 0.15)
    for ox in (-30, 40):
        tubo_olho(d, cx + ox * s, cy - 70 * s, ang, s)
    # cúpula transparente (só contorno + reflexos)
    d.arc([cx - 120 * s, cy - 290 * s, cx + 180 * s, cy - 10 * s], 180, 360, fill=O, width=int(12 * s))
    d.arc([cx - 120 * s, cy - 290 * s, cx + 180 * s, cy - 10 * s], 180, 360, fill=VIDRO, width=int(6 * s))
    d.arc([cx - 90 * s, cy - 260 * s, cx + 60 * s, cy - 110 * s], 200, 250, fill=(240, 255, 255), width=int(7 * s))
    if brilho:
        brilhos(d, cx + 120 * s, cy - 250 * s, 30 * s, T, 4, VIDRO)


def g_vidro(d, img, t, T, label=True):
    etiqueta(d)
    particulas(d, T)
    peixe_barril(d, 600, 900, 1.25, T)
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if label and k > 0.05:
        seta(d, 250, 640, 440, 700, AMARELO, 10)
        rotulo(d, 230, 600, "TRANSPARENTE", int(42 * k) + 1, AMARELO)


def c_fundo(d, img, t, T):
    # régua de profundidade: superfície -> 700 m
    d.rectangle([0, 470, 1080, 520], fill=(60, 140, 220))
    rotulo(d, 150, 560, "0 M", 40, (255, 255, 255), traduzir=False)
    d.line([(150, 600), (150, 1180)], fill=(255, 255, 255), width=6)
    for i in range(6):
        y = 600 + i * 116
        d.line([(130, y), (170, y)], fill=(255, 255, 255), width=5)
    prof = ease(t / 1.6)
    yy = 600 + 580 * prof
    d.ellipse([136, yy - 14, 164, yy + 14], fill=AMARELO, outline=O, width=4)
    rotulo(d, 150, 1220, "700 M", 52, AMARELO, traduzir=False)
    particulas(d, T, 14, 560, 1200)
    peixe_barril(d, 640, 980, 0.95, T)
    rotulo(d, 640, 640, "QUASE SEM LUZ", 46, CIANO)


def c_narinas(d, img, t, T):
    # zoom na cara: as "bolinhas" são o nariz
    peixe_barril(d, 420, 980, 1.6, T, brilho=False)
    k = pop(min(1, max(0, t - 0.4) / 0.5))
    if k > 0.05:
        d.ellipse([560, 900, 720, 990], outline=AMARELO, width=8)
        rotulo(d, 820, 1110, "NARIZ!", int(70 * k) + 1, AMARELO)
        seta(d, 800, 1060, 700, 990, AMARELO, 10)
    if t < 0.9:
        rotulo(d, 820, 760, "OLHOS?", 60, (255, 255, 255))
    else:
        rotulo(d, 820, 760, "OLHOS?", 60, (120, 120, 140))
        d.line([(720, 740), (920, 780)], fill=(255, 80, 80), width=10)


def c_tubos(d, img, t, T):
    particulas(d, T, 16)
    peixe_barril(d, 520, 1020, 1.35, T)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 300, 600, "OLHOS DE VERDADE", int(46 * k) + 1, VERDE)
        seta(d, 340, 640, 480, 820, VERDE, 10)
    # luz caindo de cima (silhuetas)
    for i in range(3):
        x = 560 + (i - 1) * 140
        d.line([(x, 470), (x + 10, 620)], fill=(200, 230, 255), width=4)


def c_cta(d, img, t, T):
    g_vidro(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="É DE VIDRO?", titulo_y=400, desenho=g_vidro, fundo=(MAR1, MAR2),
         fala="Cabeça transparente, com os olhos lá dentro! E esse peixe existe."),
    dict(tipo="fato", titulo="PEIXE-BARRIL", desenho=c_fundo, fundo=((10, 40, 90), MAR2),
         fala="É o peixe-barril: vive a uns setecentos metros de fundo, quase sem luz."),
    dict(tipo="fato", titulo="NÃO É OLHO", desenho=c_narinas, fundo=((15, 35, 75), MAR2),
         fala="Essas bolinhas na frente? Não são olhos: são o nariz. Eu jurava que era olho!"),
    dict(tipo="fato", titulo="OLHOS-TUBO", desenho=c_tubos, fundo=((12, 45, 80), MAR2),
         fala="Os olhos de verdade são esses tubos verdes, virados pra cima."),
    dict(tipo="cta", titulo="É DE VIDRO?", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Às seis tem a parte dois: um segredo de setenta anos. Segue a Maia pra ver! Tudo por causa dessa..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "peixe_barril_p1.mp4"))
