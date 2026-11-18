"""Axolote, Parte 1 (BICHOS INSANOS #3). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, brilhos, O

SERIE = "BICHOS INSANOS #3"
ROSA = (250, 170, 190); ROSA2 = (225, 120, 150); BRANQ = (255, 90, 130); BARRIGA = (255, 215, 225)
VERDE_AGUA = (40, 140, 140); AREIA = (215, 190, 140)
CORACAO = (230, 40, 70); CEREBRO = (255, 160, 200); VERDE = (90, 230, 140)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def fundo_lago(d, y0, T):
    d.rectangle([0, y0, 1080, 1920], fill=AREIA)
    for i in range(7):  # plantinhas aquáticas
        x = 60 + i * 160
        sw = 14 * math.sin(T * 2 + i)
        d.line([(x, y0 + 10), (x + sw, y0 - 120 - (i % 3) * 30)], fill=(60, 150, 90), width=12)
    for i in range(6):  # bolhas
        fase = (T * 0.35 + i / 6) % 1
        x = 120 + i * 170 + 15 * math.sin(T * 3 + i)
        y = y0 - fase * 520
        d.ellipse([x - 10, y - 10, x + 10, y + 10], outline=(220, 245, 255), width=4)


def axolote(d, cx, cy, s, T, olhar=1, perna=1.0, cor=ROSA, cor2=ROSA2, guelra=1.0):
    """Axolote de perfil (olhar=1 → direita). perna: 0..1 tamanho da pata da frente (regenerando)."""
    f = olhar
    X = lambda x: cx + f * x * s
    Y = lambda y: cy + y * s
    bx = lambda a, b: (min(X(a), X(b)), max(X(a), X(b)))
    ond = math.sin(T * 4)
    # cauda com barbatana
    cauda = [(X(-120), Y(-40)), (X(-260), Y(-45 + 20 * ond)), (X(-360), Y(-10 + 30 * ond)),
             (X(-260), Y(35 + 20 * ond)), (X(-120), Y(40))]
    d.polygon(cauda, fill=cor, outline=O)
    d.line([(X(-130), Y(-48)), (X(-330), Y(-20 + 30 * ond))], fill=BARRIGA, width=int(8 * s))
    # patas de trás e da frente
    for px, k in ((-90, 1.0), (110, perna)):
        if k <= 0.02:
            continue
        x0, y0 = X(px), Y(30)
        x1, y1 = X(px + 10 * k), Y(30 + 70 * k)
        d.line([(x0, y0), (x1, y1)], fill=cor2, width=max(2, int(26 * s)))
        for dx in (-18, 0, 18):  # dedinhos
            d.line([(x1, y1), (x1 + f * dx * s * k, y1 + 22 * s * k)], fill=cor2, width=max(2, int(9 * s)))
    # corpo
    a, b = bx(-150, 140)
    d.ellipse([a, Y(-55), b, Y(55)], fill=cor, outline=O, width=6)
    a, b = bx(-120, 120)
    d.ellipse([a, Y(15), b, Y(52)], fill=BARRIGA)
    # cabeça larga
    a, b = bx(90, 300)
    d.ellipse([a, Y(-90), b, Y(70)], fill=cor, outline=O, width=6)
    # guelras (3 de cada lado, plumas)
    for i, ang in enumerate((-2.2, -1.75, -1.3)):
        ang2 = ang + 0.08 * math.sin(T * 5 + i)
        gx0, gy0 = X(120), Y(-50 + i * 12)
        if guelra < 0.05:
            break
        L = 120 * s * guelra
        gx1 = gx0 + f * math.cos(ang2) * L
        gy1 = gy0 + math.sin(ang2) * L
        d.line([(gx0, gy0), (gx1, gy1)], fill=BRANQ, width=max(2, int(12 * s)))
        for j in range(1, 5):
            u = j / 5
            px, py = gx0 + (gx1 - gx0) * u, gy0 + (gy1 - gy0) * u
            d.line([(px, py), (px - f * 22 * s * guelra, py - 14 * s * guelra)], fill=BRANQ, width=max(2, int(6 * s)))
            d.line([(px, py), (px + f * 18 * s * guelra, py - 20 * s * guelra)], fill=BRANQ, width=max(2, int(6 * s)))
    # olho e sorriso
    ex, ey = X(240), Y(-30)
    r = 14 * s
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=O)
    d.ellipse([ex - r * 0.4 + f * 3 * s, ey - r * 0.6, ex + r * 0.2 + f * 3 * s, ey - r * 0.1], fill="white")
    a, b = bx(200, 290)
    d.arc([a, Y(-10), b, Y(40)], 20, 160, fill=O, width=max(2, int(5 * s)))
    return X(40), Y(-10)  # centro do peito


def coracao(d, cx, cy, r, cor=CORACAO):
    d.ellipse([cx - r, cy - r * 0.9, cx, cy + r * 0.1], fill=cor, outline=O, width=4)
    d.ellipse([cx, cy - r * 0.9, cx + r, cy + r * 0.1], fill=cor, outline=O, width=4)
    d.polygon([(cx - r * 0.97, cy - r * 0.25), (cx + r * 0.97, cy - r * 0.25), (cx, cy + r)], fill=cor)
    d.line([(cx - r * 0.97, cy - r * 0.25), (cx, cy + r), (cx + r * 0.97, cy - r * 0.25)], fill=O, width=4)


def cerebro(d, cx, cy, r):
    d.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75], fill=CEREBRO, outline=O, width=5)
    d.line([(cx, cy - r * 0.7), (cx, cy + r * 0.7)], fill=O, width=4)
    for k in (-1, 1):
        for j in range(3):
            y = cy - r * 0.4 + j * r * 0.4
            d.arc([cx + k * r * 0.15 - r * 0.35, y - r * 0.18, cx + k * r * 0.15 + r * 0.35 + k * r * 0.2, y + r * 0.18],
                  180, 360, fill=ROSA2, width=4)


def remendo(d, cx, cy, r, k, T):
    """Anel verde de 'regeneração' que se fecha conforme k (0..1)."""
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * k, fill=VERDE, width=12)
    if k >= 1:
        brilhos(d, cx, cy, r + 30, T, n=6, cor=VERDE)


# ---------------- cenas ----------------
def g_regenera(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    fundo_lago(d, 1150, T)
    axolote(d, 600, 1010, 1.15, T, olhar=-1)
    k = 0.5 + 0.5 * ((T * 0.6) % 1)
    bate = 1 + 0.12 * abs(math.sin(T * 6))
    coracao(d, 230, 700, 70 * bate)
    remendo(d, 230, 690, 115, min(1, k * 1.2), T)
    cerebro(d, 850, 700, 85)
    remendo(d, 850, 700, 125, min(1, k * 1.2), T)
    rotulo(d, 230, 840, "CORAÇÃO", 40, "white")
    rotulo(d, 850, 840, "CÉREBRO", 40, "white")


def mapa_mexico(d, T):
    d.polygon([(120, 600), (560, 610), (700, 760), (900, 860), (960, 980), (840, 1060), (700, 1010),
               (560, 1080), (430, 980), (300, 820), (180, 720)], fill=(150, 190, 110), outline=O, width=5)
    rotulo(d, 420, 760, "MÉXICO", 52, "white")
    x, y = 640, 960
    a = 40 + 10 * math.sin(T * 4)
    d.ellipse([x - a, y - a, x + a, y + a], outline=AMARELO, width=7)
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=AMARELO)


def c_pata(d, img, t, T):
    selo(d)
    if t < 1.8:
        mapa_mexico(d, T)
        return
    fundo_lago(d, 1150, T)
    k = ease((t - 2.2) / 2.5) if t > 2.2 else 0
    axolote(d, 520, 960, 1.35, T, olhar=1, perna=k)
    px, py = 520 + 120 * 1.35, 960 + 70 * 1.35
    remendo(d, px, py, 80, k, T)
    rotulo(d, 820, 1150, "PATA NOVA", 52, AMARELO)


def coluna(d, cx, y0, n, k, T):
    for i in range(n):
        y = y0 + i * 62
        cheio = (i / n) < k
        cor = (245, 240, 225) if cheio else (90, 90, 110)
        d.rounded_rectangle([cx - 55, y, cx + 55, y + 44], 14, fill=cor, outline=O, width=5)
        d.line([(cx - 85, y + 22), (cx - 55, y + 22)], fill=cor, width=10)
        d.line([(cx + 55, y + 22), (cx + 85, y + 22)], fill=cor, width=10)
    # medula (fio amarelo) crescendo
    h = (n * 62) * k
    d.line([(cx, y0), (cx, y0 + h)], fill=AMARELO, width=12)


def c_coluna(d, img, t, T):
    selo(d)
    k = ease(t / 3.0)
    coluna(d, 330, 520, 10, k, T)
    rotulo(d, 330, 1180, "MEDULA", 46, AMARELO)
    # pele lisa: sem cicatriz
    d.rounded_rectangle([600, 640, 960, 960], 40, fill=ROSA, outline=O, width=6)
    if t < 1.5:
        d.line([(640, 800), (920, 800)], fill=ROSA2, width=14)
        for x in range(660, 920, 40):
            d.line([(x, 780), (x + 10, 820)], fill=ROSA2, width=6)
    else:
        brilhos(d, 780, 800, 150, T, n=6, cor=VERDE)
        rotulo(d, 780, 1010, "SEM CICATRIZ", 46, "white")


def dna(d, cx, y0, h, T, cor1, cor2, larg=60):
    n = max(3, int(h / 28))
    for i in range(n):
        y = y0 + i * 28
        a = T * 3 + i * 0.5
        x1, x2 = cx + math.sin(a) * larg, cx - math.sin(a) * larg
        d.line([(x1, y), (x2, y)], fill=(230, 230, 240), width=4)
        d.ellipse([x1 - 9, y - 9, x1 + 9, y + 9], fill=cor1)
        d.ellipse([x2 - 9, y - 9, x2 + 9, y + 9], fill=cor2)


def c_dna(d, img, t, T):
    selo(d)
    k = ease(t / 2.4)
    base = 1150
    hh = 80
    dna(d, 240, base - hh, hh, T, (120, 200, 255), (255, 255, 255), larg=40)
    rotulo(d, 240, base + 40, "HUMANO", 44, "white")
    H2 = 80 + (600 - 80) * k
    dna(d, 700, base - H2, H2, T, ROSA, VERDE, larg=70)
    rotulo(d, 700, base + 40, "AXOLOTE", 44, "white")
    if t > 1.6:
        rotulo(d, 450, 800, "10x", 110, AMARELO)


def c_cta(d, img, t, T):
    g_regenera(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="REGENERA!", titulo_y=400, desenho=g_regenera, fundo=((70, 170, 190), (20, 80, 120)),
         fala="Esse bicho regenera pedaços do próprio coração e do cérebro! E o último fato é o pior."),
    dict(tipo="fato", titulo="O AXOLOTE", desenho=c_pata, fundo=((110, 200, 200), (40, 120, 140)),
         fala="É o axolote, uma salamandra do México. Segue a Maia, que piora: se ele perde uma pata, nasce outra inteira, com osso e tudo."),
    dict(tipo="fato", titulo="COLUNA NOVA", desenho=c_coluna, fundo=((150, 120, 200), (70, 50, 130)),
         fala="Ele refaz até a medula da coluna. E sem deixar cicatriz."),
    dict(tipo="fato", titulo="DNA GIGANTE", desenho=c_dna, fundo=((40, 60, 110), (15, 20, 50)), estrelas=True,
         fala="E o DNA dele é cerca de dez vezes maior que o nosso."),
    dict(tipo="cta", titulo="REGENERA!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((70, 170, 190), (20, 80, 120)),
         fala="Mas o mais estranho é que ele nunca cresce de verdade. Segue a Maia pra ver a parte dois às seis da tarde. Porque esse bicho..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "axolote_p1.mp4"))
