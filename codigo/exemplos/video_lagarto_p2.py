"""Lagarto-de-chifre, Parte 2 (BICHOS INSANOS #2). Formato v3 (25–35 s). Usa o lagarto da Parte 1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, O
from video_lagarto_p1 import lagarto, jato, chao, etiqueta, selo, SANGUE, SANGUE2, PELE, PELE2, ESPINHO

COIOTE = (175, 140, 105); COIOTE2 = (130, 100, 75); FORMIGA = (170, 50, 30); GAVIAO = (115, 80, 55)


def coiote(d, cx, cy, s, T, boca=0.0, sacode=0.0):
    """Coiote/cachorro de perfil, olhando para a esquerda."""
    X = lambda x: cx + x * s
    Y = lambda y: cy + y * s
    # rabo
    d.polygon([(X(150), Y(-30)), (X(260), Y(10 + 10 * math.sin(T * 6))), (X(150), Y(10))], fill=COIOTE2, outline=O)
    # pernas
    for px in (-90, -40, 80, 125):
        d.line([(X(px), Y(20)), (X(px), Y(150))], fill=COIOTE2, width=int(24 * s))
    # corpo
    d.ellipse([X(-140), Y(-70), X(170), Y(50)], fill=COIOTE, outline=O, width=6)
    # cabeça (sacode)
    a = sacode * 0.35 * math.sin(T * 25)
    hx, hy = X(-150), Y(-90)
    def R(px, py):
        c, sn = math.cos(a), math.sin(a)
        return (hx + (px * c - py * sn) * s, hy + (px * sn + py * c) * s)
    d.polygon([R(-30, -70), R(-10, -150), R(30, -60)], fill=COIOTE2, outline=O)  # orelha
    d.polygon([R(40, -60), R(-40, -70), R(-160, -10), R(-170, 20 + 30 * boca), R(-60, 30), R(50, 40)], fill=COIOTE, outline=O)
    if boca > 0:
        d.polygon([R(-160, 5), R(-60, 15), R(-160, 15 + 30 * boca)], fill=(120, 30, 40))
    d.ellipse([R(-175, -18)[0] - 14 * s, R(-175, -18)[1] - 12 * s, R(-175, -18)[0] + 14 * s, R(-175, -18)[1] + 12 * s], fill=O)
    ox, oy = R(-40, -35)
    d.ellipse([ox - 12 * s, oy - 12 * s, ox + 12 * s, oy + 12 * s], fill=O)
    return R(-160, 10)


def jato_alvo(d, x0, y0, x1, y1, T, altura=140):
    for i in range(20):
        u = (T * 1.4 + i / 20) % 1
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - altura * 4 * u * (1 - u)
        r = 13 - 5 * u
        d.ellipse([x - r, y - r, x + r, y + r], fill=SANGUE, outline=SANGUE2)


def g_coiote(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    chao(d, 1080)
    ex, ey = lagarto(d, 170, 1010, 0.85, T)
    bx, by = coiote(d, 900, 950, 1.05, T, boca=0.6, sacode=0.4)
    jato_alvo(d, ex, ey, bx, by, T)
    rotulo(d, 830, 680, "ECA!", 76, AMARELO)


def c_solta(d, img, t, T):
    selo(d)
    chao(d, 1100)
    k = ease((t - 1.2) / 0.8) if t > 1.2 else 0
    bx, by = coiote(d, 700, 940, 1.0, T, boca=0.9 - 0.5 * k, sacode=k)
    # lagarto na boca e depois caindo
    lx = bx + 40 - 30 * k
    ly = by - 20 + 150 * k
    lagarto(d, lx, ly, 0.45, T, olhar=-1)
    if k > 0.3:
        for i in range(6):  # baba
            y = by + 30 + ((T * 300 + i * 40) % 160)
            d.ellipse([bx + 30 + i * 8, y, bx + 44 + i * 8, y + 22], fill=(210, 235, 255))
        rotulo(d, 330, 640, "BLEH!", 84, "white")
    rotulo(d, 860, 1220, "COIOTE", 48, "white")


def ave(d, cx, cy, s, T):
    X = lambda x: cx + x * s
    Y = lambda y: cy + y * s
    bat = 60 * math.sin(T * 8)
    d.polygon([(X(-20), Y(0)), (X(-230), Y(-80 - bat)), (X(-160), Y(30))], fill=GAVIAO, outline=O)
    d.ellipse([X(-90), Y(-45), X(110), Y(55)], fill=GAVIAO, outline=O, width=5)
    d.ellipse([X(70), Y(-80), X(150), Y(0)], fill=(235, 220, 190), outline=O, width=5)
    d.polygon([(X(145), Y(-45)), (X(195), Y(-25)), (X(145), Y(-15))], fill=(250, 200, 40), outline=O)
    d.ellipse([X(112), Y(-55), X(130), Y(-37)], fill=O)
    d.polygon([(X(20), Y(0)), (X(230), Y(-80 + bat)), (X(160), Y(30))], fill=COIOTE2, outline=O)


def c_estufa(d, img, t, T):
    selo(d)
    chao(d, 1100)
    ave(d, 700 - 60 * math.sin(T), 640 + 30 * math.sin(T * 1.3), 1.0, T)
    inc = min(1, t / 1.5) * (0.85 + 0.15 * math.sin(T * 4))
    lagarto(d, 420, 1010, 1.1, T, inchado=inc)
    if t > 1.5:
        rotulo(d, 600, 1220, "BALÃO DE ESPINHOS", 50, AMARELO)


def formiga(d, cx, cy, s, T):
    X = lambda x: cx + x * s
    Y = lambda y: cy + y * s
    for i, px in enumerate((-40, 0, 40)):
        m = 12 * math.sin(T * 10 + i * 2)
        d.line([(X(px), Y(10)), (X(px - 50 + m), Y(90))], fill=O, width=int(9 * s))
        d.line([(X(px), Y(10)), (X(px + 50 - m), Y(90))], fill=O, width=int(9 * s))
    d.ellipse([X(-190), Y(-55), X(-60), Y(55)], fill=FORMIGA, outline=O, width=5)
    d.ellipse([X(-70), Y(-30), X(50), Y(30)], fill=FORMIGA, outline=O, width=5)
    d.ellipse([X(40), Y(-50), X(150), Y(45)], fill=FORMIGA, outline=O, width=5)
    d.line([(X(130), Y(-35)), (X(200), Y(-120))], fill=O, width=int(7 * s))
    d.line([(X(110), Y(-40)), (X(150), Y(-140))], fill=O, width=int(7 * s))
    d.ellipse([X(95), Y(-25), X(120), Y(0)], fill="white")
    d.polygon([(X(-190), Y(0)), (X(-235), Y(-10)), (X(-190), Y(15))], fill=O)  # ferrão


def c_formigas(d, img, t, T):
    selo(d)
    chao(d, 1150)
    formiga(d, 560, 820, 1.6, T)
    if t > 0.8:
        rotulo(d, 540, 1040, "VENENO FORTÍSSIMO", 56, AMARELO)
    for i in range(5):
        x = (i * 230 + T * 120) % 1200 - 60
        formiga(d, x, 1190, 0.35, T)


def c_cta(d, img, t, T):
    g_coiote(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="GOSTO RUIM", titulo_y=400, desenho=g_coiote, fundo=((255, 200, 130), (220, 130, 80)),
         fala="Esse lagarto, que dispara sangue pelos olhos, tem um sangue que cachorro odeia! E o fim é o mais louco."),
    dict(tipo="fato", titulo="SOLTA!", desenho=c_solta, fundo=((150, 200, 235), (80, 140, 200)),
         fala="Coiotes e cachorros levam o jato na boca, sacodem a cabeça e soltam o lagarto. E segue pra mais bicho insano:"),
    dict(tipo="fato", titulo="E AS AVES?", desenho=c_estufa, fundo=((120, 175, 225), (50, 100, 170)),
         fala="Com aves, ele quase não usa o jato: se estufa feito um balão cheio de espinhos."),
    dict(tipo="fato", titulo="O SEGREDO", desenho=c_formigas, fundo=((110, 70, 60), (50, 25, 30)),
         fala="E o segredo do gosto ruim? Os cientistas acham que vem das formigas que ele come, com um dos venenos de inseto mais fortes do mundo."),
    dict(tipo="cta", titulo="GOSTO RUIM", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((255, 200, 130), (220, 130, 80)),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. Porque esse lagarto..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lagarto_p2.mp4"))
