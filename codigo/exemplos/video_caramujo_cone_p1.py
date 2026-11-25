"""Caramujo-cone, Parte 1 (BICHOS INSANOS #10). Formato v3 + ESTRATÉGIA DA SEMANA 23/11
(20–28 s, fato chocante no 1º segundo, 1 frase de opinião da MAIA). Sem a palavra proibida.
Fatos (DAN - Divers Alert Network; StatPearls/NIH): caramujos-cone (~600+ espécies, mares quentes) caçam
disparando um dente em forma de arpão (rádula) cheio de veneno a partir de uma tromba; o veneno tem
centenas de toxinas (conotoxinas); NÃO existe antídoto (tratamento só de suporte); mortes humanas são
raras, mas acontecem (sobretudo Conus geographus); a picada pode quase não doer e ainda assim ser letal."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "BICHOS INSANOS #10"
CONCHA = (240, 215, 160); MANCHA = (150, 80, 40); MANCHA2 = (90, 45, 20)
CORPO = (225, 120, 130); TROMBA = (240, 150, 160)
VENENO = (150, 255, 90)
MAR1 = (8, 70, 100); MAR2 = (2, 18, 40)
AREIA = (215, 190, 130); AREIA2 = (175, 150, 95)


def etiqueta(d, parte="P1"):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def areia(d, y=1150):
    d.polygon([(0, 1260), (0, y), (240, y - 20), (480, y + 12), (720, y - 18), (900, y + 10), (1080, y - 8), (1080, 1260)],
              fill=AREIA, outline=O)
    for i in range(8):
        x = 60 + i * 135
        d.ellipse([x - 12, y + 45, x + 12, y + 57], fill=AREIA2)


def concha(d, cx, cy, s=1.0, T=0.0, giro=0.0):
    """Concha em forma de cone deitada (ponta à esquerda, abertura à direita), com manchas tipo mapa."""
    w, h = 300 * s, 120 * s
    # espiral (topo) à esquerda
    d.polygon([(cx - w, cy), (cx - w * 0.55, cy - h * 0.55), (cx - w * 0.55, cy + h * 0.55)], fill=CONCHA, outline=O)
    # corpo do cone
    d.polygon([(cx - w * 0.6, cy - h * 0.6), (cx + w * 0.55, cy - h), (cx + w * 0.62, cy + h), (cx - w * 0.6, cy + h * 0.6)],
              fill=CONCHA, outline=O)
    d.line([(cx - w * 0.6, cy - h * 0.6), (cx + w * 0.55, cy - h)], fill=O, width=max(4, int(7 * s)))
    d.line([(cx - w * 0.6, cy + h * 0.6), (cx + w * 0.62, cy + h)], fill=O, width=max(4, int(7 * s)))
    for i in range(9):
        u = (i % 3) / 3 + 0.1
        v = (i // 3) / 3 - 0.33
        x = cx - w * 0.45 + u * w * 0.95
        y = cy + v * h * 1.3 + math.sin(i * 2.1) * 10 * s
        r = (18 + (i * 7) % 16) * s
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=MANCHA if i % 2 else MANCHA2)
    for k in range(4):
        x = cx - w * 0.85 + k * 30 * s
        d.line([(x, cy - 20 * s + k * 3 * s), (x + 20 * s, cy + 20 * s - k * 3 * s)], fill=MANCHA2, width=max(3, int(5 * s)))
    # pé/corpo mole saindo embaixo, à direita
    d.ellipse([cx + w * 0.2, cy + h * 0.7, cx + w * 1.0, cy + h * 1.15], fill=CORPO, outline=O, width=5)
    # sifão (tubinho) balançando
    a = math.sin(T * 3) * 0.3
    sx, sy = cx + w * 0.58, cy - h * 0.7
    ex, ey = sx + math.cos(-0.6 + a) * 110 * s, sy + math.sin(-0.6 + a) * 110 * s
    d.line([(sx, sy), (ex, ey)], fill=O, width=int(30 * s))
    d.line([(sx, sy), (ex, ey)], fill=TROMBA, width=int(20 * s))
    # olhinhos em pedúnculos
    for k, dx in enumerate((0.75, 0.9)):
        bx, by = cx + w * dx, cy + h * 0.75
        tx, ty = bx + 10 * s, by - 60 * s + math.sin(T * 4 + k) * 6 * s
        d.line([(bx, by), (tx, ty)], fill=O, width=int(10 * s))
        d.ellipse([tx - 12 * s, ty - 12 * s, tx + 12 * s, ty + 12 * s], fill=(255, 255, 255), outline=O, width=3)
        d.ellipse([tx - 5 * s, ty - 5 * s, tx + 5 * s, ty + 5 * s], fill=O)
    return (cx + w * 0.62, cy + h * 0.2)


def arpao(d, x0, y0, x1, y1, w=10, veneno=True):
    """Dente-arpão: haste oca com farpa na ponta e gota de veneno."""
    d.line([(x0, y0), (x1, y1)], fill=O, width=w + 8)
    d.line([(x0, y0), (x1, y1)], fill=(245, 245, 235), width=w)
    ang = math.atan2(y1 - y0, x1 - x0)
    L = w * 3.2
    p1 = (x1 + math.cos(ang) * L, y1 + math.sin(ang) * L)
    p2 = (x1 + math.cos(ang + 2.5) * L * 0.8, y1 + math.sin(ang + 2.5) * L * 0.8)
    p3 = (x1 + math.cos(ang - 2.5) * L * 0.8, y1 + math.sin(ang - 2.5) * L * 0.8)
    d.polygon([p1, p2, p3], fill=(245, 245, 235), outline=O)
    if veneno:
        gx, gy = p1
        d.ellipse([gx - w * 0.9, gy - w * 0.4, gx + w * 0.9, gy + w * 1.6], fill=VENENO, outline=O, width=3)


def mao(d, cx, cy, s=1.0):
    """Mão humana estilizada vinda da direita, palma aberta."""
    pele = (240, 190, 150)
    d.rounded_rectangle([cx - 20 * s, cy - 70 * s, cx + 200 * s, cy + 70 * s], radius=int(50 * s), fill=pele, outline=O, width=6)
    for k in range(4):
        y = cy - 55 * s + k * 37 * s
        d.rounded_rectangle([cx - 150 * s, y - 15 * s, cx + 10 * s, y + 15 * s], radius=int(15 * s), fill=pele, outline=O, width=5)
    d.rounded_rectangle([cx - 60 * s, cy + 50 * s, cx + 60 * s, cy + 95 * s], radius=int(22 * s), fill=pele, outline=O, width=5)
    d.rectangle([cx + 200 * s, cy - 60 * s, cx + 320 * s, cy + 60 * s], fill=(60, 110, 200), outline=O, width=6)


def g_arpao(d, img, t, T, label=True):
    etiqueta(d)
    areia(d, 1170)
    boca = concha(d, 330, 960, 1.05, T)
    mao(d, 800, 640, 0.9)
    # arpão disparado da concha até a mão, em ação já no 1º quadro
    k = min(1.0, 0.55 + t / 0.6)
    x0, y0 = boca[0] + 40, boca[1] - 140
    x1, y1 = x0 + (640 - x0) * k, y0 + (680 - y0) * k
    arpao(d, x0, y0, x1, y1, 12)
    if k >= 1:
        brilhos(d, 665, 660, 70, T, 8, VENENO)
    if label:
        kk = pop(min(1, max(0, t - 0.5) / 0.5))
        if kk > 0.05:
            rotulo(d, 600, 1215, "ARPÃO DE VENENO", int(48 * kk) + 1, VENENO)


def c_mares(d, img, t, T):
    selo(d)
    areia(d, 1120)
    # recife: corais coloridos
    for i, (x, c) in enumerate([(120, (255, 120, 90)), (300, (255, 200, 80)), (820, (180, 110, 255)), (980, (90, 220, 200))]):
        for j in range(4):
            a = -1.9 + j * 0.45 + math.sin(T * 2 + i + j) * 0.05
            d.line([(x, 1130), (x + math.cos(a) * 140, 1130 + math.sin(a) * 160)], fill=O, width=30)
            d.line([(x, 1130), (x + math.cos(a) * 140, 1130 + math.sin(a) * 160)], fill=c, width=20)
    k = ease(t / 1.0)
    concha(d, 1250 - 650 * k, 960, 0.8, T)
    kk = pop(min(1, max(0, t - 0.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 620, "MARES QUENTES", int(52 * kk) + 1, CIANO)
        rotulo(d, 540, 700, "+600 ESPÉCIES", int(44 * kk) + 1, (255, 255, 255))


def c_dente(d, img, t, T):
    selo(d)
    # zoom: o dente-arpão grande atravessando a tela, peixe na mira
    k = ease(t / 0.8)
    arpao(d, 120, 1050, 120 + 640 * k, 1050 - 330 * k, 26)
    # corte mostrando que é oco
    d.line([(160, 1030), (120 + 600 * k, 1050 - 310 * k - 20)], fill=VENENO, width=6)
    # peixinho
    px, py = 860 + math.sin(T * 3) * 10, 650
    d.ellipse([px - 90, py - 50, px + 90, py + 50], fill=(255, 170, 60), outline=O, width=6)
    d.polygon([(px + 80, py), (px + 150, py - 55), (px + 150, py + 55)], fill=(255, 140, 40), outline=O)
    d.ellipse([px - 60, py - 18, px - 30, py + 12], fill=(255, 255, 255), outline=O, width=3)
    d.ellipse([px - 50, py - 8, px - 40, py + 2], fill=O)
    kk = pop(min(1, max(0, t - 0.3) / 0.5))
    if kk > 0.05:
        rotulo(d, 330, 1160, "DENTE OCO", int(50 * kk) + 1, AMARELO)
        rotulo(d, 760, 1160, "DISPARA!", int(50 * kk) + 1, VENENO)


def c_antidoto(d, img, t, T):
    selo(d)
    # frasco de antídoto vazio, com X vermelho; gotas de toxinas coloridas em volta
    for i in range(14):
        a = i / 14 * 6.283 + T * 0.6
        r = 300 + math.sin(T * 2 + i) * 20
        x, y = 540 + math.cos(a) * r, 860 + math.sin(a) * r * 0.75
        cor = [(150, 255, 90), (255, 90, 160), (120, 200, 255), (255, 210, 60)][i % 4]
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=cor, outline=O, width=4)
    d.rounded_rectangle([450, 700, 630, 1010], radius=30, outline=(230, 240, 255), width=10)
    d.rectangle([490, 650, 590, 700], fill=(180, 180, 190), outline=O, width=5)
    kk = pop(min(1, max(0, t - 0.6) / 0.4))
    if kk > 0.05:
        L = 130 * kk
        d.line([(540 - L, 855 - L), (540 + L, 855 + L)], fill=(235, 40, 40), width=24)
        d.line([(540 - L, 855 + L), (540 + L, 855 - L)], fill=(235, 40, 40), width=24)
        rotulo(d, 540, 1210, "SEM ANTÍDOTO", int(54 * kk) + 1, (255, 90, 90))
    rotulo(d, 540, 560, "CENTENAS DE TOXINAS", 42, VENENO)


def c_cta(d, img, t, T):
    g_arpao(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="ARPÃO!", titulo_y=400, desenho=g_arpao, fundo=(MAR1, MAR2),
         fala="Esse caracol mata um humano com um arpão de veneno! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="CARAMUJO", desenho=c_mares, fundo=((10, 90, 120), MAR2),
         fala="É o caramujo-cone, dos mares quentes. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="O ARPÃO", desenho=c_dente, fundo=((30, 40, 90), (10, 12, 35)),
         fala="o arpão é um dente oco, que ele dispara na presa feito flecha."),
    dict(tipo="fato", titulo="SEM CURA", desenho=c_antidoto, fundo=((70, 20, 50), (20, 5, 18)),
         fala="Centenas de toxinas, e nenhum antídoto. Nunca mais pego concha bonita na praia!"),
    dict(tipo="cta", titulo="ARPÃO!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="A parte dois é ainda mais louca: segue a Maia pra ver às seis da tarde. Tudo por causa desse caracol..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "caramujo_cone_p1.mp4"))
