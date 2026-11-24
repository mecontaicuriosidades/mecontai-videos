"""O corpo humano brilha no escuro (CIÊNCIA BIZARRA #5). Formato v3 + ESTRATÉGIA DA SEMANA 23/11.
Fatos (Kobayashi et al., PLoS ONE 2009): câmeras ultrassensíveis no escuro total filmaram a emissão
espontânea de luz do corpo; ela é cerca de 1.000 vezes mais fraca do que o olho consegue perceber;
o rosto (bochechas, testa, pescoço) brilha mais; ritmo diário: mais forte por volta das 16h e mais
fraco por volta das 10h; vem de reações químicas do metabolismo (radicais livres)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "CIÊNCIA BIZARRA #5"
ESC1 = (10, 8, 25); ESC2 = (0, 0, 5)
PELE = (240, 200, 165); PELE2 = (200, 150, 120); CABELO = (60, 40, 30)
GLOW = (120, 255, 200)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def aura(d, cx, cy, r, T, cor=GLOW, forca=1.0):
    for i in range(6, 0, -1):
        rr = r + i * 18 + math.sin(T * 2 + i) * 6
        a = int(14 * forca * (7 - i) / 6) + 4
        c = tuple(int(v * a / 60) for v in cor)
        d.ellipse([cx - rr, cy - rr * 1.15, cx + rr, cy + rr * 1.15], outline=c, width=18)


def rosto(d, cx, cy, s, T, brilho=1.0, bochechas=False):
    """Pessoa (silhueta de busto) com rosto; brilho 0..1 mistura a pele com verde-brilho."""
    def mix(c):
        return tuple(int(c[i] * (1 - 0.5 * brilho) + GLOW[i] * 0.5 * brilho) for i in range(3))
    d.rounded_rectangle([cx - 230 * s, cy + 170 * s, cx + 230 * s, cy + 420 * s], radius=int(90 * s), fill=(50, 60, 90), outline=O, width=6)
    d.rectangle([cx - 50 * s, cy + 110 * s, cx + 50 * s, cy + 190 * s], fill=mix(PELE2), outline=O, width=5)
    d.ellipse([cx - 150 * s, cy - 190 * s, cx + 150 * s, cy + 170 * s], fill=mix(PELE), outline=O, width=7)
    d.chord([cx - 160 * s, cy - 210 * s, cx + 160 * s, cy + 30 * s], 180, 360, fill=CABELO, outline=O)
    # olhos fechados (dormindo no escuro) e boca
    for sx in (-1, 1):
        d.arc([cx + sx * 60 * s - 30 * s, cy - 10 * s, cx + sx * 60 * s + 30 * s, cy + 25 * s], 20, 160, fill=O, width=6)
    d.arc([cx - 35 * s, cy + 60 * s, cx + 35 * s, cy + 100 * s], 20, 160, fill=O, width=6)
    if bochechas:
        for sx in (-1, 1):
            x, y = cx + sx * 85 * s, cy + 55 * s
            d.ellipse([x - 40 * s, y - 28 * s, x + 40 * s, y + 28 * s], fill=(160, 255, 210))
        d.ellipse([cx - 70 * s, cy - 90 * s, cx + 70 * s, cy - 45 * s], fill=(140, 245, 200))


def g_brilha(d, img, t, T, label=True):
    etiqueta(d)
    b = 0.6 + 0.4 * math.sin(T * 2.5)
    aura(d, 620, 880, 190, T, forca=b)
    rosto(d, 620, 880, 1.0, T, 0.8)
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if label and k > 0.05:
        rotulo(d, 230, 700, "LUZ!", int(70 * k) + 1, GLOW)
        seta(d, 280, 740, 420, 820, GLOW, 10)


def camera(d, x, y, T):
    d.rounded_rectangle([x - 120, y - 80, x + 120, y + 80], radius=16, fill=(70, 70, 85), outline=O, width=6)
    d.ellipse([x + 60, y - 60, x + 180, y + 60], fill=(40, 40, 50), outline=O, width=6)
    d.ellipse([x + 95, y - 25, x + 145, y + 25], fill=(90, 160, 255))
    on = int(T * 3) % 2
    d.ellipse([x - 100, y - 60, x - 76, y - 36], fill=(255, 60, 60) if on else (90, 20, 20))


def c_japao(d, img, t, T):
    selo(d)
    camera(d, 220, 800, T)
    rosto(d, 760, 820, 0.75, T, 0.35)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 220, 640, "JAPÃO · 2009", int(46 * k) + 1, AMARELO)
        rotulo(d, 540, 1180, "ESCURO TOTAL", int(50 * k) + 1, (255, 255, 255))


def c_mil(d, img, t, T):
    selo(d)
    # olho humano e um brilho minúsculo
    cx, cy = 300, 820
    d.ellipse([cx - 170, cy - 95, cx + 170, cy + 95], fill=(245, 245, 240), outline=O, width=7)
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(110, 80, 50), outline=O, width=5)
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=O)
    rotulo(d, cx, cy + 170, "NÃO VÊ", 50, (255, 90, 90))
    p = 3 + 2 * math.sin(T * 6)
    d.ellipse([800 - p, 820 - p, 800 + p, 820 + p], fill=GLOW)
    rotulo(d, 540, 560, "JAPÃO · 2009", 46, AMARELO)
    contador(d, 800, 700, 1000, t, 1.6, 84, "x")
    k = pop(min(1, max(0, t - 1.0) / 0.5))
    if k > 0.05:
        rotulo(d, 800, 960, "MAIS FRACA", int(48 * k) + 1, GLOW)


def c_rosto(d, img, t, T):
    selo(d)
    aura(d, 540, 860, 160, T, forca=0.7)
    rosto(d, 540, 860, 0.95, T, 0.25, bochechas=True)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 200, 640, "TESTA", int(48 * k) + 1, GLOW)
        seta(d, 240, 680, 450, 770, GLOW, 9)
        rotulo(d, 890, 1010, "BOCHECHAS", int(48 * k) + 1, GLOW)
        seta(d, 860, 970, 680, 920, GLOW, 9)


def relogio(d, cx, cy, r, hora, cor):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 245, 250), outline=O, width=7)
    for i in range(12):
        a = i * math.pi / 6
        d.line([(cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8), (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)], fill=O, width=5)
    a = (hora % 12) / 12 * 2 * math.pi - math.pi / 2
    d.line([(cx, cy), (cx + math.cos(a) * r * 0.5, cy + math.sin(a) * r * 0.5)], fill=O, width=10)
    d.line([(cx, cy), (cx, cy - r * 0.75)], fill=O, width=6)
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], outline=cor, width=10)


def c_relogio(d, img, t, T):
    selo(d)
    relogio(d, 280, 760, 140, 10, (120, 120, 140))
    rotulo(d, 280, 960, "10H: FRACO", 46, (180, 180, 200))
    k = pop(min(1, max(0, t - 0.6) / 0.5))
    if k > 0.05:
        b = 0.7 + 0.3 * math.sin(T * 4)
        aura(d, 800, 760, 120, T, forca=b)
        relogio(d, 800, 760, 140, 16, GLOW)
        rotulo(d, 800, 960, "16H: FORTE", int(46 * k) + 1, GLOW)
    rotulo(d, 540, 1180, "MUDA COM A HORA", 48, AMARELO)


def c_cta(d, img, t, T):
    g_brilha(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="BRILHA!", titulo_y=400, desenho=g_brilha, fundo=(ESC1, ESC2),
         fala="Seu corpo brilha no escuro. De verdade! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="MIL VEZES", desenho=c_mil, fundo=((12, 20, 30), ESC2),
         fala="Cientistas do Japão filmaram isso em 2009. Segue a Maia, que tem mais: a luz é mil vezes mais fraca do que o olho enxerga."),
    dict(tipo="fato", titulo="O ROSTO", desenho=c_rosto, fundo=((15, 10, 30), ESC2),
         fala="O que mais brilha é o rosto. A gente é vaga-lume e nem sabe!"),
    dict(tipo="fato", titulo="RELÓGIO", desenho=c_relogio, fundo=((20, 15, 40), ESC2),
         fala="E o brilho segue o relógio: é mais forte às quatro da tarde e mais fraco às dez da manhã."),
    dict(tipo="cta", titulo="BRILHA!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(ESC1, ESC2),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. E lembra:"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "brilho_humano.mp4"))
