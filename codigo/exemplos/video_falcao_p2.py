"""Falcão-peregrino, Parte 2 (BICHOS INSANOS #1). Formato v3 (25–35 s). Usa o falcão da Parte 1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, O
from video_falcao_p1 import falcao, etiqueta, selo, CINZA, CINZA2

MARROM = (150, 100, 60); PALHA = (210, 170, 90); OVO = (215, 150, 110); VERMELHO = (230, 60, 60)


def ninho(d, cx, cy, s):
    d.ellipse([cx - 230 * s, cy - 60 * s, cx + 230 * s, cy + 90 * s], fill=MARROM, outline=O, width=6)
    for i in range(9):
        x = cx - 200 * s + i * 50 * s
        d.line([(x, cy + 10 * s), (x + 60 * s, cy - 40 * s)], fill=PALHA, width=max(3, int(8 * s)))


def ovo(d, x, y, s, rachado=0.0, T=0):
    d.ellipse([x - 45 * s, y - 60 * s, x + 45 * s, y + 55 * s], fill=OVO, outline=O, width=5)
    for k in range(4):
        d.ellipse([x - 25 * s + k * 14 * s, y - 20 * s + (k % 2) * 25 * s, x - 13 * s + k * 14 * s, y - 8 * s + (k % 2) * 25 * s], fill=(150, 80, 50))
    if rachado > 0:
        pts = [(x - 45 * s, y - 5 * s), (x - 20 * s, y - 25 * s), (x, y), (x + 20 * s, y - 30 * s), (x + 45 * s, y - 8 * s)]
        n = max(2, int(len(pts) * rachado))
        d.line(pts[:n], fill=O, width=6)


def g_ovos(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    cx, cy = 560, 1040
    ninho(d, cx, cy, 1.25)
    ciclo = (T % 2.0) / 2.0
    for i, x in enumerate((-110, 0, 110)):
        ovo(d, cx + x, cy - 40, 1.0, rachado=min(1, ciclo * 2.2 - i * 0.2) if ciclo > 0.15 else 0)
    # mãe sentando (desce e sobe)
    desce = 1 - abs(math.sin(T * math.pi / 2))
    falcao(d, cx - 20, 760 + desce * 120, 1.05, 0, T, asas=0.35)
    if ciclo > 0.45:
        s = pop((ciclo - 0.45) / 0.15)
        rotulo(d, 860, 900, "CRACK!", int(80 * s) + 10, VERMELHO)


def c_ddt(d, img, t, T):
    selo(d)
    # avião pulverizador soltando nuvem
    x = (T * 260) % 1400 - 200
    d.rounded_rectangle([x - 120, 560, x + 120, 610], 25, fill=(250, 210, 40), outline=O, width=6)
    d.rectangle([x - 40, 530, x + 40, 640], fill=(250, 210, 40), outline=O, width=5)
    for i in range(14):
        px = x - 100 - i * 40; py = 640 + (i % 3) * 30 + i * 6
        d.ellipse([px - 30, py - 20, px + 30, py + 20], fill=(200, 230, 140, 120))
    rotulo(d, 860, 680, "DDT", 80, (200, 255, 120))
    # cascas: normal x com DDT
    k = min(1, t / 1.5)
    for cx, esp, nome, cor in ((300, 34, "NORMAL", (255, 255, 255)), (780, 34 - 28 * k, "COM DDT", VERMELHO)):
        cy = 1030
        d.ellipse([cx - 160, cy - 200, cx + 160, cy + 170], fill=OVO, outline=O, width=6)
        d.ellipse([cx - 160 + esp, cy - 200 + esp, cx + 160 - esp, cy + 170 - esp], fill=(255, 250, 220), outline=O, width=3)
        rotulo(d, cx, 1240, nome, 52, cor)


def c_zero(d, img, t, T):
    selo(d)
    rotulo(d, 540, 560, "1964", 90, (255, 255, 255))
    rotulo(d, 540, 650, "LESTE DOS EUA", 56, CIANO)
    for i in range(6):
        cx = 220 + (i % 3) * 320; cy = 830 + (i // 3) * 230
        ninho(d, cx, cy, 0.5)
        if t > 0.5 + i * 0.25:
            s = pop((t - 0.5 - i * 0.25) / 0.3)
            d.line([(cx - 90 * s, cy - 90 * s), (cx + 90 * s, cy + 50 * s)], fill=VERMELHO, width=16)
            d.line([(cx - 90 * s, cy + 50 * s), (cx + 90 * s, cy - 90 * s)], fill=VERMELHO, width=16)
    if t > 2.2:
        rotulo(d, 540, 1230, "0 FILHOTES", 70, AMARELO)


def predio(d, x, y0, w, cor, T):
    d.rectangle([x, y0, x + w, 1300], fill=cor, outline=O, width=6)
    for r in range(int((1300 - y0) / 70)):
        for c in range(int(w / 60)):
            acesa = (r * 7 + c * 3) % 5 == 0
            d.rectangle([x + 15 + c * 60, y0 + 20 + r * 70, x + 50 + c * 60, y0 + 60 + r * 70],
                        fill=(255, 220, 120) if acesa else (120, 160, 210))


def pombo(d, x, y, s, T):
    a = math.sin(T * 14) * 40 * s
    d.ellipse([x - 40 * s, y - 25 * s, x + 40 * s, y + 25 * s], fill=(170, 170, 190), outline=O, width=4)
    d.polygon([(x - 10 * s, y - 10 * s), (x - 60 * s, y - 50 * s - a), (x + 20 * s, y - 15 * s)], fill=(140, 140, 165), outline=O)
    d.ellipse([x + 25 * s, y - 40 * s, x + 60 * s, y - 5 * s], fill=(120, 130, 160), outline=O, width=4)


def c_cidade(d, img, t, T):
    selo(d)
    predio(d, 60, 700, 260, (90, 100, 130), T)
    predio(d, 380, 560, 300, (70, 80, 115), T)
    predio(d, 740, 760, 280, (100, 110, 140), T)
    # falcão na beirada do prédio mais alto
    falcao(d, 560, 510 + 0 * T, 0.6, 0, T, asas=0.1)
    for i in range(3):
        px = (700 + T * 220 + i * 160) % 1200
        pombo(d, px, 650 + i * 70, 0.9, T + i)
    if t > 1.0:
        d.rounded_rectangle([250, 1160, 830, 1270], 30, fill=(0, 140, 60), outline=O, width=6)
        rotulo(d, 540, 1215, "BRASIL: OUT A ABR", 52, (255, 230, 60))


def c_cta(d, img, t, T):
    g_ovos(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="OVO FRÁGIL", titulo_y=400, desenho=g_ovos, fundo=((110, 170, 220), (40, 90, 160)),
         fala="Esse falcão, o bicho mais rápido do mundo, quebrava os próprios ovos só de chocar! E o fim é o mais louco."),
    dict(tipo="fato", titulo="O CULPADO", desenho=c_ddt, fundo=((140, 190, 120), (60, 110, 60)),
         fala="O culpado era o DDT, um veneno de lavoura. E segue pra mais bicho insano: ele deixava a casca fina demais."),
    dict(tipo="fato", titulo="SUMIRAM", desenho=c_zero, fundo=((90, 80, 110), (35, 30, 55)),
         fala="Por volta de 1964, não sobrou nenhum casal criando filhotes no leste dos Estados Unidos."),
    dict(tipo="fato", titulo="A VOLTA", desenho=c_cidade, fundo=((255, 170, 110), (120, 70, 140)),
         fala="O veneno foi proibido, e eles voltaram morando em arranha-céus, caçando pombos! E alguns voam até o Brasil."),
    dict(tipo="cta", titulo="OVO FRÁGIL", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((110, 170, 220), (40, 90, 160)),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. Porque esse falcão..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "falcao_p2.mp4"))
