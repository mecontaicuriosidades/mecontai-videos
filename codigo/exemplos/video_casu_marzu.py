"""Casu marzu: o queijo com larvas vivas que pulam. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, brilhos, O

QUEIJO = (250, 225, 150); QUEIJO2 = (225, 190, 110); CASCA = (190, 140, 70)
LARVA = (250, 250, 240); MOSCA = (60, 70, 60); CREME = (245, 215, 140)


def larva(d, x, y, s, T, fase=0, ang=0.0):
    """Larvinha branca segmentada, se contorcendo."""
    pts = []
    for i in range(6):
        u = i / 5
        dx = (u - 0.5) * 60 * s
        dy = math.sin(u * 4 + T * 10 + fase) * 6 * s
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((x + dx * ca - dy * sa, y + dx * sa + dy * ca))
    for i, (px, py) in enumerate(pts):
        r = 11 * s * (0.75 + 0.25 * math.sin(i / 5 * math.pi))
        d.ellipse([px - r - 2, py - r - 2, px + r + 2, py + r + 2], fill=O)
    for i, (px, py) in enumerate(pts):
        r = 11 * s * (0.75 + 0.25 * math.sin(i / 5 * math.pi))
        d.ellipse([px - r, py - r, px + r, py + r], fill=LARVA)
    hx, hy = pts[-1]
    d.ellipse([hx - 3 * s, hy - 3 * s, hx + 3 * s, hy + 3 * s], fill=O)


def fatia_queijo(d, cx, cy, s, furos=True):
    topo = [(cx - 260 * s, cy - 40 * s), (cx + 220 * s, cy - 160 * s), (cx + 300 * s, cy - 60 * s)]
    frente = [(cx - 260 * s, cy - 40 * s), (cx + 300 * s, cy - 60 * s), (cx + 300 * s, cy + 140 * s), (cx - 260 * s, cy + 160 * s)]
    d.polygon(frente, fill=QUEIJO2, outline=O)
    d.line(frente + [frente[0]], fill=O, width=7)
    d.polygon(topo, fill=QUEIJO, outline=O)
    d.line(topo + [topo[0]], fill=O, width=7)
    if furos:
        for (fx, fy, r) in [(-150, 40, 30), (40, 80, 22), (180, 20, 34), (-40, -10, 18)]:
            d.ellipse([cx + (fx - r) * s, cy + (fy - r) * s, cx + (fx + r) * s, cy + (fy + r) * s], fill=CASCA)


def mosca(d, x, y, s, T):
    bat = math.sin(T * 40) * 0.5 + 0.5
    for sx in (-1, 1):
        d.ellipse([x + sx * 10 * s - 26 * s, y - 40 * s - 10 * s * bat, x + sx * 10 * s + 26 * s, y - 4 * s],
                  fill=(220, 240, 255, 170), outline=O, width=3)
    d.ellipse([x - 26 * s, y - 16 * s, x + 26 * s, y + 18 * s], fill=MOSCA, outline=O, width=4)
    d.ellipse([x + 14 * s, y - 14 * s, x + 34 * s, y + 6 * s], fill=(200, 40, 40), outline=O, width=3)


# ---------------- cenas ----------------
def g_pulo(d, img, t, T):
    fatia_queijo(d, 620, 900, 1.05)
    for i in range(7):  # larvas saltando em arco
        ciclo = ((T * 0.9 + i * 0.37) % 1.0)
        x0 = 420 + i * 60
        x = x0 + ciclo * 160
        y = 830 - math.sin(ciclo * math.pi) * 380
        larva(d, x, y, 1.7, T, fase=i, ang=ciclo * 6)
    for i in range(5):
        larva(d, 470 + i * 70, 860 + (i % 2) * 20, 1.4, T, fase=i * 2)
    if t > 0.3:
        rotulo(d, 640, 1210, "LARVAS VIVAS", 64, (255, 120, 90))


def c_sardenha(d, img, t, T):
    # ilha simples + queijo e mosca botando ovos
    d.polygon([(130, 620), (230, 520), (330, 560), (360, 700), (310, 860), (200, 900), (150, 780)],
              fill=(110, 190, 110), outline=O)
    rotulo(d, 245, 960, "SARDENHA", 44, AMARELO)
    fatia_queijo(d, 700, 900, 0.8)
    mosca(d, 640 + math.sin(T * 3) * 80, 620 + math.cos(T * 4) * 30, 1.6, T)
    k = ease(t / 2.0)
    for i in range(int(k * 8)):  # ovinhos
        x = 560 + i * 35
        d.ellipse([x - 9, 840 - 6, x + 9, 840 + 8], fill=LARVA, outline=O, width=2)


def c_mole(d, img, t, T):
    # queijo amolecendo e escorrendo
    k = ease(t / 2.4)
    cx, cy = 520, 820
    d.ellipse([cx - 320, cy + 160, cx + 320, cy + 260], fill=(230, 230, 240), outline=O, width=6)  # prato
    d.rounded_rectangle([cx - 230, cy - 140 + 80 * k, cx + 230, cy + 170], int(40 + 60 * k), fill=QUEIJO2, outline=O, width=7)
    for i in range(5):  # escorridas
        x = cx - 190 + i * 95
        d.ellipse([x - 30, cy + 140, x + 30, cy + 170 + 50 * k + (i % 2) * 20], fill=CREME, outline=O, width=4)
    for i in range(6):
        larva(d, cx - 170 + i * 68, cy - 80 + 80 * k + math.sin(T * 3 + i) * 10, 1.3, T, fase=i)
    for i in range(3):  # cheiro
        x = cx - 120 + i * 120
        pts = [(x + math.sin(T * 3 + j * 0.9 + i) * 18, cy - 200 - j * 28) for j in range(8)]
        d.line(pts, fill=(160, 210, 90), width=10, joint="curve")
    if t > 1.3:
        rotulo(d, cx, 1180, "QUASE LÍQUIDO", 54, (255, 240, 180))


def c_mao(d, img, t, T):
    # pão com queijo, mão cobrindo, larvas pulando com régua
    d.rounded_rectangle([200, 900, 760, 1040], 50, fill=(215, 160, 90), outline=O, width=7)
    d.rectangle([230, 880, 730, 910], fill=CREME)
    cobre = ease((t - 0.8) / 0.8)
    mx = 480; my = 640 + 200 * cobre
    d.rounded_rectangle([mx - 190, my - 70, mx + 190, my + 80], 60, fill=(240, 190, 160), outline=O, width=6)
    for k in range(4):
        d.line([(mx - 150 + k * 90, my - 60), (mx - 150 + k * 90, my - 120)], fill=O, width=8)
        d.ellipse([mx - 180 + k * 90, my - 150, mx - 120 + k * 90, my - 50], fill=(240, 190, 160), outline=O, width=5)
    d.rectangle([880, 560, 930, 1040], fill=(255, 220, 80), outline=O, width=5)  # régua
    for k in range(9):
        y = 1040 - k * 55
        d.line([(880, y), (905 if k % 2 else 920, y)], fill=O, width=4)
    rotulo(d, 905, 520, "15 CM", 50, AMARELO)
    ciclo = (T * 0.8) % 1.0
    larva(d, 820, 1000 - math.sin(ciclo * math.pi) * 420, 1.6, T, ang=ciclo * 7)


def trofeu(d, cx, cy, s):
    d.polygon([(cx - 90 * s, cy - 120 * s), (cx + 90 * s, cy - 120 * s), (cx + 60 * s, cy + 20 * s), (cx - 60 * s, cy + 20 * s)],
              fill=AMARELO, outline=O)
    d.rectangle([cx - 18 * s, cy + 20 * s, cx + 18 * s, cy + 80 * s], fill=AMARELO, outline=O, width=4)
    d.rectangle([cx - 70 * s, cy + 80 * s, cx + 70 * s, cy + 110 * s], fill=(150, 100, 40), outline=O, width=4)
    for sx in (-1, 1):
        d.arc([cx + sx * 90 * s - 45 * s, cy - 110 * s, cx + sx * 90 * s + 45 * s, cy - 20 * s],
              270 if sx > 0 else 90, 90 if sx > 0 else 270, fill=O, width=8)


def c_proibido(d, img, t, T):
    trofeu(d, 280, 800, 1.6 * pop(t / 0.5))
    rotulo(d, 280, 1030, "MAIS PERIGOSO", 46, (255, 240, 180))
    fatia_queijo(d, 760, 820, 0.5)
    if t > 1.0:
        r = 190
        d.ellipse([760 - r, 800 - r, 760 + r, 800 + r], outline=(230, 40, 40), width=26)
        d.line([(760 - r * 0.7, 800 + r * 0.7), (760 + r * 0.7, 800 - r * 0.7)], fill=(230, 40, 40), width=26)
        rotulo(d, 760, 1040, "VENDA PROIBIDA", 46, (255, 120, 110))


CENAS = [
    dict(tipo="gancho", titulo="QUEIJO VIVO", desenho=g_pulo, fundo=((200, 120, 50), (70, 35, 20)),
         fala="Esse queijo vem cheio de larvas vivas, e elas pulam! E tem gente que come assim mesmo."),
    dict(tipo="fato", titulo="RECEITA DE MOSCA", desenho=c_sardenha, fundo=((60, 140, 190), (20, 50, 90)),
         fala="É o casu marzu, da ilha da Sardenha, na Itália. Moscas botam ovos no queijo de ovelha, e as larvas nascem lá dentro."),
    dict(tipo="fato", titulo="AMOLECIDO", desenho=c_mole, fundo=((110, 90, 60), (40, 30, 20)),
         fala="Elas digerem a gordura, e o queijo vai ficando mole, quase líquido, com um cheiro fortíssimo."),
    dict(tipo="fato", titulo="CUIDADO COM O OLHO", desenho=c_mao, fundo=((150, 60, 90), (50, 20, 40)),
         fala="As larvas saltam até quinze centímetros! Por isso, quem come costuma cobrir o pão com a mão."),
    dict(tipo="fato", titulo="RECORDE NOJENTO", desenho=c_proibido, fundo=((70, 60, 120), (20, 20, 50)),
         fala="O Guinness já chamou de queijo mais perigoso do mundo, e a venda é proibida pelas regras de higiene."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você provaria?",
         fala="Comenta: você teria coragem de provar? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "casu_marzu.mp4"))
