"""Besouro-bombardeiro, Parte 1 (BICHOS INSANOS #12). Formato v3 + ESTRATÉGIA DA SEMANA 23/11
(20–28 s, fato chocante no 1º segundo, 1 frase de opinião da MAIA). Convite sem a palavra proibida.
Fatos (National Geographic; Arndt et al., Science 2015; Eisner): o besouro-bombardeiro (Brachinini) guarda
hidroquinonas e água oxigenada (peróxido de hidrogênio) em reservatórios; ao se defender, mistura tudo numa câmara
com enzimas e a reação explode e solta um jato a ~100 °C; o jato sai em pulsos (~500 por segundo) e a ponta do
abdômen gira, então ele mira para trás, para os lados e até por cima das costas."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, termometro, O
import idioma

SERIE = "BICHOS INSANOS #12"
CABECA = (235, 120, 40); ASA = (40, 60, 120); ASA2 = (80, 110, 190)
PERNA = (200, 95, 30); JATO = (255, 245, 200); JATO2 = (255, 200, 90)
TERRA1 = (70, 45, 30); TERRA2 = (25, 15, 10)


def etiqueta(d, parte="P1"):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def besouro(d, cx, cy, s=1.0, T=0.0, lado=1):
    """Besouro visto de lado: cabeça laranja, asas azul-escuras. lado=1 olha pra direita (bumbum à esquerda)."""
    L = lado
    # pernas
    for k, dx in enumerate((-60, 0, 60)):
        mex = math.sin(T * 10 + k * 2) * 8 * s
        x0 = cx + dx * s
        d.line([(x0, cy + 30 * s), (x0 + 25 * s * L + mex, cy + 85 * s), (x0 + 45 * s * L + mex, cy + 95 * s)],
               fill=PERNA, width=max(3, int(9 * s)))
    # corpo (asas)
    d.ellipse([cx - 140 * s, cy - 75 * s, cx + 90 * s, cy + 55 * s], fill=ASA, outline=O, width=max(3, int(7 * s)))
    d.arc([cx - 120 * s, cy - 60 * s, cx + 70 * s, cy + 20 * s], 200, 330, fill=ASA2, width=max(2, int(6 * s)))
    d.line([(cx - 130 * s, cy - 10 * s), (cx + 85 * s, cy - 10 * s)], fill=O, width=max(2, int(4 * s)))
    # cabeça e tórax laranja
    hx = cx + 110 * s * L
    d.ellipse([hx - 50 * s, cy - 50 * s, hx + 50 * s, cy + 40 * s], fill=CABECA, outline=O, width=max(3, int(6 * s)))
    hx2 = cx + 165 * s * L
    d.ellipse([hx2 - 35 * s, cy - 35 * s, hx2 + 35 * s, cy + 30 * s], fill=CABECA, outline=O, width=max(3, int(6 * s)))
    # olho e antenas
    ex = hx2 + 12 * s * L
    d.ellipse([ex - 11 * s, cy - 20 * s, ex + 11 * s, cy + 2 * s], fill=(255, 255, 255), outline=O, width=3)
    d.ellipse([ex - 4 * s + 3 * s * L, cy - 13 * s, ex + 4 * s + 3 * s * L, cy - 5 * s], fill=O)
    for k in (0, 1):
        a = -0.6 - k * 0.5 + math.sin(T * 3 + k) * 0.1
        d.line([(hx2 + 20 * s * L, cy - 25 * s), (hx2 + (20 + math.cos(a) * 110) * s * L, cy - 25 * s + math.sin(a) * 110 * s)],
               fill=PERNA, width=max(2, int(5 * s)))


def jato(d, x, y, ang, s=1.0, T=0.0, comp=1.0):
    """Jato em pulsos (nuvenzinhas que andam) saindo de (x, y) na direção ang (radianos)."""
    n = 7
    for i in range(n):
        f = ((T * 2.5 + i / n) % 1.0) * comp
        r = (18 + 50 * f) * s
        px = x + math.cos(ang) * 380 * f * s
        py = y + math.sin(ang) * 380 * f * s
        cor = JATO if i % 2 else JATO2
        d.ellipse([px - r, py - r, px + r, py + r], fill=cor, outline=O, width=max(2, int(4 * s)))


def chao(d):
    d.rectangle([0, 1100, 1080, 1290], fill=(95, 65, 40))
    for i in range(14):
        x = i * 80 + 20
        d.line([(x, 1100), (x + 20, 1070)], fill=(90, 170, 70), width=6)


def g_jato(d, img, t, T, label=True):
    etiqueta(d)
    chao(d)
    besouro(d, 680, 980, 1.25, T, lado=1)
    jato(d, 500, 960, math.pi + 0.15, 1.1, T)
    brilhos(d, 260, 900, 110, T, 8, AMARELO)
    if label:
        kk = pop(min(1, max(0, t - 0.3) / 0.5))
        if kk > 0.05:
            rotulo(d, 260, 680, "100 °C", int(86 * kk) + 1, (255, 90, 60), traduzir=False)
            rotulo(d, 740, 1200, "PELO BUMBUM!", int(50 * kk) + 1, AMARELO)


def c_nome(d, img, t, T):
    selo(d)
    k = ease(t / 0.7)
    d.ellipse([190, 620, 890, 1200], outline=CIANO, width=10)
    besouro(d, 540 - 60 * (1 - k), 900, 1.55, T, lado=1)
    kk = pop(min(1, max(0, t - 0.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1250, "BESOURO-BOMBARDEIRO", int(52 * kk) + 1, AMARELO)


def c_quimica(d, img, t, T):
    selo(d)
    # dois frascos que despejam numa câmara: explosão
    k = ease(t / 1.0)
    d.rounded_rectangle([110, 560, 330, 820], 30, fill=(250, 230, 120), outline=O, width=7)
    d.rounded_rectangle([670, 560, 870, 820], 30, fill=(150, 220, 255), outline=O, width=7)
    rotulo(d, 220, 860, "HIDROQUINONA", 34, (250, 230, 120))
    rotulo(d, 770, 860, "ÁGUA OXIGENADA", 32, (150, 220, 255))
    seta(d, 300, 900, 300 + 140 * k, 960 + 60 * k, AMARELO, 12)
    seta(d, 780, 900, 780 - 140 * k, 960 + 60 * k, AMARELO, 12)
    cx, cy = 540, 1090
    d.ellipse([cx - 120, cy - 100, cx + 120, cy + 100], fill=(120, 60, 40), outline=O, width=8)
    if t > 1.0:
        kk = pop(min(1, (t - 1.0) / 0.4))
        r = 150 * kk
        pts = []
        for i in range(16):
            a = i / 16 * 6.283 + T
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=(255, 210, 60), outline=O)
        rotulo(d, cx, cy, "BUM!", int(70 * kk) + 1, (255, 70, 50))
    termometro(d, 1000, 1060, min(1.0, max(0.0, (t - 1.0) / 1.0)), h=300)
    rotulo(d, 860, 1240, "100 °C", 50, (255, 90, 60), traduzir=False)


def c_metralhadora(d, img, t, T):
    selo(d)
    cx, cy = 540, 860
    besouro(d, cx, cy, 1.0, T, lado=1)
    # a ponta gira: jato muda de direção
    ang = math.pi + math.sin(T * 1.6) * 1.3
    jato(d, cx - 130, cy - 10, ang, 0.8, T)
    contador(d, 540, 1120, 500, t, 1.4, 110, "", AMARELO)
    kk = pop(min(1, max(0, t - 1.0) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1210, "ESTOUROS POR SEGUNDO", int(42 * kk) + 1, (255, 255, 255))
        rotulo(d, 780, 640, "MIRA PRA TODO LADO", int(40 * kk) + 1, CIANO)


def c_cta(d, img, t, T):
    g_jato(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="FERVENDO!", titulo_y=400, desenho=g_jato, fundo=(TERRA1, TERRA2),
         fala="Esse besouro dispara um jato fervendo pelo bumbum! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="BOMBARDEIRO", desenho=c_nome, fundo=((60, 40, 90), (15, 10, 30)),
         fala="É o besouro-bombardeiro. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="EXPLOSÃO", desenho=c_quimica, fundo=((90, 30, 30), (25, 8, 8)),
         fala="lá dentro, ele mistura dois químicos, e eles explodem a cem graus."),
    dict(tipo="fato", titulo="RATATATÁ", desenho=c_metralhadora, fundo=((30, 70, 60), (8, 20, 18)),
         fala="São uns quinhentos estouros por segundo, e ele mira pra todo lado. Uma metralhadora de bumbum!"),
    dict(tipo="cta", titulo="FERVENDO!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=(TERRA1, TERRA2),
         fala="Segue a Maia pra ver a parte dois às seis da tarde, ainda mais louca! Tudo por causa desse besouro..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "besouro_p1.mp4"))
