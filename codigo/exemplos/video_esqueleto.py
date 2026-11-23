"""Esqueleto novo a cada ~10 anos (CIÊNCIA BIZARRA #4). Formato v3 + estratégia 23/11 (abertura com número)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "CIÊNCIA BIZARRA #4"
OSSO = (250, 245, 225); VELHO = (170, 160, 140); ROSA = (255, 120, 160); VERDEC = (90, 220, 140)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def osso(d, a, b, w, cor):
    d.line([a, b], fill=O, width=int(w + 10))
    d.line([a, b], fill=cor, width=int(w))
    for (x, y) in (a, b):
        r = w * 0.85
        d.ellipse([x - r, y - r, x + r, y + r], fill=cor, outline=O, width=4)


def esqueleto(d, cx, cy, s, T, novo=1.0, danca=True):
    """novo: 0 = osso velho (cinza), 1 = osso novo (branco); troca de baixo para cima."""
    def cor(y):
        lim = cy + 330 * s - novo * 700 * s
        return OSSO if y > lim else VELHO
    sw = math.sin(T * 3) * 0.25 if danca else 0
    # pernas
    for sx in (-1, 1):
        q = (cx + sx * 45 * s, cy + 90 * s); j = (cx + sx * 60 * s, cy + 220 * s); p = (cx + sx * 60 * s, cy + 330 * s)
        osso(d, q, j, 22 * s, cor(j[1])); osso(d, j, p, 20 * s, cor(p[1]))
    # bacia
    d.ellipse([cx - 80 * s, cy + 50 * s, cx + 80 * s, cy + 120 * s], fill=cor(cy + 90 * s), outline=O, width=5)
    # coluna e costelas
    for k in range(7):
        y = cy - 200 * s + k * 36 * s
        d.ellipse([cx - 16 * s, y - 12 * s, cx + 16 * s, y + 12 * s], fill=cor(y), outline=O, width=4)
    for k in range(4):
        y = cy - 170 * s + k * 40 * s
        d.arc([cx - 95 * s, y - 30 * s, cx + 95 * s, y + 50 * s], 200, 340, fill=O, width=int(16 * s))
        d.arc([cx - 95 * s, y - 30 * s, cx + 95 * s, y + 50 * s], 200, 340, fill=cor(y), width=int(9 * s))
    # braços (acenando)
    for sx in (-1, 1):
        o = (cx + sx * 85 * s, cy - 175 * s)
        a = sw * sx
        c = (o[0] + sx * math.cos(0.9 + a) * 120 * s, o[1] + math.sin(0.9 + a) * 120 * s)
        m = (c[0] + sx * 20 * s, c[1] + 110 * s)
        osso(d, o, c, 18 * s, cor(c[1])); osso(d, c, m, 16 * s, cor(m[1]))
    # crânio
    hy = cy - 270 * s
    d.ellipse([cx - 70 * s, hy - 75 * s, cx + 70 * s, hy + 60 * s], fill=cor(hy), outline=O, width=6)
    for sx in (-1, 1):
        d.ellipse([cx + sx * 28 * s - 18 * s, hy - 25 * s, cx + sx * 28 * s + 18 * s, hy + 10 * s], fill=O)
    d.rectangle([cx - 30 * s, hy + 30 * s, cx + 30 * s, hy + 52 * s], fill=OSSO, outline=O, width=3)
    for k in range(1, 4):
        d.line([(cx - 30 * s + k * 15 * s, hy + 30 * s), (cx - 30 * s + k * 15 * s, hy + 52 * s)], fill=O, width=3)


def g_novo(d, img, t, T):
    etiqueta(d)
    novo = (T * 0.4) % 1.2
    esqueleto(d, 600, 900, 1.0, T, min(1, novo))
    brilhos(d, 600, 640 + 600 * (1 - min(1, novo)), 110, T, 6, AMARELO)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 900, 620, "10 ANOS", int(56 * k) + 1, AMARELO)


def celula_come(d, x, y, r, T, cor, boca=True):
    a = 25 + 20 * abs(math.sin(T * 6)) if boca else 0
    d.pieslice([x - r, y - r, x + r, y + r], a, 360 - a, fill=cor, outline=O, width=5)
    d.ellipse([x + r * 0.1, y - r * 0.55, x + r * 0.35, y - r * 0.3], fill=O)


def c_vivo(d, img, t, T):
    # pedaço de osso em corte: buracos sendo cavados e tapados
    d.rounded_rectangle([90, 560, 990, 1120], 60, fill=OSSO, outline=O, width=7)
    for i in range(6):
        x = 200 + i * 135
        d.ellipse([x - 30, 680, x + 30, 740], fill=(230, 220, 190))
    fase = (t * 0.6) % 1
    xc = 260 + 560 * fase
    d.ellipse([140, 820, xc, 980], fill=(150, 60, 70), outline=O, width=4)  # buraco cavado
    celula_come(d, xc + 40, 900, 70, T, ROSA)
    # construtoras tapando atrás
    for j in range(3):
        x = 160 + j * 90
        if x < xc - 60:
            d.ellipse([x - 40, 860, x + 40, 940], fill=OSSO, outline=O, width=3)
            celula_come(d, x, 1030, 38, T + j, VERDEC, boca=False)
    rotulo(d, 760, 640, "CAVA OSSO VELHO", 40, ROSA)
    rotulo(d, 330, 1180, "TAPA COM OSSO NOVO", 40, VERDEC)


def casa(d, cx, cy, T, k):
    d.rectangle([cx - 200, cy - 150, cx + 200, cy + 150], fill=(250, 220, 170), outline=O, width=7)
    d.polygon([(cx - 240, cy - 150), (cx, cy - 330), (cx + 240, cy - 150)], fill=(210, 90, 70), outline=O)
    d.rectangle([cx - 50, cy + 20, cx + 50, cy + 150], fill=(120, 80, 50), outline=O, width=5)
    # tijolo sendo trocado
    for i in range(10):
        x = cx - 180 + (i % 5) * 72; y = cy - 120 + (i // 5) * 60
        trocado = i < int(k * 10)
        d.rectangle([x, y, x + 60, y + 40], fill=(255, 255, 255) if trocado else (200, 140, 100), outline=O, width=3)
    # Maia-mini dentro (janela)
    d.ellipse([cx + 90, cy + 30, cx + 170, cy + 110], fill=(150, 220, 255), outline=O, width=5)


def c_reforma(d, img, t, T):
    k = min(1, t / 3)
    casa(d, 540, 900, T, k * 0.1 * 10 if False else k)
    rotulo(d, 540, 520, "~10% POR ANO", 60, AMARELO)
    rotulo(d, 540, 1170, "SEM SAIR DE CASA", 44, (255, 255, 255))


def c_espaco(d, img, t, T):
    # astronauta flutuando, osso encolhendo
    x, y = 360, 860 + 20 * math.sin(T * 1.5)
    ang = T * 0.4
    d.ellipse([x - 110, y - 180, x + 110, y + 40], fill=(240, 240, 245), outline=O, width=7)
    d.ellipse([x - 70, y - 140, x + 70, y - 20], fill=(40, 60, 110), outline=O, width=5)
    d.rounded_rectangle([x - 120, y + 30, x + 120, y + 260], 40, fill=(240, 240, 245), outline=O, width=7)
    for sx in (-1, 1):
        d.line([(x + sx * 110, y + 80), (x + sx * 200, y + 20 + 30 * math.sin(T * 2 + sx))], fill=O, width=48)
        d.line([(x + sx * 110, y + 80), (x + sx * 200, y + 20 + 30 * math.sin(T * 2 + sx))], fill=(240, 240, 245), width=36)
    for i in range(12):
        sx = (i * 211) % 1080; sy = 520 + (i * 97) % 700
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255))
    esc = 1 - 0.25 * ease(t / 3)
    osso(d, (720, 800), (720 + 200 * esc, 800 + 200 * esc), 40 * esc, OSSO)
    rotulo(d, 800, 1120, "-1% POR MÊS", 60, (255, 110, 110))


def c_cta(d, img, t, T):
    etiqueta(d)
    esqueleto(d, 600, 940, 0.95, T, 1.0)


CENAS = [
    dict(tipo="gancho", titulo="OSSO NOVO", titulo_y=400, desenho=g_novo, fundo=((50, 30, 90), (18, 10, 40)),
         fala="A cada dez anos, mais ou menos, você ganha um esqueleto quase todo novo!"),
    dict(tipo="fato", titulo="OSSO VIVO", desenho=c_vivo, fundo=((70, 30, 60), (25, 10, 25)),
         fala="Osso é vivo: umas células cavam o osso velho, e outras tapam com osso novo."),
    dict(tipo="fato", titulo="REFORMA", desenho=c_reforma, fundo=((40, 60, 100), (15, 20, 40)),
         fala="Num adulto, uns dez por cento por ano. É reformar a casa sem sair dela!"),
    dict(tipo="fato", titulo="NO ESPAÇO", desenho=c_espaco, fundo=((10, 10, 40), (0, 0, 10)), estrelas=True,
         fala="E o pior: no espaço, astronautas perdem cerca de um por cento de massa óssea por mês!"),
    dict(tipo="cta", titulo="OSSO NOVO", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((50, 30, 90), (18, 10, 40)),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. Então lembra..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "esqueleto.mp4"))
