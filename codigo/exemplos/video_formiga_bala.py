"""Formiga-bala (BICHOS INSANOS #4). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, brilhos, O

SERIE = "BICHOS INSANOS #4"
CORPO = (70, 30, 20); CORPO2 = (110, 50, 30); BRILHO = (170, 90, 60)
FOLHA = (60, 150, 70); FOLHA2 = (40, 110, 55); PALHA = (210, 170, 100); PALHA2 = (160, 120, 60)
DOR = (255, 70, 40)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def formiga(d, cx, cy, s, T, dir=1, ferrao=False):
    """Formiga grande vista de lado, cabeça para o lado de dir."""
    X = lambda v: cx + v * s * dir
    Y = lambda v: cy + v * s
    # pernas
    for i, px in enumerate((-30, 10, 50)):
        b = 10 * math.sin(T * 10 + i * 2)
        d.line([(X(px), Y(10)), (X(px - 40 + b), Y(70)), (X(px - 60 + b), Y(130))], fill=O, width=int(9 * s))
    # abdômen, tórax, cabeça
    d.ellipse([X(-230) if dir > 0 else X(-60), Y(-70), X(-60) if dir > 0 else X(-230), Y(70)], fill=CORPO, outline=O, width=5)
    d.ellipse([X(-60) if dir > 0 else X(70), Y(-35), X(70) if dir > 0 else X(-60), Y(35)], fill=CORPO2, outline=O, width=5)
    d.ellipse([X(70) if dir > 0 else X(180), Y(-55), X(180) if dir > 0 else X(70), Y(45)], fill=CORPO, outline=O, width=5)
    d.ellipse([X(-190) if dir > 0 else X(-140), Y(-50), X(-140) if dir > 0 else X(-190), Y(-25)], fill=BRILHO)
    # olho bravo e mandíbulas
    ex, ey = X(140), Y(-15)
    d.ellipse([ex - 14 * s, ey - 14 * s, ex + 14 * s, ey + 14 * s], fill="white", outline=O, width=3)
    d.ellipse([ex - 6 * s, ey - 6 * s, ex + 6 * s, ey + 6 * s], fill=O)
    d.line([(X(115), Y(-40)), (X(165), Y(-28))], fill=O, width=int(7 * s))
    m = 8 * math.sin(T * 12)
    d.line([(X(175), Y(10)), (X(215), Y(30 + m))], fill=O, width=int(10 * s))
    d.line([(X(175), Y(25)), (X(210), Y(50 - m))], fill=O, width=int(10 * s))
    # antenas
    d.line([(X(150), Y(-50)), (X(190), Y(-130)), (X(250), Y(-150))], fill=O, width=int(7 * s))
    d.line([(X(130), Y(-50)), (X(150), Y(-140)), (X(210), Y(-175))], fill=O, width=int(7 * s))
    if ferrao:
        d.polygon([(X(-225), Y(-8)), (X(-275), Y(5)), (X(-225), Y(18))], fill=(30, 20, 20))


def relogio(d, x, y, r, T, giro):
    d.ellipse([x - r, y - r, x + r, y + r], fill="white", outline=O, width=7)
    for i in range(12):
        a = i * math.pi / 6
        d.line([(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82), (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)], fill=O, width=5)
    a = -math.pi / 2 + giro
    d.line([(x, y), (x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.75)], fill=DOR, width=9)
    a2 = -math.pi / 2 + giro / 12
    d.line([(x, y), (x + math.cos(a2) * r * 0.5, y + math.sin(a2) * r * 0.5)], fill=O, width=11)


def raios_dor(d, x, y, T, n=8, r0=60, r1=120):
    for i in range(n):
        a = i * 2 * math.pi / n + T
        k = 0.8 + 0.2 * math.sin(T * 9 + i)
        d.line([(x + math.cos(a) * r0, y + math.sin(a) * r0), (x + math.cos(a) * r1 * k, y + math.sin(a) * r1 * k)], fill=DOR, width=10)


def g_picada(d, img, t, T):
    etiqueta(d)
    d.rectangle([0, 1250, 1080, 1920], fill=FOLHA2)
    formiga(d, 470, 1010, 1.55, T, 1, ferrao=True)
    relogio(d, 860, 660, 105, T, T * 6)
    raios_dor(d, 140, 1000, T)


def mapa_amazonia(d, T):
    d.polygon([(180, 700), (520, 640), (900, 720), (960, 900), (820, 1080), (560, 1120), (300, 1040), (160, 880)],
              fill=FOLHA, outline=O, width=5)
    for i in range(6):  # rio
        d.line([(220 + i * 120, 880 + 20 * math.sin(i)), (340 + i * 120, 880 + 20 * math.sin(i + 1))], fill=(90, 160, 220), width=14)
    rotulo(d, 560, 1210, "AMAZÔNIA", 64, AMARELO)


def c_tiro(d, img, t, T):
    selo(d)
    if t < 2.4:
        mapa_amazonia(d, T)
        formiga(d, 560, 790, 0.45, T, 1)
        return
    d.rectangle([0, 1250, 1080, 1920], fill=FOLHA2)
    formiga(d, 360, 1080, 1.1, T, 1, ferrao=True)
    p = pop((t - 2.6) / 0.35) if t > 2.6 else 0
    if p > 0:
        r = int(150 * p)
        x, y = 800, 900
        pts = []
        for i in range(16):
            a = i * math.pi / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        d.polygon(pts, fill=AMARELO, outline=O)
        rotulo(d, x, y, "BANG!", int(60 * p), DOR)


def c_ranking(d, img, t, T):
    selo(d)
    k = ease(t / 2.4)
    alturas = (120, 230, 350, 480)
    for i, h in enumerate(alturas):
        x = 190 + i * 230
        hh = h * min(1, k * 1.3 - i * 0.15) if k * 1.3 - i * 0.15 > 0 else 0
        cor = (255, 200 - i * 45, 60)
        d.rectangle([x - 80, 1150 - hh, x + 80, 1150], fill=cor, outline=O, width=5)
        rotulo(d, x, 1200, str(i + 1) if i < 3 else "4+", 52, "white", traduzir=False)
    if k > 0.9:
        formiga(d, 880, 600, 0.5, T, -1)
        brilhos(d, 880, 600, 150, T)
        rotulo(d, 360, 580, "DOR MÁXIMA", 64, AMARELO)


def luva(d, x, y, T, s=1.0):
    d.rounded_rectangle([x - 150 * s, y - 120 * s, x + 150 * s, y + 260 * s], int(80 * s), fill=PALHA, outline=O, width=6)
    for j in range(4):  # dedos
        fx = x - 120 * s + j * 80 * s
        d.rounded_rectangle([fx - 32 * s, y - 280 * s, fx + 32 * s, y - 80 * s], int(30 * s), fill=PALHA, outline=O, width=6)
    for i in range(8):  # trama
        yy = y - 80 * s + i * 42 * s
        d.line([(x - 140 * s, yy), (x + 140 * s, yy)], fill=PALHA2, width=5)
    # cabecinhas de formiga saindo da trama
    for i in range(9):
        fx = x - 110 * s + (i % 3) * 110 * s + 8 * math.sin(T * 8 + i)
        fy = y - 40 * s + (i // 3) * 100 * s
        d.ellipse([fx - 18 * s, fy - 14 * s, fx + 18 * s, fy + 14 * s], fill=CORPO, outline=O, width=3)
        d.line([(fx, fy - 12 * s), (fx - 18 * s, fy - 40 * s)], fill=O, width=4)
        d.line([(fx, fy - 12 * s), (fx + 18 * s, fy - 40 * s)], fill=O, width=4)


def c_luva(d, img, t, T):
    selo(d)
    luva(d, 400, 1050, T, 1.3)
    raios_dor(d, 400, 1050, T, 10, 260, 330)
    if t > 1.6:
        relogio(d, 860, 720, 90, T, min(1, (t - 1.6) / 2.5) * math.pi * 1.0)
        rotulo(d, 860, 870, "10 MIN", 56, AMARELO)


def c_cta(d, img, t, T):
    g_picada(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="24 HORAS!", titulo_y=400, desenho=g_picada, fundo=((90, 160, 90), (30, 80, 40)),
         fala="Essa formiga tem uma picada que dói por até vinte e quatro horas! E o último fato é o pior."),
    dict(tipo="fato", titulo="FORMIGA-BALA", desenho=c_tiro, fundo=((110, 180, 110), (40, 100, 60)),
         fala="É a formiga-bala, da Amazônia, com até três centímetros. Segue a Maia, que piora: o nome é porque a dor parece um tiro."),
    dict(tipo="fato", titulo="NO TOPO", desenho=c_ranking, fundo=((80, 60, 140), (35, 25, 80)),
         fala="Num ranking famoso de dor de picadas de insetos, ela ficou lá no topo."),
    dict(tipo="fato", titulo="O RITUAL", desenho=c_luva, fundo=((200, 120, 70), (120, 60, 35)),
         fala="E no Amazonas, meninos do povo Sateré-Mawé vestem luvas cheias dessas formigas, por uns dez minutos, num ritual."),
    dict(tipo="cta", titulo="24 HORAS!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((90, 160, 90), (30, 80, 40)),
         fala="Segue a Maia: amanhã tem mais Bichos Insanos. Porque essa formiga..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "formiga_bala.mp4"))
