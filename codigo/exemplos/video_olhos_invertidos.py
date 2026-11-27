"""Seus olhos veem de cabeça pra baixo (CIÊNCIA BIZARRA #8). Formato v3 + ESTRATÉGIA DA SEMANA 23/11.
Fatos: a lente do olho (cristalino + córnea) projeta na retina uma imagem invertida e o cérebro interpreta o
mundo "do lado certo"; George M. Stratton (1896/1897) usou óculos que inverteram a visão (3 dias no 1º teste e
8 dias no 2º) e, com o passar dos dias, foi se adaptando e se mexendo cada vez mais normalmente; cada olho tem um
ponto cego onde o nervo óptico sai da retina (sem fotorreceptores) e o cérebro preenche essa falha com o que
está em volta."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
import idioma

SERIE = "CIÊNCIA BIZARRA #8"
FUNDO1 = (60, 30, 90); FUNDO2 = (15, 8, 30)
BRANCO = (245, 245, 250); IRIS = (70, 150, 90); RETINA = (230, 90, 90)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def arvore(d, x, y, s=1.0, inv=False):
    """Arvorezinha com o pé em y (inv=True: de cabeça pra baixo, com o pé em y e a copa embaixo)."""
    g = -1 if not inv else 1
    d.rectangle([x - 12 * s, min(y, y + g * 90 * s), x + 12 * s, max(y, y + g * 90 * s)], fill=(140, 90, 50), outline=O, width=3)
    cy = y + g * 150 * s
    d.ellipse([x - 70 * s, cy - 70 * s, x + 70 * s, cy + 70 * s], fill=(80, 190, 90), outline=O, width=4)


def olho_corte(d, cx, cy, R, T, inv_k=1.0):
    """Olho em corte, visto de lado: luz entra pela lente (esquerda) e forma a imagem invertida na retina (direita)."""
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=BRANCO, outline=O, width=8)
    d.arc([cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14], -70, 70, fill=RETINA, width=16)
    lx = cx - R + 30
    d.ellipse([lx - 30, cy - 75, lx + 30, cy + 75], fill=(170, 220, 255), outline=O, width=5)
    d.line([(cx + R - 5, cy + 30), (cx + R + 90, cy + 60)], fill=(240, 190, 120), width=26)
    d.line([(cx + R - 5, cy + 30), (cx + R + 90, cy + 60)], fill=O, width=4)
    return lx


def g_olho(d, img, t, T, label=True):
    etiqueta(d)
    cx, cy, R = 690, 880, 230
    lx = olho_corte(d, cx, cy, R, T)
    # árvore de verdade à esquerda
    arvore(d, 150, 1010, 1.0)
    # raios que se cruzam na lente
    k = min(1.0, 0.5 + t / 0.8)
    topo, pe = (150, 790), (150, 1010)
    fim_topo, fim_pe = (cx + R - 30, cy + 150), (cx + R - 30, cy - 70)
    for (a, b, cor) in ((topo, fim_topo, AMARELO), (pe, fim_pe, CIANO)):
        d.line([a, (lx, cy)], fill=cor, width=6)
        bx = lx + (b[0] - lx) * k; by = cy + (b[1] - cy) * k
        d.line([(lx, cy), (bx, by)], fill=cor, width=6)
    # árvore invertida dentro do olho
    if k >= 1.0:
        arvore(d, cx + 130, cy - 60, 0.6, inv=True)
    if label:
        kk = pop(min(1, max(0, t - 0.4) / 0.5))
        if kk > 0.05:
            rotulo(d, 690, 1180, "AO CONTRÁRIO!", int(52 * kk) + 1, AMARELO)


def c_lente(d, img, t, T):
    selo(d)
    # seta pra cima → lente → seta pra baixo
    k = ease(t / 1.0)
    seta(d, 190, 1080, 190, 700, CIANO, 22)
    d.ellipse([460, 600, 620, 1180], fill=(170, 220, 255), outline=O, width=8)
    d.line([(190, 700), (540, 890)], fill=AMARELO, width=5)
    d.line([(190, 1080), (540, 890)], fill=AMARELO, width=5)
    if k > 0.3:
        x2 = 540 + 350 * k
        d.line([(540, 890), (x2, 700 + 380 * k)], fill=AMARELO, width=5)
        d.line([(540, 890), (x2, 1080 - 380 * k)], fill=AMARELO, width=5)
    if k > 0.95:
        seta(d, 890, 700, 890, 1080, (255, 120, 120), 22)
    kk = pop(min(1, max(0, t - 0.3) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1240, "LENTE DO OLHO", int(48 * kk) + 1, (170, 220, 255))


def casinha(d, x, y, s=1.0, inv=False):
    g = 1 if inv else -1
    d.rectangle([x - 60 * s, min(y, y + g * 100 * s), x + 60 * s, max(y, y + g * 100 * s)], fill=(250, 200, 120), outline=O, width=4)
    d.polygon([(x - 80 * s, y + g * 100 * s), (x + 80 * s, y + g * 100 * s), (x, y + g * 180 * s)], fill=(200, 60, 50), outline=O)


def c_oculos(d, img, t, T):
    selo(d)
    # cabeça com óculos grandes; balão com o mundo de ponta-cabeça
    cx, cy = 300, 930
    d.ellipse([cx - 150, cy - 170, cx + 150, cy + 170], fill=(240, 190, 150), outline=O, width=7)
    d.chord([cx - 155, cy - 180, cx + 155, cy + 20], 180, 360, fill=(90, 60, 40), outline=O, width=6)
    for dx in (-65, 65):
        d.rounded_rectangle([cx + dx - 58, cy - 40, cx + dx + 58, cy + 40], 14, fill=(30, 30, 40), outline=O, width=6)
        d.ellipse([cx + dx - 24, cy - 22, cx + dx + 4, cy + 6], fill=(120, 140, 160))
    d.arc([cx - 50, cy + 70, cx + 50, cy + 120], 200, 340, fill=O, width=6)
    # balão: mundo virado
    bx, by = 780, 760
    d.ellipse([bx - 230, by - 170, bx + 230, by + 170], fill=(140, 200, 255), outline=O, width=6)
    for i in range(3):
        d.ellipse([500 + i * 40, 900 + i * 35, 530 + i * 40, 930 + i * 35], fill=(140, 200, 255), outline=O, width=3)
    d.rectangle([bx - 200, by - 160, bx + 200, by - 110], fill=(110, 180, 80))
    casinha(d, bx - 70, by - 110, 0.7, inv=True)
    arvore(d, bx + 110, by - 110, 0.55, inv=True)
    rotulo(d, 300, 640, "1896", 60, (255, 255, 255), traduzir=False)
    kk = pop(min(1, max(0, t - 1.2) / 0.5))
    if kk > 0.05:
        rotulo(d, 780, 1010, "DIAS DEPOIS...", int(40 * kk) + 1, (255, 255, 255))
        rotulo(d, 780, 1080, "SE ADAPTOU!", int(56 * kk) + 1, AMARELO)


def c_ponto(d, img, t, T):
    selo(d)
    # retina vista de frente: cheia de pontinhos (sensores) e um buraco onde sai o nervo
    cx, cy, R = 540, 820, 270
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(200, 70, 70), outline=O, width=8)
    for i in range(110):
        a = i * 2.399; r = R * 0.92 * math.sqrt((i + 0.5) / 110)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        if math.hypot(x - (cx + 100), y - cy) > 80:
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(255, 210, 120))
    hx, hy = cx + 100, cy
    d.ellipse([hx - 70, hy - 70, hx + 70, hy + 70], fill=(250, 235, 200), outline=O, width=5)
    kk = pop(min(1, max(0, t - 0.8) / 0.5))
    if kk > 0.05:
        rotulo(d, hx, hy, "?", int(90 * kk) + 1, (255, 60, 60), traduzir=False)
        rotulo(d, 540, 1235, "SEM NENHUM SENSOR", int(44 * kk) + 1, (255, 255, 255))
    if t > 1.8:
        k2 = pop(min(1, (t - 1.8) / 0.4))
        rotulo(d, 540, 1170, "O CÉREBRO INVENTA", int(48 * k2) + 1, AMARELO)


def c_cta(d, img, t, T):
    g_olho(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="INVERTIDO!", titulo_y=400, desenho=g_olho, fundo=(FUNDO1, FUNDO2),
         fala="Seus olhos veem tudo de cabeça pra baixo! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="A LENTE", desenho=c_lente, fundo=((30, 60, 100), (8, 15, 35)),
         fala="A lente do olho vira a imagem, e o cérebro desvira. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="ÓCULOS LOUCOS", desenho=c_oculos, fundo=((40, 80, 60), (10, 25, 18)),
         fala="em 1896, um cientista usou óculos que viravam o mundo, e o cérebro foi se adaptando!"),
    dict(tipo="fato", titulo="PONTO CEGO", desenho=c_ponto, fundo=((80, 25, 40), (20, 5, 10)),
         fala="Cada olho tem um ponto cego, sem sensor. O cérebro tapa inventando! Que trapaceiro!"),
    dict(tipo="cta", titulo="INVERTIDO!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(FUNDO1, FUNDO2),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. E lembra: seus olhos veem..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "olhos_invertidos.mp4"))
