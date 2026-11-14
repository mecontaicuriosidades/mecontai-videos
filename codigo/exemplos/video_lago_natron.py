"""Lago Natron (Tanzânia): o lago vermelho que deixa animais mortos como estátuas. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, sol, brilhos, O

LAGO = (200, 50, 50); LAGO2 = (150, 25, 35); SAL = (245, 240, 225); SAL2 = (210, 200, 180)
PEDRA = (225, 220, 205); ROSA = (255, 130, 170); ROSA2 = (230, 90, 130); MONTANHA = (130, 90, 80)
LINHO = (235, 215, 160)


def lago(d, y, T, cor=LAGO, cor2=LAGO2):
    d.rectangle([0, y, 1080, 1300], fill=cor)
    for i in range(6):
        yy = y + 30 + i * 45
        off = math.sin(T * 1.5 + i) * 30
        d.arc([100 + off + i * 60, yy, 360 + off + i * 60, yy + 30], 0, 180, fill=cor2, width=6)
    # crostas de sal na margem
    for i in range(7):
        x = 60 + i * 160
        d.ellipse([x - 70, y - 18, x + 70, y + 22], fill=SAL, outline=O, width=4)


def passaro_pedra(d, cx, cy, s, cor=PEDRA):
    """Ave calcificada empoleirada (estátua), virada para a direita."""
    d.line([(cx - 10 * s, cy + 70 * s), (cx - 10 * s, cy + 140 * s)], fill=O, width=int(10 * s) + 2)
    d.line([(cx + 20 * s, cy + 70 * s), (cx + 25 * s, cy + 140 * s)], fill=O, width=int(10 * s) + 2)
    d.ellipse([cx - 90 * s, cy - 10 * s, cx + 70 * s, cy + 90 * s], fill=cor, outline=O, width=6)   # corpo
    d.polygon([(cx - 80 * s, cy + 20 * s), (cx - 170 * s, cy + 50 * s), (cx - 90 * s, cy + 70 * s)], fill=cor, outline=O)
    d.ellipse([cx + 30 * s, cy - 80 * s, cx + 110 * s, cy], fill=cor, outline=O, width=6)          # cabeça
    d.polygon([(cx + 105 * s, cy - 45 * s), (cx + 160 * s, cy - 35 * s), (cx + 105 * s, cy - 25 * s)], fill=SAL2, outline=O)
    # olho "de pedra" (fechado) e rachaduras
    d.line([(cx + 62 * s, cy - 45 * s), (cx + 82 * s, cy - 45 * s)], fill=O, width=5)
    for a, b in (((-40, 20), (-10, 50)), ((10, 30), (30, 60)), ((40, -50), (55, -25))):
        d.line([(cx + a[0] * s, cy + a[1] * s), (cx + b[0] * s, cy + b[1] * s)], fill=SAL2, width=4)


def flamingo(d, cx, cy, s, T, fase=0):
    bal = math.sin(T * 2 + fase) * 6 * s
    d.line([(cx, cy + 40 * s), (cx + 5 * s, cy + 220 * s)], fill=ROSA2, width=int(8 * s) + 2)
    d.line([(cx + 5 * s, cy + 130 * s), (cx + 40 * s, cy + 110 * s), (cx + 10 * s, cy + 90 * s)], fill=ROSA2, width=int(8 * s) + 2)
    d.ellipse([cx - 80 * s, cy - 30 * s, cx + 70 * s, cy + 60 * s], fill=ROSA, outline=O, width=5)
    pts = [(cx + 50 * s, cy), (cx + 90 * s, cy - 90 * s + bal), (cx + 60 * s, cy - 160 * s + bal)]
    d.line(pts, fill=O, width=int(18 * s) + 6)
    d.line(pts, fill=ROSA, width=int(18 * s))
    hx, hy = pts[-1]
    d.ellipse([hx - 25 * s, hy - 22 * s, hx + 25 * s, hy + 22 * s], fill=ROSA, outline=O, width=4)
    d.polygon([(hx + 15 * s, hy - 8 * s), (hx + 55 * s, hy + 10 * s), (hx + 40 * s, hy + 30 * s), (hx + 12 * s, hy + 12 * s)],
              fill=(40, 30, 40))
    d.ellipse([hx - 6 * s, hy - 10 * s, hx + 6 * s, hy + 2 * s], fill=O)


# ---------------- cenas ----------------
def g_estatua(d, img, t, T):
    # montanha vulcânica no fundo
    d.polygon([(560, 900), (820, 560), (1080, 900)], fill=MONTANHA, outline=O)
    d.polygon([(780, 610), (820, 560), (860, 610)], fill=(90, 60, 55))
    lago(d, 920, T)
    # galho seco saindo do lago com o pássaro-estátua
    d.line([(300, 1280), (330, 980), (420, 900)], fill=(170, 150, 130), width=26)
    passaro_pedra(d, 420, 760, 1.25)
    if t > 0.2:
        brilhos(d, 430, 760, 200, T, n=6, cor=SAL)
        rotulo(d, 800, 1130, "VIROU PEDRA?", 58, SAL)


def medidor(d, x, y, nivel, T):
    """Escala de pH de 7 a 14 com ponteiro."""
    cores = [(80, 200, 120), (120, 190, 200), (100, 150, 230), (90, 100, 220), (110, 80, 200), (140, 60, 180), (160, 40, 150)]
    for i, c in enumerate(cores):
        d.rectangle([x + i * 110, y, x + (i + 1) * 110, y + 80], fill=c, outline=O, width=4)
        rotulo(d, x + i * 110 + 55, y + 40, str(7 + i), 40, (255, 255, 255), traduzir=False)
    px = x + (nivel - 7) * 110
    d.polygon([(px, y - 10), (px - 30, y - 70), (px + 30, y - 70)], fill=AMARELO, outline=O)


def c_ph(d, img, t, T):
    lago(d, 1080, T)
    nivel = 7 + ease(t / 2.0) * 3.5
    medidor(d, 155, 780, nivel, T)
    rotulo(d, 155 + 3.5 * 110, 650, "pH " + __import__("idioma").num(10.5, 1), 70, AMARELO, traduzir=False)
    if t > 2.0:
        rotulo(d, 540, 960, "QUEIMA A PELE", 56, (255, 140, 140))


def c_vermelho(d, img, t, T):
    lago(d, 1150, T)
    # lupa mostrando micróbios
    cx, cy, r = 520, 820, 240
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 190, 180), outline=O, width=12)
    d.line([(cx + r * 0.7, cy + r * 0.7), (cx + r * 1.15, cy + r * 1.15)], fill=O, width=40)
    for i in range(9):
        a = i * 0.7 + T * 0.6
        rr = 60 + (i * 37) % 140
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.9
        d.ellipse([x - 26, y - 16, x + 26, y + 16], fill=(220, 40, 60), outline=O, width=4)
        d.ellipse([x - 8, y - 6, x + 2, y + 4], fill="white")
    if t > 1.0:
        rotulo(d, 540, 1100, "MICRÓBIOS VERMELHOS", 52, (255, 210, 210))


def mumia(d, cx, cy, s, T):
    d.rounded_rectangle([cx - 70 * s, cy - 230 * s, cx + 70 * s, cy + 200 * s], int(60 * s), fill=LINHO, outline=O, width=6)
    for i in range(9):
        y = cy - 190 * s + i * 45 * s
        d.line([(cx - 65 * s, y), (cx + 65 * s, y + 18 * s)], fill=(190, 165, 110), width=6)
    olhos(d, cx, cy - 150 * s, T, esp=50 * s, r=14 * s)


def c_mumia(d, img, t, T):
    passaro_pedra(d, 300, 820, 1.0)
    d.rectangle([150, 960, 470, 1000], fill=SAL, outline=O, width=4)
    if t > 1.2:
        s = max(0.1, pop((t - 1.2) / 0.5))
        mumia(d, 800, 860, 1.0 * s, T)
        # saco de natrão
        d.rounded_rectangle([640, 1110, 960, 1200], 20, fill=(150, 110, 60), outline=O, width=5)
        rotulo(d, 800, 1155, "NATRÃO", 50, SAL)
    rotulo(d, 300, 1080, "CONSERVADO", 46, SAL)


def c_flamingos(d, img, t, T):
    lago(d, 1020, T, cor=(220, 80, 70), cor2=(170, 50, 50))
    n = 1 + int(min(1, t / 1.5) * 5)
    pos = [(200, 820), (420, 780), (640, 830), (860, 790), (310, 960), (750, 980)]
    for i in range(n):
        x, y = pos[i]
        flamingo(d, x, y, 0.8 if i < 4 else 0.6, T, fase=i)
    # predador com medo, de longe
    if t > 2.2:
        rotulo(d, 540, 470, "MILHÕES DE FILHOTES", 56, (255, 240, 250))


CENAS = [
    dict(tipo="gancho", titulo="VIRA ESTÁTUA", desenho=g_estatua, fundo=((240, 140, 80), (120, 40, 40)),
         fala="Esse lago vermelho deixa animais mortos parecendo estátuas de pedra. E mesmo assim, tem bicho que ama viver nele!"),
    dict(tipo="fato", titulo="ÁGUA QUE QUEIMA", desenho=c_ph, fundo=((90, 60, 140), (30, 20, 60)),
         fala="É o lago Natron, na Tanzânia. A água é tão alcalina que chega a pH dez e meio, e pode queimar a pele."),
    dict(tipo="fato", titulo="COR DE SANGUE", desenho=c_vermelho, fundo=((170, 60, 70), (60, 15, 25)),
         fala="O vermelho vem de micróbios que adoram sal e calor, e tingem a água inteira."),
    dict(tipo="fato", titulo="MÚMIA NATURAL", desenho=c_mumia, fundo=((200, 160, 90), (90, 60, 30)),
         fala="Os animais que morrem ali ficam cobertos de sais e se conservam. Esse mesmo mineral, o natrão, era usado pelos egípcios nas múmias!"),
    dict(tipo="fato", titulo="BERÇÁRIO ROSA", desenho=c_flamingos, fundo=((255, 170, 120), (180, 80, 90)),
         fala="E o mais louco: milhões de flamingos nascem justamente ali, porque quase nenhum predador chega perto."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você visitaria esse lago?",
         fala="Comenta: você teria coragem de visitar? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lago_natron.mp4"))
