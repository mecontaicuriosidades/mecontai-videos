"""Axolote, Parte 2 (BICHOS INSANOS #3). Formato v3 (25–35 s). Usa o axolote da Parte 1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, brilhos, seta, O
from video_axolote_p1 import axolote, etiqueta, selo, ROSA, ROSA2, BARRIGA, VERDE

MARROM = (120, 95, 70); MARROM2 = (85, 65, 45); PEDRA = (130, 130, 145)
VERMELHO = (225, 45, 55)


def regua_altura(d, x, y0, y1, T):
    d.line([(x, y0), (x, y1)], fill="white", width=8)
    for i in range(6):
        y = y0 + (y1 - y0) * i / 5
        d.line([(x - 20, y), (x + 20, y)], fill="white", width=6)


def chupeta(d, x, y, s):
    d.ellipse([x - 40 * s, y - 30 * s, x + 40 * s, y + 30 * s], fill=(120, 200, 255), outline=O, width=5)
    d.ellipse([x - 16 * s, y - 16 * s, x + 16 * s, y + 16 * s], fill=AMARELO, outline=O, width=4)
    d.arc([x - 30 * s, y - 70 * s, x + 30 * s, y - 20 * s], 180, 360, fill=(120, 200, 255), width=int(10 * s))


def g_bebe(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    d.rectangle([0, 1150, 1080, 1920], fill=(215, 190, 140))
    axolote(d, 470, 920, 1.55, T, olhar=1)
    # chupeta na boca (cabeça vai até x ≈ 470 + 300*1.55)
    chupeta(d, 470 + 300 * 1.55 + 10, 920 + 15 * 1.55, 1.1)
    regua_altura(d, 80, 620, 1100, T)
    rotulo(d, 200, 600, "ADULTO?", 48, AMARELO)


def bebe_axolote(d, x, y, T, i):
    axolote(d, x, y + 8 * math.sin(T * 3 + i), 0.4, T + i, olhar=-1 if i % 2 else 1)


def c_guelras(d, img, t, T):
    selo(d)
    d.rectangle([0, 1150, 1080, 1920], fill=(215, 190, 140))
    axolote(d, 420, 830, 1.25, T, olhar=1)
    # destaque nas guelras
    gx, gy = 420 + 120 * 1.25, 830 - 140
    a = 115 + 8 * math.sin(T * 5)
    d.ellipse([gx - a, gy - a, gx + a, gy + a], outline=AMARELO, width=8)
    rotulo(d, gx + 260, gy - 40, "GUELRAS", 50, AMARELO)
    if t > 2.5:  # filhotes
        for i, x in enumerate((260, 520, 780)):
            bebe_axolote(d, x, 1100, T, i)
        rotulo(d, 830, 990, "FILHOTES", 44, "white")


def salamandra_terra(d, cx, cy, s, T, k):
    """Mistura o axolote (k=0) com a forma de terra (k=1): sem guelras, mais escuro."""
    cor = tuple(int(a + (b - a) * k) for a, b in zip(ROSA, MARROM))
    cor2 = tuple(int(a + (b - a) * k) for a, b in zip(ROSA2, MARROM2))
    axolote(d, cx, cy, s, T * (1 - 0.8 * k), olhar=-1, cor=cor, cor2=cor2, guelra=1 - k)
    if k > 0.6:
        for i in range(6):  # pintinhas
            x = cx - (-110 + i * 45) * s
            d.ellipse([x - 9 * s, cy - 30 * s, x + 9 * s, cy - 12 * s], fill=AMARELO)


def gota(d, x, y, r):
    d.polygon([(x, y - r * 1.8), (x - r * 0.9, y - r * 0.2), (x + r * 0.9, y - r * 0.2)], fill=(120, 220, 255), outline=O)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 220, 255), outline=O, width=4)


def c_vira(d, img, t, T):
    selo(d)
    # água à esquerda, terra/pedra à direita
    d.rectangle([0, 1100, 540, 1920], fill=(60, 140, 170))
    d.polygon([(540, 1100), (1080, 960), (1080, 1920), (540, 1920)], fill=(140, 120, 90))
    d.ellipse([700, 980, 1000, 1080], fill=PEDRA, outline=O, width=5)
    k = ease((t - 1.0) / 2.6) if t > 1.0 else 0
    # gota de hormônio caindo
    if t < 1.4:
        gy = 560 + 380 * ease(t / 1.2)
        gota(d, 300, gy, 34)
        rotulo(d, 300, 520, "HORMÔNIO", 48, AMARELO)
    x = 330 + 520 * k
    y = 1010 - 60 * k
    salamandra_terra(d, x, y, 1.0, T, k)
    if k > 0.2:
        seta(d, 300, 760, 700, 760)
        rotulo(d, 500, 680, "SEM GUELRAS", 46, "white")


def canal(d, T):
    d.rectangle([0, 900, 1080, 1250], fill=(70, 150, 140))
    for i in range(5):
        y = 940 + i * 60
        x = (T * 80 + i * 200) % 1300 - 100
        d.arc([x, y, x + 120, y + 30], 200, 340, fill=(160, 220, 210), width=5)
    d.rectangle([0, 760, 1080, 900], fill=(90, 170, 90))
    for x in range(40, 1080, 170):  # árvores da margem
        d.rectangle([x + 30, 700, x + 50, 890], fill=(110, 80, 50))
        d.ellipse([x - 20, 600, x + 100, 740], fill=(60, 150, 70), outline=O, width=4)
    # barquinho colorido
    bx = 620 + 30 * math.sin(T)
    d.polygon([(bx - 170, 1000), (bx + 170, 1000), (bx + 130, 1060), (bx - 130, 1060)], fill=(230, 80, 60), outline=O)
    d.rectangle([bx - 140, 920, bx + 140, 1000], fill=AMARELO, outline=O, width=4)
    d.polygon([(bx - 160, 920), (bx + 160, 920), (bx + 120, 880), (bx - 120, 880)], fill=(60, 170, 220), outline=O)


def c_extinto(d, img, t, T):
    selo(d)
    canal(d, T)
    axolote(d, 260, 1150, 0.55, T, olhar=1)
    if t > 1.6:
        s = pop((t - 1.6) / 0.4)
        d.rounded_rectangle([540 - 330 * s, 500, 540 + 330 * s, 640], 30, fill=VERMELHO, outline=O, width=6)
        if s > 0.8:
            rotulo(d, 540, 570, "MENOS DE 1.000", 60, "white")
        rotulo(d, 780, 1160, "CIDADE DO MÉXICO", 40, "white")


def c_cta(d, img, t, T):
    g_bebe(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="NÃO CRESCE", titulo_y=400, desenho=g_bebe, fundo=((90, 180, 200), (30, 90, 130)),
         fala="Esse bicho refaz o próprio coração... e nunca deixa de ser bebê! E o fim é o mais triste."),
    dict(tipo="fato", titulo="BEBÊ ADULTO", desenho=c_guelras, fundo=((120, 200, 220), (50, 120, 160)),
         fala="Segue pra mais bicho insano: o axolote cresce e até tem filhotes, mas continua com as guelras de bebê, debaixo d'água."),
    dict(tipo="fato", titulo="VIRA OUTRO", desenho=c_vira, fundo=((150, 110, 190), (70, 45, 120)),
         fala="Mas, com um hormônio da tireoide, ele pode se transformar: perde as guelras e sai da água."),
    dict(tipo="fato", titulo="AMEAÇADO", desenho=c_extinto, fundo=((240, 150, 110), (170, 70, 70)),
         fala="E o pior: na natureza, ele só vive nos canais perto da Cidade do México. E estimam que restem menos de mil adultos."),
    dict(tipo="cta", titulo="NÃO CRESCE", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((90, 180, 200), (30, 90, 130)),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. Porque esse bicho..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "axolote_p2.mp4"))
