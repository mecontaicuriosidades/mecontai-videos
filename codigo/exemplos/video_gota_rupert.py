"""Gota do Príncipe Rupert (CIÊNCIA BIZARRA #3). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "CIÊNCIA BIZARRA #3"
VIDRO = (170, 230, 255); VIDRO2 = (110, 190, 235); BRANCO = (255, 255, 255); FERRO = (120, 120, 135)
CABO = (150, 95, 50); QUENTE = (255, 140, 40); AGUA = (60, 130, 210)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def gota(d, cx, cy, s=1.0, cor=VIDRO, rabo=True):
    """Gota de vidro em forma de girino: cabeça redonda à esquerda, rabo fino para a direita."""
    if rabo:
        pts = [(cx + 60 * s, cy - 50 * s), (cx + 200 * s, cy - 18 * s), (cx + 330 * s, cy - 4 * s), (cx + 340 * s, cy + 2 * s),
               (cx + 200 * s, cy + 18 * s), (cx + 60 * s, cy + 50 * s)]
        d.polygon(pts, fill=cor, outline=O)
    d.ellipse([cx - 90 * s, cy - 90 * s, cx + 90 * s, cy + 90 * s], fill=cor, outline=O, width=6)
    d.ellipse([cx - 55 * s, cy - 60 * s, cx - 15 * s, cy - 25 * s], fill=BRANCO)
    d.arc([cx - 70 * s, cy - 70 * s, cx + 70 * s, cy + 70 * s], 20, 110, fill=VIDRO2, width=int(6 * s))


def martelo(d, cx, cy, ang):
    """Martelo girando em torno do fim do cabo (cx, cy)."""
    c, s_ = math.cos(ang), math.sin(ang)
    def p(x, y):
        return (cx + x * c - y * s_, cy + x * s_ + y * c)
    d.polygon([p(0, -14), p(300, -14), p(300, 14), p(0, 14)], fill=CABO, outline=O)
    d.polygon([p(270, -70), p(360, -70), p(360, 70), p(270, 70)], fill=FERRO, outline=O)


def g_explode(d, img, t, T):
    etiqueta(d)
    # bigorna
    d.polygon([(330, 1060), (800, 1060), (760, 1110), (370, 1110)], fill=FERRO, outline=O)
    d.rectangle([450, 1110, 680, 1240], fill=FERRO, outline=O, width=5)
    fase = (T % 1.2) / 1.2
    ang = -1.7 + 1.25 * ease(min(1, fase / 0.35)) if fase < 0.6 else -1.7 + 1.25 * (1 - ease((fase - 0.6) / 0.4))
    gota(d, 470, 1000, 0.75)
    martelo(d, 140, 1000, ang + 0.85)
    if 0.33 < fase < 0.5:
        rotulo(d, 470, 860, "TÓIN!", 54, AMARELO)
    # alicate perto do rabo + aviso
    d.line([(760, 1000), (900, 870)], fill=(200, 60, 60), width=16)
    d.line([(760, 1000), (930, 930)], fill=(200, 60, 60), width=16)
    rotulo(d, 860, 640, "NÃO CORTA!", 50, (255, 90, 90))
    seta(d, 860, 690, 780, 960, (255, 90, 90), 10)


def c_feita(d, img, t, T):
    selo(d)
    # balde de água com vidro quente pingando
    d.polygon([(260, 900), (820, 900), (760, 1250), (320, 1250)], fill=(200, 200, 210), outline=O)
    d.polygon([(280, 960), (800, 960), (762, 1230), (318, 1230)], fill=AGUA)
    for i in range(3):
        d.arc([360 + i * 140, 990, 460 + i * 140, 1030], 0, 180, fill=(180, 220, 255), width=5)
    f = (t % 1.6) / 1.6
    y = 560 + f * 520
    cor = QUENTE if y < 960 else VIDRO
    d.ellipse([515, y - 40, 565, y + 40], fill=cor, outline=O, width=5)
    if y > 960:
        rotulo(d, 640, 940, "TSSS!", 50, BRANCO)
        gota(d, 540, 1150, 0.4)
    # canudo/vara com vidro derretido
    d.line([(300, 520), (540, 540)], fill=FERRO, width=18)
    d.ellipse([500, 505, 580, 575], fill=QUENTE, outline=O, width=5)
    rotulo(d, 830, 620, "VIDRO QUENTE", 44, QUENTE)
    rotulo(d, 830, 800, "ÁGUA FRIA", 44, (150, 210, 255))


def c_po(d, img, t, T):
    selo(d)
    if t < 1.3:
        gota(d, 360, 850, 1.1)
        d.line([(700, 780), (760, 840), (700, 900)], fill=(200, 60, 60), width=16)
        rotulo(d, 720, 680, "CLIC", 52, AMARELO)
    else:
        k = min(1, (t - 1.3) / 1.2)
        for i in range(60):
            a = i * 2.39
            r = (40 + (i * 37) % 300) * ease(k)
            x = 400 + math.cos(a) * r
            y = 850 + math.sin(a) * r * 0.7
            sz = 6 + (i % 4) * 3
            d.polygon([(x - sz, y), (x, y - sz), (x + sz, y + sz * 0.6)], fill=VIDRO, outline=O)
        rotulo(d, 540, 1150, "PÓ DE VIDRO", 58, BRANCO)


def c_rapido(d, img, t, T):
    selo(d)
    # rachadura correndo pela gota e bala ficando para trás
    gota(d, 300, 700, 1.2)
    k = min(1, t / 1.8)
    xs = 300 + 400 * k
    pts = [(720, 700)]
    for i in range(8):
        x = 720 - (720 - 260) * min(1, k * 1.2) * (i + 1) / 8
        pts.append((x, 700 + 25 * math.sin(i * 2.2)))
    d.line(pts, fill=(40, 40, 60), width=7)
    # bala
    bx = 200 + 500 * k * 0.55
    d.rounded_rectangle([bx - 70, 1000, bx + 40, 1040], 18, fill=(210, 170, 80), outline=O, width=4)
    d.pieslice([bx + 10, 1000, bx + 80, 1040], 270, 90, fill=(210, 170, 80), outline=O)
    rotulo(d, bx, 1100, "BALA DE FUZIL", 40, (230, 200, 120))
    rotulo(d, 640, 900, "+5.000 KM/H", 62, AMARELO)


def c_cta(d, img, t, T):
    g_explode(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="EXPLODE!", titulo_y=400, desenho=g_explode, fundo=((70, 50, 120), (25, 15, 55)),
         fala="Essa gota de vidro aguenta martelada... mas explode se você quebrar o rabinho! E o último fato é o pior."),
    dict(tipo="fato", titulo="GOTA DE RUPERT", desenho=c_feita, fundo=((90, 50, 80), (35, 20, 40)),
         fala="É a gota do Príncipe Rupert: vidro derretido pingado na água fria. Segue a Maia, que piora: por fora, ela esfria na hora e fica espremida e superforte."),
    dict(tipo="fato", titulo="VIRA PÓ", desenho=c_po, fundo=((60, 60, 110), (20, 20, 50)),
         fala="Mas quebre a pontinha do rabo, e a gota inteira vira pó em microssegundos."),
    dict(tipo="fato", titulo="MAIS QUE BALA", desenho=c_rapido, fundo=((50, 40, 90), (15, 12, 40)),
         fala="A rachadura corre a mais de cinco mil quilômetros por hora. Mais rápido que uma bala de fuzil!"),
    dict(tipo="cta", titulo="EXPLODE!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((70, 50, 120), (25, 15, 55)),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. Porque essa gota..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "gota_rupert.mp4"))
