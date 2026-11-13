"""Mancenilha: a árvore mais perigosa do mundo (recorde Guinness). Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, brilhos, O

TRONCO = (120, 80, 50); COPA = (60, 150, 70); COPA2 = (35, 105, 50); FRUTO = (170, 220, 90)
SEIVA = (245, 245, 225); PELE = (245, 190, 150); BOLHA = (255, 120, 110); CHUVA = (150, 210, 255)
VERMELHO = (230, 50, 50); FOGO = (255, 140, 30)


def arvore(d, cx, cy, s, T, frutos=True, xis=False):
    """Árvore com tronco torto e copa; (cx, cy) = base do tronco."""
    bal = math.sin(T * 1.2) * 6 * s
    d.polygon([(cx - 40 * s, cy), (cx - 25 * s + bal, cy - 330 * s), (cx + 30 * s + bal, cy - 330 * s), (cx + 45 * s, cy)],
              fill=TRONCO, outline=O)
    for dx, dy, r in ((-150, -380, 140), (150, -390, 140), (0, -470, 160), (-60, -330, 120), (80, -320, 120)):
        x, y, rr = cx + dx * s + bal, cy + dy * s, r * s
        d.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=COPA if dx % 2 == 0 else COPA2, outline=O, width=6)
    if frutos:
        for i, (dx, dy) in enumerate(((-170, -300), (-40, -280), (120, -300), (200, -360), (-210, -420))):
            x, y = cx + dx * s + bal, cy + dy * s
            r = 22 * s
            d.line([(x, y - r - 12 * s), (x, y - r)], fill=O, width=4)
            d.ellipse([x - r, y - r, x + r, y + r], fill=FRUTO, outline=O, width=4)
    if xis:
        x, y = cx, cy - 170 * s
        d.line([(x - 35 * s, y - 45 * s), (x + 40 * s, y + 45 * s)], fill=VERMELHO, width=int(20 * s))
        d.line([(x + 40 * s, y - 45 * s), (x - 35 * s, y + 45 * s)], fill=VERMELHO, width=int(20 * s))


def braco(d, x, y, s, bolhas=0.0, T=0):
    """Braço na horizontal saindo da esquerda, com bolhas aparecendo (0..1)."""
    d.rounded_rectangle([x - 420 * s, y - 60 * s, x, y + 60 * s], int(55 * s), fill=PELE, outline=O, width=6)
    d.ellipse([x - 40 * s, y - 75 * s, x + 110 * s, y + 75 * s], fill=PELE, outline=O, width=6)
    n = int(7 * bolhas)
    for i in range(n):
        bx = x - 360 * s + i * 50 * s
        by = y - 10 * s + ((i * 37) % 50 - 25) * s
        r = (14 + (i * 7) % 12) * s
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=BOLHA, outline=O, width=3)
        d.ellipse([bx - r * 0.4, by - r * 0.5, bx, by - r * 0.1], fill=(255, 220, 210))


def gotas(d, x0, x1, y0, y1, T, cor=CHUVA, n=16):
    for i in range(n):
        x = x0 + (i * 71) % max(1, (x1 - x0))
        y = y0 + ((T * 500 + i * 97) % max(1, (y1 - y0)))
        d.line([(x, y), (x - 6, y + 30)], fill=cor, width=7)


# ---------------- cenas ----------------
def g_chuva(d, img, t, T):
    arvore(d, 380, 1240, 1.2, T)
    gotas(d, 120, 660, 520, 1150, T, n=18)
    # pingos que passam pelas folhas viram "veneno" (amarelados) e caem no braço
    braco(d, 960, 1050, 0.75, bolhas=min(1, t / 1.4), T=T)
    gotas(d, 700, 940, 820, 1000, T, cor=SEIVA, n=6)
    if t > 0.3:
        rotulo(d, 820, 880, "QUEIMA!", 70, BOLHA)


def trofeu(d, cx, cy, s, T):
    d.polygon([(cx - 120 * s, cy - 220 * s), (cx + 120 * s, cy - 220 * s), (cx + 70 * s, cy - 40 * s), (cx - 70 * s, cy - 40 * s)],
              fill=AMARELO, outline=O)
    for sx in (-1, 1):
        d.arc([cx + sx * 120 * s - 60 * s, cy - 210 * s, cx + sx * 120 * s + 60 * s, cy - 110 * s],
              -90 if sx > 0 else 90, 90 if sx > 0 else 270, fill=O, width=10)
    d.rectangle([cx - 25 * s, cy - 40 * s, cx + 25 * s, cy + 30 * s], fill=AMARELO, outline=O, width=5)
    d.rounded_rectangle([cx - 100 * s, cy + 30 * s, cx + 100 * s, cy + 80 * s], 10, fill=(200, 140, 20), outline=O, width=5)
    rotulo(d, cx, cy - 130 * s, "Nº 1", int(70 * s), O, traduzir=False)


def c_recorde(d, img, t, T):
    arvore(d, 300, 1230, 0.9, T)
    s = max(0.1, pop(t / 0.6))
    trofeu(d, 790, 870, 1.1 * s, T)
    brilhos(d, 790, 760, 220, T)
    if t > 0.8:
        rotulo(d, 790, 1060, "MAIS PERIGOSA", 50, AMARELO)
        rotulo(d, 790, 1120, "DO MUNDO", 50, AMARELO)
    # praia
    d.rectangle([0, 1230, 1080, 1300], fill=(240, 215, 150), outline=O, width=5)


def c_seiva(d, img, t, T):
    # galho quebrado pingando seiva leitosa
    d.line([(80, 620), (560, 700)], fill=TRONCO, width=50)
    d.ellipse([530, 670, 600, 730], fill=SEIVA, outline=O, width=5)
    k = (t * 1.3) % 1
    d.ellipse([555, 740 + k * 220, 585, 780 + k * 220], fill=SEIVA, outline=O, width=3)
    braco(d, 760, 1030, 0.9, bolhas=min(1, max(0, (t - 0.8) / 1.5)), T=T)
    if t > 1.0:
        rotulo(d, 820, 760, "SEIVA TÓXICA", 52, SEIVA)
    if t > 2.6:
        gotas(d, 100, 1000, 520, 640, T, n=10)


def c_fruto(d, img, t, T):
    s = max(0.1, pop(t / 0.5))
    r = 170 * s
    cx, cy = 360, 860
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=FRUTO, outline=O, width=8)
    d.line([(cx, cy - r), (cx + 20, cy - r - 60 * s)], fill=O, width=10)
    d.ellipse([cx + 10, cy - r - 70 * s, cx + 110 * s, cy - r - 20 * s], fill=COPA, outline=O, width=5)
    olhos(d, cx, cy - 20 * s, T, esp=90 * s, r=24 * s)
    d.arc([cx - 50 * s, cy + 30 * s, cx + 50 * s, cy + 80 * s], 200, 340, fill=O, width=7)  # sorriso malvado
    # garganta pegando fogo
    if t > 1.0:
        fx, fy = 830, 960
        for i in range(5):
            h = 120 + 40 * math.sin(T * 8 + i)
            x = fx - 140 + i * 70
            d.polygon([(x - 40, fy + 120), (x, fy + 120 - h), (x + 40, fy + 120)], fill=FOGO if i % 2 else (255, 210, 60), outline=O)
        rotulo(d, 830, 1160, "BOCA EM CHAMAS", 48, FOGO)
    if t > 2.0:
        rotulo(d, 330, 1080, "MAÇÃZINHA DA MORTE", 42, FRUTO)


def c_fumaca(d, img, t, T):
    # fogueira
    fx, fy = 300, 1150
    for i in range(4):
        h = 140 + 50 * math.sin(T * 9 + i)
        x = fx - 90 + i * 60
        d.polygon([(x - 45, fy), (x, fy - h), (x + 45, fy)], fill=FOGO if i % 2 else (255, 210, 60), outline=O)
    d.line([(fx - 130, fy + 20), (fx + 130, fy - 5)], fill=TRONCO, width=26)
    # nuvens de fumaça subindo para um olho
    for i in range(5):
        k = ((T * 0.4 + i * 0.2) % 1)
        x, y = fx + k * 420, fy - 200 - k * 380
        r = 40 + k * 50
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 150, 150), outline=O, width=4)
    # olho irritado
    ox, oy = 840, 680
    d.ellipse([ox - 130, oy - 75, ox + 130, oy + 75], fill=(255, 200, 200), outline=O, width=7)
    d.ellipse([ox - 45, oy - 45, ox + 45, oy + 45], fill=(90, 60, 40), outline=O, width=5)
    for i in range(4):
        d.line([(ox - 120 + i * 20, oy - 10 + i * 6), (ox - 70 + i * 15, oy + 5)], fill=VERMELHO, width=4)
    if t > 2.0:
        arvore(d, 820, 1250, 0.55, T, frutos=False, xis=True)
        rotulo(d, 820, 870, "X = PERIGO", 46, VERMELHO)


CENAS = [
    dict(tipo="gancho", titulo="ÁRVORE ASSASSINA", desenho=g_chuva, fundo=((50, 80, 110), (15, 25, 45)),
         fala="Ficar embaixo dessa árvore na chuva pode queimar a sua pele. E isso nem é o pior dela!"),
    dict(tipo="fato", titulo="RECORDE MUNDIAL", desenho=c_recorde, fundo=((40, 160, 200), (10, 70, 110)),
         fala="É a mancenilha, recordista do Guinness como a árvore mais perigosa do mundo. Ela cresce em praias do Caribe e da Flórida."),
    dict(tipo="fato", titulo="SEIVA QUE QUEIMA", desenho=c_seiva, fundo=((70, 110, 60), (20, 40, 20)),
         fala="A seiva leitosa dela causa bolhas na pele. Até a chuva que escorre das folhas leva esse veneno."),
    dict(tipo="fato", titulo="FRUTO DA MORTE", desenho=c_fruto, fundo=((130, 60, 60), (45, 15, 20)),
         fala="O fruto parece uma maçãzinha cheirosa, mas queima a boca e a garganta. Os espanhóis chamavam de maçãzinha da morte."),
    dict(tipo="fato", titulo="NEM QUEIMAR", desenho=c_fumaca, fundo=((80, 70, 90), (25, 20, 35)),
         fala="E nem adianta queimar: a fumaça irrita e pode até cegar por um tempo. Por isso muitas têm um X vermelho no tronco."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você chegaria perto dela?",
         fala="Comenta: você chegaria perto dela? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "mancenilha.mp4"))
