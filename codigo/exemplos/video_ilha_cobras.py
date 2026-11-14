"""Ilha da Queimada Grande (SP): a ilha das cobras onde ninguém pode pisar. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, brilhos, O

MAR = (30, 120, 170); MAR2 = (20, 85, 135); ILHA = (70, 140, 60); ILHA2 = (45, 100, 45); ROCHA = (120, 110, 100)
COBRA = (205, 170, 70); COBRA2 = (150, 110, 40); VERM = (230, 50, 50)


def mar(d, y, T, cor=MAR, cor2=MAR2):
    d.rectangle([0, y, 1080, 1300], fill=cor)
    for i in range(5):
        yy = y + 30 + i * 50
        off = math.sin(T * 1.8 + i * 1.3) * 40
        for k in range(3):
            x = 80 + k * 340 + off
            d.arc([x, yy, x + 160, yy + 30], 200, 340, fill=cor2, width=6)


def ilha(d, cx, cy, s, T):
    d.ellipse([cx - 360 * s, cy - 40 * s, cx + 360 * s, cy + 70 * s], fill=ROCHA, outline=O, width=6)
    d.polygon([(cx - 330 * s, cy), (cx - 160 * s, cy - 230 * s), (cx + 20 * s, cy - 300 * s),
               (cx + 200 * s, cy - 220 * s), (cx + 330 * s, cy)], fill=ILHA, outline=O)
    for i in range(6):  # moitas
        x = cx - 240 * s + i * 95 * s
        y = cy - 80 * s - abs(math.sin(i * 1.7)) * 120 * s
        d.ellipse([x - 55 * s, y - 40 * s, x + 55 * s, y + 40 * s], fill=ILHA2, outline=O, width=4)
    # farol
    fx, fy = cx + 150 * s, cy - 230 * s
    d.rectangle([fx - 18 * s, fy - 110 * s, fx + 18 * s, fy], fill="white", outline=O, width=4)
    d.rectangle([fx - 18 * s, fy - 70 * s, fx + 18 * s, fy - 45 * s], fill=VERM)
    d.polygon([(fx - 26 * s, fy - 110 * s), (fx, fy - 140 * s), (fx + 26 * s, fy - 110 * s)], fill=VERM, outline=O)


def cobra(d, x, y, s, T, fase=0, cor=COBRA, cor2=COBRA2, lingua=True):
    """Jararaca em S, cabeça triangular à direita."""
    pts = []
    for i in range(26):
        u = i / 25
        pts.append((x - 170 * s + u * 170 * s, y + math.sin(u * 7 + T * 3 + fase) * 30 * s))
    d.line(pts, fill=O, width=int(34 * s) + 8, joint="curve")
    d.line(pts, fill=cor, width=int(34 * s), joint="curve")
    for i in range(2, 24, 3):
        px, py = pts[i]
        d.ellipse([px - 8 * s, py - 8 * s, px + 8 * s, py + 8 * s], fill=cor2)
    hx, hy = pts[-1]
    d.polygon([(hx - 10 * s, hy - 26 * s), (hx + 50 * s, hy - 6 * s), (hx + 50 * s, hy + 6 * s), (hx - 10 * s, hy + 26 * s)],
              fill=cor, outline=O)
    d.ellipse([hx + 14 * s, hy - 14 * s, hx + 26 * s, hy - 2 * s], fill="black")
    if lingua and math.sin(T * 6 + fase) > 0:
        d.line([(hx + 50 * s, hy), (hx + 80 * s, hy)], fill=VERM, width=max(3, int(5 * s)))
        d.line([(hx + 80 * s, hy), (hx + 92 * s, hy - 10 * s)], fill=VERM, width=max(3, int(4 * s)))
        d.line([(hx + 80 * s, hy), (hx + 92 * s, hy + 10 * s)], fill=VERM, width=max(3, int(4 * s)))


def placa_proibido(d, cx, cy, s):
    d.rectangle([cx - 10 * s, cy, cx + 10 * s, cy + 170 * s], fill=(130, 90, 50), outline=O, width=4)
    d.ellipse([cx - 90 * s, cy - 90 * s, cx + 90 * s, cy + 90 * s], fill="white", outline=VERM, width=int(20 * s))
    d.line([(cx - 60 * s, cy + 60 * s), (cx + 60 * s, cy - 60 * s)], fill=VERM, width=int(20 * s))
    # bonequinho
    d.ellipse([cx - 14 * s, cy - 55 * s, cx + 14 * s, cy - 27 * s], fill=O)
    d.line([(cx, cy - 25 * s), (cx, cy + 20 * s)], fill=O, width=int(10 * s))
    d.line([(cx, cy + 18 * s), (cx - 20 * s, cy + 55 * s)], fill=O, width=int(9 * s))
    d.line([(cx, cy + 18 * s), (cx + 20 * s, cy + 55 * s)], fill=O, width=int(9 * s))


# ---------------- cenas ----------------
def g_ilha(d, img, t, T):
    mar(d, 1000, T)
    ilha(d, 620, 1000, 1.05, T)
    for i, (x, y) in enumerate([(470, 880), (700, 820), (560, 760), (820, 930)]):
        cobra(d, x, y, 0.68, T, fase=i)
    placa_proibido(d, 210, 760, 0.9)


def c_mapa(d, img, t, T):
    # costa à esquerda, ilha à direita, seta de distância
    mar(d, 640, T)
    d.polygon([(0, 600), (220, 620), (300, 800), (260, 1000), (330, 1300), (0, 1300)], fill=(110, 170, 80), outline=O)
    rotulo(d, 130, 780, "SP", 70, (255, 255, 255))
    ilha(d, 830, 960, 0.45, T)
    k = ease(t / 1.5)
    seta(d, 340, 960, 340 + k * 280, 960, cor=AMARELO, w=12)
    if t > 1.0:
        rotulo(d, 520, 880, "35 km", 64, AMARELO)
    if t > 1.8:
        rotulo(d, 540, 1150, "SÓ AQUI NO MUNDO", 54, (255, 240, 200))


def c_isolada(d, img, t, T):
    # mar subindo e separando a ilha do continente
    nivel = 1150 - ease(t / 2.2) * 330
    d.polygon([(0, 700), (300, 720), (420, 860), (600, 780), (760, 700), (1080, 680), (1080, 1300), (0, 1300)],
              fill=(120, 160, 80), outline=O)
    d.rectangle([0, nivel, 1080, 1300], fill=(40, 130, 190, 230))
    for i in range(3):
        d.arc([150 + i * 300, nivel + 10, 300 + i * 300, nivel + 40], 200, 340, fill=MAR2, width=6)
    cobra(d, 600, 730, 0.6, T, fase=1)
    if t > 1.6:
        rotulo(d, 540, 1120, "11 MIL ANOS ATRÁS", 58, (255, 255, 255))


def passaro(d, x, y, s, T, cor=(240, 240, 250)):
    bat = math.sin(T * 9) * 30 * s
    d.polygon([(x - 60 * s, y - bat), (x, y + 6 * s), (x + 60 * s, y - bat)], fill=cor, outline=O)
    d.ellipse([x - 22 * s, y - 12 * s, x + 22 * s, y + 18 * s], fill=cor, outline=O, width=3)


def c_aves(d, img, t, T):
    # galho com cobra esperando, aves migrando
    d.line([(0, 980), (500, 900), (760, 950)], fill=(120, 80, 50), width=34)
    d.ellipse([480, 820, 640, 920], fill=ILHA2, outline=O, width=4)
    cobra(d, 420, 870, 0.75, T, fase=2)
    for i in range(4):
        x = (1150 - ((T * 120 + i * 260) % 1300))
        passaro(d, x, 640 + i * 45, 0.8, T + i)
    if t > 1.2:
        rotulo(d, 540, 1120, "CARDÁPIO: AVES", 58, (255, 230, 150))


def c_veneno(d, img, t, T):
    # gota de veneno gigante + cobra e cadeado (área proibida)
    cx, cy = 300, 860
    pulso = 1 + 0.05 * math.sin(T * 6)
    r = 150 * pulso
    d.polygon([(cx, cy - r * 1.8), (cx - r * 0.85, cy - r * 0.2), (cx + r * 0.85, cy - r * 0.2)], fill=(130, 220, 80))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(130, 220, 80), outline=O, width=7)
    d.line([(cx, cy - r * 1.8), (cx - r * 0.85, cy - r * 0.2)], fill=O, width=7)
    d.line([(cx, cy - r * 1.8), (cx + r * 0.85, cy - r * 0.2)], fill=O, width=7)
    d.ellipse([cx - 60, cy - 70, cx - 20, cy - 20], fill=(220, 255, 200))
    rotulo(d, cx, cy + 20, "VENENO", 50, (255, 255, 255))
    if t > 1.2:
        s = max(0.1, pop((t - 1.2) / 0.5))
        placa_proibido(d, 760, 820, 1.2 * s)
        rotulo(d, 760, 1120, "SÓ CIENTISTAS", 54, (255, 255, 255))


CENAS = [
    dict(tipo="gancho", titulo="ILHA PROIBIDA", desenho=g_ilha, fundo=((90, 170, 220), (30, 70, 120)),
         fala="Existe uma ilha no Brasil onde ninguém pode pisar, porque ela é dominada por cobras venenosas. E elas só existem ali!"),
    dict(tipo="fato", titulo="ILHA DAS COBRAS", desenho=c_mapa, fundo=((60, 140, 190), (20, 60, 100)),
         fala="É a Queimada Grande, a uns trinta e cinco quilômetros do litoral de São Paulo. Lá vive a jararaca-ilhoa, que não existe em nenhum outro lugar do mundo."),
    dict(tipo="fato", titulo="PRESAS NO MAR", desenho=c_isolada, fundo=((150, 200, 160), (50, 100, 80)),
         fala="Há uns onze mil anos, o mar subiu e isolou a ilha, com as cobras presas lá em cima."),
    dict(tipo="fato", titulo="CAÇA NO AR", desenho=c_aves, fundo=((240, 170, 90), (130, 60, 40)),
         fala="Sem ratos para comer, elas aprenderam a caçar aves que param na ilha durante a migração."),
    dict(tipo="fato", titulo="VENENO TURBO", desenho=c_veneno, fundo=((90, 50, 120), (30, 15, 50)),
         fala="O veneno age rápido, para a presa não fugir voando. Por isso, só cientistas autorizados podem desembarcar."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você pisaria nessa ilha?",
         fala="Comenta: você teria coragem de pisar lá? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "ilha_cobras.mp4"))
