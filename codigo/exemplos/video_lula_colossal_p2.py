"""Lula-colossal, Parte 2 (BICHOS INSANOS #9). Importa desenhos de video_lula_colossal_p1.
Fatos: descrita em 1925 a partir de pedaços achados no estômago de cachalotes; cachalotes trazem
marcas de ventosas/ganchos; primeira filmagem de uma viva em março de 2025 (juvenil de ~30 cm,
quase transparente, ~600 m, Ilhas Sandwich do Sul, robô submarino do Schmidt Ocean Institute)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_lula_colossal_p1 import etiqueta, selo, bolhas, lula, olho, LULA, LULA2, PELE, MAR1, MAR2

CACH = (95, 105, 125); CACH2 = (65, 72, 90); CICAT = (230, 230, 235)
VIDRO = (190, 240, 255)


def cachalote(d, cx, cy, s=1.0, T=0.0, cicatrizes=False, barriga=False):
    """Cachalote de cabeça quadrada nadando para a direita."""
    ond = math.sin(T * 2) * 18 * s
    d.polygon([(cx - 380 * s, cy), (cx - 470 * s, cy - 80 * s + ond), (cx - 460 * s, cy + 80 * s + ond)], fill=CACH2, outline=O)
    d.rounded_rectangle([cx - 400 * s, cy - 120 * s, cx + 330 * s, cy + 120 * s], radius=int(110 * s), fill=CACH, outline=O, width=7)
    d.rectangle([cx + 80 * s, cy - 120 * s, cx + 300 * s, cy + 40 * s], fill=CACH)
    d.line([(cx + 330 * s, cy - 40 * s), (cx + 330 * s, cy + 40 * s)], fill=O, width=7)
    d.line([(cx + 80 * s, cy + 90 * s), (cx + 300 * s, cy + 90 * s)], fill=O, width=6)  # boca
    d.ellipse([cx + 140 * s, cy - 10 * s, cx + 170 * s, cy + 20 * s], fill=O)
    if cicatrizes:
        for i in range(9):
            x = cx - 220 * s + (i % 5) * 80 * s
            y = cy - 60 * s + (i // 5) * 70 * s
            d.ellipse([x - 22 * s, y - 22 * s, x + 22 * s, y + 22 * s], outline=CICAT, width=max(3, int(6 * s)))
    if barriga:
        d.ellipse([cx - 250 * s, cy - 70 * s, cx + 30 * s, cy + 90 * s], fill=(120, 60, 70), outline=O, width=5)
        for i in range(3):  # pedaços de braço da lula
            x0 = cx - 210 * s + i * 80 * s
            pts = [(x0 + j * 14 * s, cy + 20 * s + math.sin(j + i + T * 2) * 18 * s) for j in range(6)]
            d.line(pts, fill=O, width=int(26 * s))
            d.line(pts, fill=PELE, width=int(18 * s))


def g_cem(d, img, t, T, label=True):
    etiqueta(d, "P2")
    bolhas(d, T)
    lula(d, 640, 930, 0.8, T)
    # ampulheta: cem anos
    x, y = 170, 700
    d.polygon([(x - 70, y - 110), (x + 70, y - 110), (x, y), (x + 70, y + 110), (x - 70, y + 110), (x, y)], outline=(240, 220, 160), width=8)
    q = (T * 0.15) % 1
    d.polygon([(x - 70 * (1 - q), y - 110 + 110 * q), (x + 70 * (1 - q), y - 110 + 110 * q), (x, y)], fill=AMARELO)
    d.polygon([(x - 70 * q, y + 110 - 110 * q), (x + 70 * q, y + 110 - 110 * q), (x + 70, y + 110), (x - 70, y + 110)], fill=AMARELO)
    rotulo(d, x, y + 160, "100", 60, AMARELO, traduzir=False)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if label and k > 0.05:
        rotulo(d, 540, 1200, "NINGUÉM VIU UMA VIVA", int(44 * k) + 1, AMARELO)


def c_1925(d, img, t, T):
    selo(d)
    cachalote(d, 560, 820, 1.05, T, barriga=True)
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if k > 0.05:
        rotulo(d, 540, 590, "1925", int(80 * k) + 1, AMARELO, traduzir=False)
        rotulo(d, 420, 1060, "NO ESTÔMAGO", int(50 * k) + 1, CIANO)


def c_briga(d, img, t, T):
    selo(d)
    cachalote(d, 470, 830, 0.85, T, cicatrizes=True)
    lula(d, 900, 1110, 0.45, T, ganchos=True)
    k = pop(min(1, max(0, t - 0.5) / 0.5))
    if k > 0.05:
        rotulo(d, 330, 600, "MARCAS DOS GANCHOS", int(44 * k) + 1, AMARELO)
        seta(d, 330, 640, 380, 760, AMARELO, 9)


def bebe(d, cx, cy, s, T):
    """Lulinha juvenil quase transparente: só contornos claros."""
    bal = math.sin(T * 2.5) * 10
    cy += bal
    for k in range(8):
        pts = [(cx + 60 * s + j * 22 * s, cy + (k - 3.5) * 9 * s * (1 + j / 4) + math.sin(T * 3 + k + j) * 6 * s) for j in range(8)]
        d.line(pts, fill=VIDRO, width=max(3, int(6 * s)))
    d.ellipse([cx - 160 * s, cy - 45 * s, cx + 70 * s, cy + 45 * s], outline=VIDRO, width=5)
    d.polygon([(cx - 150 * s, cy), (cx - 210 * s, cy - 60 * s), (cx - 110 * s, cy - 25 * s)], outline=VIDRO)
    d.polygon([(cx - 150 * s, cy), (cx - 210 * s, cy + 60 * s), (cx - 110 * s, cy + 25 * s)], outline=VIDRO)
    for i in range(6):
        d.ellipse([cx - 120 * s + i * 28 * s, cy - 6 * s, cx - 108 * s + i * 28 * s, cy + 6 * s], fill=(240, 150, 140))
    d.ellipse([cx + 20 * s, cy - 22 * s, cx + 60 * s, cy + 18 * s], fill=(30, 40, 60), outline=VIDRO, width=3)


def robo(d, x, y, T):
    d.rounded_rectangle([x - 130, y - 90, x + 130, y + 90], radius=20, fill=(240, 200, 40), outline=O, width=6)
    d.rectangle([x - 110, y + 90, x + 110, y + 130], fill=(90, 90, 100), outline=O, width=5)
    d.ellipse([x + 90, y - 40, x + 170, y + 40], fill=(60, 60, 70), outline=O, width=6)
    d.ellipse([x + 112, y - 18, x + 148, y + 18], fill=(120, 220, 255))
    for i in range(2):  # luzes
        on = (int(T * 4) + i) % 2
        d.ellipse([x - 100 + i * 50, y - 70, x - 76 + i * 50, y - 46], fill=(255, 80, 80) if on else (90, 30, 30))


def c_filmada(d, img, t, T):
    selo(d)
    robo(d, 240, 760, T)
    # facho de luz do robô
    d.polygon([(410, 760), (1080, 560), (1080, 1000)], fill=(40, 70, 110))
    bebe(d, 800, 780, 1.2, T)
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 280, 1000, "2025", int(70 * k) + 1, AMARELO, traduzir=False)
        rotulo(d, 780, 960, "BEBÊ DE 30 CM", int(44 * k) + 1, CIANO)
        rotulo(d, 540, 1190, "QUASE TRANSPARENTE", int(46 * k) + 1, (255, 255, 255))


def c_cta(d, img, t, T):
    g_cem(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="100 ANOS!", titulo_y=400, desenho=g_cem, fundo=(MAR1, MAR2),
         fala="Essa lula do olho gigante passou cem anos sem ser vista viva! E o fim é o mais louco."),
    dict(tipo="fato", titulo="SÓ PEDAÇOS", desenho=c_1925, fundo=((25, 55, 100), MAR2),
         fala="Em 1925, só acharam pedaços dela, na barriga de cachalotes. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="A BRIGA", desenho=c_briga, fundo=((15, 30, 60), (3, 8, 20)),
         fala="cachalotes caçam essa lula e saem com marcas dos ganchos. Que briga!"),
    dict(tipo="fato", titulo="FILMADA!", desenho=c_filmada, fundo=((5, 20, 45), (0, 3, 12)),
         fala="Em 2025, um robô filmou a primeira viva: um bebê de trinta centímetros, quase transparente."),
    dict(tipo="cta", titulo="100 ANOS!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. E pensar que..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "lula_colossal_p2.mp4"))
