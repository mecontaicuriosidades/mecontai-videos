"""Baiacu (fugu): o peixe mais venenoso que se come. Formato v2 (35–50 s), piloto."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, brilhos, O

PELE = (232, 196, 92); BARRIGA = (250, 236, 190); MANCHA = (150, 110, 50)
ROXO = (150, 70, 200); VERDE_VEN = (120, 230, 90); VERMELHO = (230, 60, 60)


def baiacu(d, cx, cy, r, T, inflar=1.0, bravo=False):
    """Baiacu de desenho: inflar 0..1 (0 = magro, 1 = bola de espinhos)."""
    rx, ry = r * (0.85 + 0.25 * inflar), r * (0.55 + 0.45 * inflar)
    # espinhos
    if inflar > 0.3:
        n = 22
        for i in range(n):
            a = i / n * 2 * math.pi + math.sin(T * 2) * 0.03
            x0, y0 = cx + math.cos(a) * rx * 0.95, cy + math.sin(a) * ry * 0.95
            L = r * 0.28 * inflar
            x1, y1 = cx + math.cos(a) * (rx + L), cy + math.sin(a) * (ry + L)
            p = [(x1, y1), (x0 + math.cos(a + 1.6) * 12, y0 + math.sin(a + 1.6) * 12),
                 (x0 + math.cos(a - 1.6) * 12, y0 + math.sin(a - 1.6) * 12)]
            d.polygon(p, fill=(245, 240, 220), outline=O)
    # cauda e nadadeiras
    d.polygon([(cx - rx * 0.9, cy), (cx - rx * 1.45, cy - r * 0.45), (cx - rx * 1.35, cy + r * 0.45)],
              fill=PELE, outline=O)
    bat = math.sin(T * 9) * 0.25
    d.polygon([(cx + rx * 0.05, cy + ry * 0.2), (cx - rx * 0.25, cy + ry * (0.75 + bat)), (cx + rx * 0.3, cy + ry * 0.55)],
              fill=(240, 170, 70), outline=O)
    # corpo
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PELE, outline=O, width=8)
    d.chord([cx - rx * 0.92, cy - ry * 0.2, cx + rx * 0.92, cy + ry * 0.97], 0, 180, fill=BARRIGA)
    for k in range(6):
        mx = cx - rx * 0.5 + k * rx * 0.2; my = cy - ry * 0.55 + (k % 2) * ry * 0.18
        d.ellipse([mx - 14, my - 10, mx + 14, my + 10], fill=MANCHA)
    # olhos e boca
    olhos(d, cx + rx * 0.42, cy - ry * 0.25, T, esp=r * 0.42, r=r * 0.13)
    if bravo:
        for sx in (-1, 1):
            ex = cx + rx * 0.42 + sx * r * 0.21
            d.line([(ex - 22, cy - ry * 0.25 - r * 0.24 - sx * 8), (ex + 22, cy - ry * 0.25 - r * 0.24 + sx * 8)],
                   fill=O, width=8)
    bx, by = cx + rx * 0.92, cy + ry * 0.12
    d.ellipse([bx - 20, by - 14, bx + 14, by + 14], fill=(200, 80, 80), outline=O, width=5)


def gota(d, x, y, s, cor=VERDE_VEN):
    d.polygon([(x, y - s * 1.6), (x - s * 0.9, y), (x + s * 0.9, y)], fill=cor)
    d.ellipse([x - s, y - s * 0.6, x + s, y + s * 1.1], fill=cor, outline=O, width=4)


def caveira(d, x, y, s, cor=(245, 245, 245)):
    d.ellipse([x - s, y - s, x + s, y + s * 0.8], fill=cor, outline=O, width=5)
    d.rounded_rectangle([x - s * 0.55, y + s * 0.5, x + s * 0.55, y + s * 1.1], 8, fill=cor, outline=O, width=5)
    for sx in (-1, 1):
        d.ellipse([x + sx * s * 0.45 - s * 0.28, y - s * 0.15, x + sx * s * 0.45 + s * 0.28, y + s * 0.35], fill=O)
    d.polygon([(x, y + s * 0.3), (x - s * 0.12, y + s * 0.5), (x + s * 0.12, y + s * 0.5)], fill=O)


# ---------------- cenas ----------------
def g_baiacu(d, img, t, T):
    # já no 1º quadro: baiacu inchando, gotas de veneno e caveiras
    k = 0.55 + 0.45 * pop(t / 0.8)
    baiacu(d, 560, 800, 230, T, inflar=k, bravo=True)
    for i, (x, y) in enumerate([(220, 560), (900, 520), (860, 1120), (250, 1080)]):
        yy = y + ((T * 120 + i * 60) % 120)
        gota(d, x, yy, 22)
    if t > 0.6:
        caveira(d, 900, 640, 55)
    if t > 1.2:
        rotulo(d, 560, 1200, "1.200x MAIS FORTE QUE CIANETO", 46, VERDE_VEN)


def c_onde(d, img, t, T):
    baiacu(d, 540, 760, 240, T, inflar=0.0)
    # órgãos venenosos brilhando por dentro
    pulso = 0.5 + 0.5 * math.sin(T * 6)
    org = [((470, 790), 60, "FÍGADO", (430, 1010)), ((620, 830), 42, "OVÁRIOS", (760, 1010)),
           ((720, 700), 30, "OLHOS", (860, 520))]
    for i, ((x, y), s, nome, (lx, ly)) in enumerate(org):
        if t > 0.5 + i * 0.7:
            rr = s * (1 + 0.12 * pulso)
            d.ellipse([x - rr, y - rr * 0.75, x + rr, y + rr * 0.75], outline=VERMELHO, width=10)
            d.line([(x, y), (lx, ly)], fill=VERMELHO, width=5)
            rotulo(d, lx, ly + (30 if ly > y else -30), nome, 44, VERMELHO)


def c_antidoto(d, img, t, T):
    # frasco de remédio riscado + pessoa paralisada, mas de olhos abertos
    d.rounded_rectangle([170, 600, 400, 940], 30, fill=(200, 235, 255), outline=O, width=7)
    d.rectangle([215, 545, 355, 605], fill=(120, 120, 140), outline=O, width=6)
    rotulo(d, 285, 770, "ANTÍDOTO", 36, (40, 80, 160))
    if t > 0.7:
        e = ease((t - 0.7) / 0.4)
        d.line([(140, 560), (140 + 290 * e, 560 + 400 * e)], fill=VERMELHO, width=22)
        d.line([(430, 560), (430 - 290 * e, 560 + 400 * e)], fill=VERMELHO, width=22)
    # pessoa rígida (palito) com olhos abertos
    px, py = 760, 640
    d.ellipse([px - 75, py - 75, px + 75, py + 75], fill=(252, 214, 188), outline=O, width=7)
    olhos(d, px, py - 5, 0.5, esp=60, r=18, piscada=999)
    d.line([(px - 25, py + 40), (px + 25, py + 40)], fill=O, width=7)
    d.line([(px, py + 75), (px, py + 330)], fill=(60, 120, 220), width=40)
    for sx in (-1, 1):
        d.line([(px, py + 130), (px + sx * 110, py + 260)], fill=(60, 120, 220), width=26)
        d.line([(px, py + 330), (px + sx * 60, py + 520)], fill=(40, 50, 90), width=28)
    if t > 1.6:
        for i in range(3):
            a = T * 3 + i * 2.1
            x, y = px + math.cos(a) * 150, py + 200 + math.sin(a) * 60
            rotulo(d, x, y, "!", 60, AMARELO)
    if t > 2.0:
        rotulo(d, 600, 1235, "PARALISADO E ACORDADO", 46, AMARELO)


def c_licenca(d, img, t, T):
    # certificado com selo + chapéu de chef + faca
    k = pop(t / 0.6)
    w, h = 520 * k, 380 * k
    d.rounded_rectangle([540 - w / 2, 560 - h / 2 + 120, 540 + w / 2, 560 + h / 2 + 120], 20,
                        fill=(255, 250, 230), outline=(180, 140, 40), width=10)
    if k > 0.9:
        rotulo(d, 540, 560, "LICENÇA", 60, (150, 100, 20))
        for i in range(4):
            d.line([(360, 630 + i * 36), (720, 630 + i * 36)], fill=(200, 190, 160), width=8)
        d.ellipse([650, 700, 760, 810], fill=VERMELHO, outline=O, width=5)
        brilhos(d, 705, 755, 80, T, n=6)
    # chapéu de chef
    d.ellipse([110, 930, 270, 1050], fill="white", outline=O, width=6)
    d.ellipse([190, 900, 350, 1030], fill="white", outline=O, width=6)
    d.rectangle([140, 1020, 320, 1090], fill="white", outline=O, width=6)
    if t > 1.4:
        rotulo(d, 640, 1160, "ANOS DE TREINO", 56, AMARELO)


def c_imperador(d, img, t, T):
    # coroa + prato de fugu + sinal de proibido
    cx, cy = 540, 860
    d.ellipse([cx - 300, cy - 70, cx + 300, cy + 110], fill=(240, 240, 250), outline=O, width=7)
    for i in range(9):  # fatias finas de fugu em flor
        a = i / 9 * 2 * math.pi
        x, y = cx + math.cos(a) * 150, cy + 20 + math.sin(a) * 40
        d.ellipse([x - 70, y - 22, x + 70, y + 22], fill=(255, 240, 235), outline=(220, 180, 170), width=3)
    # coroa flutuando
    y0 = 500 + math.sin(T * 2) * 10
    d.polygon([(400, y0 + 90), (420, y0), (470, y0 + 55), (540, y0 - 20), (610, y0 + 55), (660, y0), (680, y0 + 90)],
              fill=AMARELO, outline=O)
    for x in (420, 540, 660):
        d.ellipse([x - 14, y0 - 14 - (20 if x == 540 else 0), x + 14, y0 + 14 - (20 if x == 540 else 0)], fill=VERMELHO, outline=O, width=3)
    if t > 0.9:
        s = pop((t - 0.9) / 0.5)
        r = 260 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=VERMELHO, width=int(30 * s) + 1)
        d.line([(cx - r * 0.7, cy - r * 0.7), (cx + r * 0.7, cy + r * 0.7)], fill=VERMELHO, width=int(30 * s) + 1)
    if t > 1.6:
        rotulo(d, 540, 1200, "SÓ ELE NÃO PODE", 56, AMARELO)


CENAS = [
    dict(tipo="gancho", titulo="MAIS QUE CIANETO", desenho=g_baiacu, fundo=((20, 60, 70), (5, 20, 30)),
         fala="Esse peixe tem um veneno mil e duzentas vezes mais forte que cianeto. E tem gente que paga caro pra comer ele!"),
    dict(tipo="fato", titulo="É O BAIACU", desenho=c_onde, fundo=((40, 120, 150), (10, 40, 70)),
         fala="É o baiacu, o fugu no Japão. O veneno fica no fígado, nos ovários e nos olhos."),
    dict(tipo="fato", titulo="NÃO TEM ANTÍDOTO", desenho=c_antidoto, fundo=((70, 30, 90), (25, 10, 40)),
         fala="E não existe antídoto. Ele paralisa os músculos, mas a pessoa continua acordada."),
    dict(tipo="fato", titulo="SÓ COM LICENÇA", desenho=c_licenca, fundo=((150, 90, 40), (70, 35, 15)),
         fala="Por isso, no Japão, só cozinheiros com licença especial podem preparar, depois de anos de treino."),
    dict(tipo="fato", titulo="PROIBIDO PRO IMPERADOR", desenho=c_imperador, fundo=((120, 20, 40), (40, 5, 15)),
         fala="E o mais bizarro: por tradição, é a única comida que o imperador do Japão não pode comer!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você comeria baiacu?",
         fala="Comenta: você teria coragem? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "baiacu.mp4"))
