"""Salar de Uyuni, Bolívia (LUGARES MORTAIS #6). Formato v3 + estratégia 23/11 (abertura com pergunta)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "LUGARES MORTAIS #6"
CEU1 = (90, 170, 240); CEU2 = (190, 225, 255); SAL = (245, 245, 250); SAL2 = (215, 220, 230)
NUVEM = (255, 255, 255); ROUPA = (230, 70, 90); PELE = (240, 190, 150)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def ceu_espelho(d, T, y0=500, hz=880, y1=1260):
    """Céu em cima e o mesmo céu refletido embaixo do horizonte."""
    for y in range(y0, hz, 6):
        k = (y - y0) / (hz - y0)
        c = tuple(int(CEU1[i] + (CEU2[i] - CEU1[i]) * k) for i in range(3))
        d.rectangle([0, y, 1080, y + 6], fill=c)
        yr = 2 * hz - y
        if yr < y1:
            d.rectangle([0, yr - 6, 1080, yr], fill=c)
    d.line([(0, hz), (1080, hz)], fill=(255, 255, 255), width=3)
    for i, (x, y, r) in enumerate(((200, 620, 60), (700, 580, 80), (950, 700, 50))):
        x = (x + T * 15) % 1200 - 60
        for dx, dy, rr in ((0, 0, r), (r * 0.8, 10, r * 0.7), (-r * 0.8, 12, r * 0.65)):
            for yy in (y + dy, 2 * hz - y - dy):
                d.ellipse([x + dx - rr, yy - rr * 0.6, x + dx + rr, yy + rr * 0.6], fill=NUVEM)


def pessoa(d, x, hz, T, s=1.0, refl=True):
    passo = math.sin(T * 4) * 14 * s
    for sinal in ((1, -1) if refl else (1,)):
        def P(px, py):
            return (x + px * s, hz - sinal * py * s)
        d.line([P(0, 0), P(-12 + passo / s, 0), ], fill=O, width=1)
        d.line([P(0, 90), P(-18, 0)], fill=O, width=int(14 * s))
        d.line([P(0, 90), P(18, 0)], fill=O, width=int(14 * s))
        d.polygon([P(-28, 90), P(28, 90), P(22, 190), P(-22, 190)], fill=ROUPA, outline=O)
        d.line([P(-22, 180), P(-50, 120 + passo / s)], fill=O, width=int(12 * s))
        d.line([P(22, 180), P(50, 120 - passo / s)], fill=O, width=int(12 * s))
        cx, cy = P(0, 225)
        d.ellipse([cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s], fill=PELE, outline=O, width=4)


def g_espelho(d, img, t, T):
    etiqueta(d)
    ceu_espelho(d, T, 500, 880, 1260)
    pessoa(d, 560, 880, T, 1.3)
    k = pop(min(1, max(0, t - 0.4) / 0.5))
    if k > 0.05:
        rotulo(d, 880, 1060, "REFLEXO", int(40 * k) + 1, (255, 255, 255))


def c_tamanho(d, img, t, T):
    # salar branco visto de cima + 2 "Distritos Federais" encaixados
    d.polygon([(120, 620), (500, 520), (900, 600), (960, 900), (760, 1150), (300, 1120), (110, 900)], fill=SAL, outline=O)
    for i in range(14):
        x = 180 + (i * 61) % 720; y = 620 + (i * 113) % 460
        d.polygon([(x, y), (x + 40, y + 10), (x + 30, y + 45), (x - 8, y + 38)], outline=SAL2)
    k = ease(min(1, max(0, t - 0.6) / 0.8))
    for j, (x0, y0) in enumerate(((240, 700), (520, 800))):
        if k > 0:
            w, h = 260 * k, 160 * k
            d.rectangle([x0, y0, x0 + w, y0 + h], fill=(80, 190, 110), outline=O, width=5)
            if k > 0.9:
                rotulo(d, x0 + w / 2, y0 + h / 2, "DF", 54, (255, 255, 255))
    rotulo(d, 540, 1200, "+10 MIL KM²", 60, AMARELO)
    rotulo(d, 540, 500, "BOLÍVIA · 3.650 M", 44, (255, 255, 255))


def c_chuva(d, img, t, T):
    ceu_espelho(d, T, 500, 820, 1150)
    # gotas caindo
    for i in range(22):
        x = (i * 97) % 1080; y = 500 + ((i * 131 + T * 600) % 320)
        d.line([(x, y), (x - 6, y + 26)], fill=(255, 255, 255), width=4)
    # corte lateral: sal + lâmina de água
    d.rectangle([0, 1150, 1080, 1250], fill=SAL, outline=O, width=4)
    d.rectangle([0, 1130, 1080, 1150], fill=(120, 200, 255))
    rotulo(d, 300, 1200, "SAL", 44, AMARELO)
    rotulo(d, 780, 1100, "ÁGUA FININHA", 40, (255, 255, 255))


def satelite(d, x, y, T):
    d.rectangle([x - 40, y - 30, x + 40, y + 30], fill=(200, 200, 210), outline=O, width=5)
    for sx in (-1, 1):
        d.rectangle([min(x + sx * 50, x + sx * 170), y - 22, max(x + sx * 50, x + sx * 170), y + 22], fill=(40, 80, 170), outline=O, width=4)
        for k in range(3):
            xx = x + sx * (70 + k * 35)
            d.line([(xx, y - 20), (xx, y + 20)], fill=(150, 190, 255), width=3)


def c_plano(d, img, t, T):
    d.rectangle([0, 1000, 1080, 1250], fill=SAL)
    d.line([(0, 1000), (1080, 1000)], fill=O, width=6)
    sx = 200 + (t * 120) % 700
    satelite(d, sx, 560, T)
    # feixe medindo o chão
    if (T * 3) % 1 < 0.7:
        d.line([(sx, 600), (sx, 995)], fill=(255, 80, 80), width=6)
        d.ellipse([sx - 16, 984, sx + 16, 1016], fill=(255, 80, 80))
    # régua de altura quase reta
    pts = [(x, 1000 - 3 * math.sin(x / 90)) for x in range(0, 1081, 30)]
    d.line(pts, fill=AMARELO, width=6)
    rotulo(d, 540, 1100, "MENOS DE 1 METRO", 52, AMARELO)
    rotulo(d, 540, 1170, "DE DIFERENÇA", 44, (255, 255, 255))


def c_cta(d, img, t, T):
    etiqueta(d)
    ceu_espelho(d, T, 560, 900, 1260)
    pessoa(d, 560, 900, T, 0.9)


CENAS = [
    dict(tipo="gancho", titulo="ESPELHO!", titulo_y=400, desenho=g_espelho, fundo=((40, 90, 160), (15, 35, 80)),
         fala="Você andaria em cima do céu? Nesse deserto, parece que dá."),
    dict(tipo="fato", titulo="UYUNI", desenho=c_tamanho, fundo=((60, 110, 170), (20, 40, 80)),
         fala="Salar de Uyuni, na Bolívia: o maior deserto de sal do mundo. Quase dois Distritos Federais!"),
    dict(tipo="fato", titulo="ÁGUA + SAL", desenho=c_chuva, fundo=((50, 100, 160), (20, 40, 80)),
         fala="Quando chove, uma água fininha cobre o sal e vira um espelho gigante. Eu ficaria tonta!"),
    dict(tipo="fato", titulo="LISO DEMAIS", desenho=c_plano, fundo=((20, 30, 70), (5, 10, 30)),
         fala="É tão plano que satélites usam ele pra calibrar medidores: menos de um metro de diferença!"),
    dict(tipo="cta", titulo="ESPELHO!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 90, 160), (15, 35, 80)),
         fala="Segue a Maia: amanhã tem mais Lugares Mortais. E aí..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "uyuni.mp4"))
