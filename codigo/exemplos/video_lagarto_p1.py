"""Lagarto-de-chifre, Parte 1 (BICHOS INSANOS #2). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, O

SERIE = "BICHOS INSANOS #2"
PELE = (205, 160, 105); PELE2 = (160, 115, 70); BARRIGA = (235, 210, 160); ESPINHO = (240, 225, 190)
SANGUE = (215, 25, 35); SANGUE2 = (150, 10, 20)
AREIA = (235, 195, 130); AREIA2 = (205, 160, 95)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def chao(d, y0):
    d.rectangle([0, y0, 1080, 1920], fill=AREIA2)
    pts = [(0, 1920)] + [(x, y0 + math.sin(x / 130) * 18) for x in range(0, 1101, 40)] + [(1080, 1920)]
    d.polygon(pts, fill=AREIA)


def cacto(d, x, y, s):
    V = (70, 150, 80)
    d.rounded_rectangle([x - 35 * s, y - 300 * s, x + 35 * s, y], 30, fill=V, outline=O, width=6)
    d.rounded_rectangle([x - 120 * s, y - 220 * s, x - 70 * s, y - 120 * s], 22, fill=V, outline=O, width=6)
    d.rectangle([x - 100 * s, y - 140 * s, x - 30 * s, y - 110 * s], fill=V)
    d.rounded_rectangle([x + 70 * s, y - 250 * s, x + 120 * s, y - 150 * s], 22, fill=V, outline=O, width=6)
    d.rectangle([x + 30 * s, y - 170 * s, x + 100 * s, y - 140 * s], fill=V)


def lagarto(d, cx, cy, s, T, inchado=0.0, olhar=1):
    """Lagarto-de-chifre de perfil, olhando para a direita (olhar=1) ou esquerda (-1).
    Devolve a posição do olho (para o jato de sangue)."""
    f = olhar
    X = lambda x: cx + f * x * s
    Y = lambda y: cy + y * s
    g = 1 + 0.25 * inchado
    # cauda
    d.polygon([(X(-150), Y(10)), (X(-330), Y(40)), (X(-150), Y(45))], fill=PELE2, outline=O)
    # patas
    for px in (-100, 90):
        d.line([(X(px), Y(30)), (X(px - 20), Y(95))], fill=PELE2, width=int(26 * s))
        d.line([(X(px - 20), Y(95)), (X(px + 15), Y(100))], fill=PELE2, width=int(14 * s))
    # corpo achatado (incha)
    d.ellipse([X(-175 * g) if f > 0 else X(175 * g), Y(-70 * g), X(175 * g) if f > 0 else X(-175 * g), Y(55)], fill=PELE, outline=O, width=6)
    d.ellipse([X(-140) if f > 0 else X(140), Y(10), X(140) if f > 0 else X(-140), Y(52)], fill=BARRIGA)
    # espinhos das costas e dos lados
    for i in range(9):
        a = math.pi * (0.1 + 0.8 * i / 8)
        bx, by = -math.cos(a) * 165 * g, -math.sin(a) * 62 * g
        d.polygon([(X(bx - 14), Y(by + 4)), (X(bx), Y(by - 34)), (X(bx + 14), Y(by + 4))], fill=ESPINHO, outline=O)
    for i in range(5):  # pintas
        x = -110 + i * 50
        d.ellipse([X(x - 14) if f > 0 else X(x + 14), Y(-30), X(x + 14) if f > 0 else X(x - 14), Y(-8)], fill=PELE2)
    # cabeça
    d.polygon([(X(130), Y(-40)), (X(215), Y(-50)), (X(265), Y(-5)), (X(240), Y(30)), (X(140), Y(35))], fill=PELE, outline=O)
    # chifres da coroa
    for hx, hl in ((170, 60), (200, 70), (228, 55)):
        d.polygon([(X(hx - 14), Y(-44)), (X(hx - 22), Y(-44 - hl)), (X(hx + 10), Y(-46))], fill=ESPINHO, outline=O)
    # boca
    d.line([(X(200), Y(15)), (X(260), Y(5))], fill=O, width=5)
    # olho
    ex, ey = X(212), Y(-18)
    r = 15 * s
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(250, 200, 40), outline=O, width=4)
    d.ellipse([ex - r * 0.45, ey - r * 0.8, ex + r * 0.45, ey + r * 0.8], fill=O)
    return ex, ey


def jato(d, ex, ey, T, alcance=420, dir=1, forca=1.0, t0=0.0):
    """Arco de gotas de sangue saindo do olho."""
    for i in range(22):
        fase = (T * 1.4 + i / 22) % 1
        u = fase * forca
        x = ex + dir * alcance * u
        y = ey - 140 * forca * math.sin(u * math.pi * 0.9) + 120 * u * u
        r = 13 - 6 * u
        d.ellipse([x - r, y - r, x + r, y + r], fill=SANGUE, outline=SANGUE2)


def poca(d, x, y, k):
    if k <= 0:
        return
    d.ellipse([x - 90 * k, y - 22 * k, x + 90 * k, y + 22 * k], fill=SANGUE2)


# ---------------- cenas ----------------
def g_sangue(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    chao(d, 1060)
    cacto(d, 90, 1075, 0.5)
    ex, ey = lagarto(d, 330, 980, 1.25, T)
    jato(d, ex, ey, T, alcance=380)
    poca(d, ex + 390, 1085, 0.9)
    rotulo(d, 820, 1210, "OLHOS!", 76, AMARELO)


def regua(d, x0, x1, y, rot):
    d.line([(x0, y), (x1, y)], fill="white", width=8)
    for x in (x0, x1):
        d.line([(x, y - 25), (x, y + 25)], fill="white", width=8)
    rotulo(d, (x0 + x1) / 2, y + 60, rot, 64, AMARELO)


def mapa_eua_mex(d, T):
    # mapa simplificado: EUA (cima) e México (baixo), sem fronteiras exatas
    d.polygon([(140, 560), (900, 540), (960, 640), (900, 720), (700, 760), (520, 780), (300, 770), (160, 700)],
              fill=(120, 175, 110), outline=O)
    d.polygon([(300, 770), (520, 780), (600, 860), (560, 960), (480, 1000), (430, 900), (330, 830)], fill=(150, 190, 110), outline=O)
    rotulo(d, 520, 640, "EUA", 48, "white")
    rotulo(d, 480, 880, "MÉXICO", 40, "white")
    # mancha onde vive
    a = 140 + 20 * math.sin(T * 3)
    d.ellipse([480 - a, 720 - a * 0.55, 480 + a, 720 + a * 0.55], fill=(255, 196, 30, 110), outline=(255, 196, 30), width=5)


def c_metro(d, img, t, T):
    selo(d)
    if t < 1.6:
        mapa_eua_mex(d, T)
        return
    chao(d, 1060)
    ex, ey = lagarto(d, 230, 980, 0.95, T)
    k = ease((t - 1.6) / 0.8)
    jato(d, ex, ey, T, alcance=560 * k + 1, forca=1.0)
    if t > 2.2:
        regua(d, ex, ex + 560, 1140, "1,5 METRO")


def cabeca_grande(d, T, pressao):
    cx, cy = 470, 940
    d.polygon([(cx - 330, cy - 120), (cx + 160, cy - 160), (cx + 360, cy - 10), (cx + 280, cy + 140), (cx - 330, cy + 150)],
              fill=PELE, outline=O, width=7)
    for hx, hl in ((-120, 170), (0, 200), (120, 160)):
        d.polygon([(cx + hx - 40, cy - 140), (cx + hx - 60, cy - 140 - hl), (cx + hx + 30, cy - 148)], fill=ESPINHO, outline=O)
    d.line([(cx + 60, cy + 70), (cx + 340, cy + 20)], fill=O, width=8)
    # veias ficando cheias
    for i, (vx, vy) in enumerate(((-260, 40), (-180, 90), (-240, -40))):
        w = int(8 + 14 * pressao)
        d.line([(cx + vx, cy + vy), (cx + 60, cy - 20 + i * 15)], fill=SANGUE, width=w)
    ex, ey = cx + 100, cy - 30
    r = 50
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(250, 200, 40), outline=O, width=6)
    d.ellipse([ex - 18, ey - 38, ex + 18, ey + 38], fill=O)
    return ex, ey


def c_pressao(d, img, t, T):
    selo(d)
    p = min(1, t / 2.2)
    ex, ey = cabeca_grande(d, T, p)
    # manômetro
    mx, my, mr = 180, 590, 100
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill="white", outline=O, width=7)
    a = math.pi * (1.1 + 0.8 * p) + (0.05 * math.sin(T * 30) if p > 0.9 else 0)
    d.line([(mx, my), (mx + math.cos(a) * 85, my + math.sin(a) * 85)], fill=SANGUE, width=10)
    d.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=O)
    rotulo(d, mx, my + 140, "PRESSÃO", 46, AMARELO)
    if t > 2.2:
        s = pop((t - 2.2) / 0.4)
        for i in range(8):
            a = -0.9 + i * 0.25
            dd = 70 + 160 * s + (i % 3) * 30
            x, y = ex + math.cos(a) * dd, ey + math.sin(a) * dd * 0.6
            d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=SANGUE, outline=SANGUE2)
        rotulo(d, ex - 20, ey + 230, "PLOFT!", 70, "white")


def tanque(d, x, y, nivel, rot):
    w, h = 170, 380
    d.rounded_rectangle([x - w / 2, y - h, x + w / 2, y], 30, fill=(240, 240, 250), outline=O, width=7)
    hh = (h - 20) * nivel
    d.rounded_rectangle([x - w / 2 + 12, y - 10 - hh, x + w / 2 - 12, y - 10], 20, fill=SANGUE)
    rotulo(d, x, y + 60, rot, 48, "white")


def c_terco(d, img, t, T):
    selo(d)
    k = ease((t - 0.5) / 2.0) if t > 0.5 else 0
    tanque(d, 300, 1080, 1 - k / 3, "SANGUE")
    for i in range(3):
        y = 1080 - 120 * i - 60
        d.line([(400, y), (440, y)], fill="white", width=6)
    ex, ey = lagarto(d, 760, 900, 0.7, T, olhar=-1)
    jato(d, ex, ey, T, alcance=200, dir=-1, forca=0.6)
    if t > 1.0:
        rotulo(d, 760, 1120, "ATÉ 1/3", 90, AMARELO)


def c_cta(d, img, t, T):
    g_sangue(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="SANGUE!", titulo_y=400, desenho=g_sangue, fundo=((255, 190, 120), (230, 120, 80)),
         fala="Esse lagarto dispara sangue pelos olhos! E o último fato é o pior."),
    dict(tipo="fato", titulo="O LAGARTO", desenho=c_metro, fundo=((120, 180, 230), (60, 120, 190)),
         fala="É o lagarto-de-chifre, dos Estados Unidos e do México. Segue a Maia, que piora: o jato chega a um metro e meio!"),
    dict(tipo="fato", titulo="COMO?", desenho=c_pressao, fundo=((250, 170, 110), (190, 90, 70)),
         fala="Ele aperta umas veias da cabeça, a pressão sobe, e estouram vasinhos no canto dos olhos."),
    dict(tipo="fato", titulo="1/3 DO SANGUE", desenho=c_terco, fundo=((90, 60, 100), (40, 25, 60)),
         fala="E num jato só, ele pode perder até um terço do próprio sangue."),
    dict(tipo="cta", titulo="SANGUE!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((255, 190, 120), (230, 120, 80)),
         fala="Mas o pior é o que tem nesse sangue. Segue a Maia pra ver a parte dois às seis da tarde. Porque esse lagarto..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lagarto_p1.mp4"))
