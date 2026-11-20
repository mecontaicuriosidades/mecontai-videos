"""Gálio, Parte 2 (CIÊNCIA BIZARRA #1). Formato v3 (25–35 s). Importa desenhos de video_galio_p1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_galio_p1 import etiqueta, selo, PRATA, PRATA2, BRILHO

LATA = (200, 40, 50); LATA2 = (150, 25, 35); ALU = (195, 200, 210); ALU2 = (160, 165, 175)
PAPEL = (240, 230, 200); TINTA = (60, 50, 90)


def lata(d, cx, cy, T, rasgo=0.0, s=1.0):
    """Lata de refrigerante (sem marca) com gota de gálio e rasgo que abre."""
    w, h = 130 * s, 250 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], int(30 * s), fill=LATA, outline=O, width=6)
    d.ellipse([cx - w, cy - h - 30 * s, cx + w, cy - h + 30 * s], fill=ALU, outline=O, width=5)
    d.ellipse([cx - 30 * s, cy - h - 10 * s, cx + 30 * s, cy - h + 10 * s], fill=ALU2, outline=O, width=3)
    d.rectangle([cx - w + 20 * s, cy - 60 * s, cx + w - 20 * s, cy + 20 * s], fill=LATA2)
    # gota de gálio
    d.ellipse([cx - 50 * s, cy - 150 * s, cx + 10 * s, cy - 100 * s], fill=PRATA, outline=O, width=4)
    d.ellipse([cx - 40 * s, cy - 143 * s, cx - 22 * s, cy - 130 * s], fill=BRILHO)
    if rasgo > 0:
        # rasgo em zigue-zague que abre
        pts = []
        for i in range(8):
            y = cy - 120 * s + i * 45 * s
            x = cx - 20 * s + (25 if i % 2 else -25) * s
            pts.append((x, y))
        a = 18 * rasgo * s
        esq = [(x - a, y) for x, y in pts]
        dir_ = [(x + a, y) for x, y in pts[::-1]]
        d.polygon(esq + dir_, fill=(20, 15, 30))
        d.line(esq, fill=O, width=5)
        d.line(dir_, fill=O, width=5)


def g_lata(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    k = 0.5 + 0.5 * math.sin(T * 1.4)
    lata(d, 560, 960, T, 0.3 + 0.7 * k, 1.15)
    brilhos(d, 520, 800, 120, T, 6, BRILHO)
    rotulo(d, 870, 640, "ALUMÍNIO", 48, ALU)


def dedos(d, x, y, lado, s=1.0):
    pele = (240, 190, 150)
    for i in range(3):
        yy = y + i * 55 * s
        d.rounded_rectangle([x - 90 * s if lado < 0 else x, yy, x if lado < 0 else x + 90 * s, yy + 45 * s], int(22 * s),
                            fill=pele, outline=O, width=4)


def c_quebra(d, img, t, T):
    selo(d)
    k = ease(t / 3.4)
    # duas metades da lata se afastando, presas pelos dedos
    sep = 10 + 140 * k
    for lado in (-1, 1):
        cx = 540 + lado * sep
        d.rounded_rectangle([cx - 110 if lado < 0 else cx, 700, cx if lado < 0 else cx + 110, 1200], 26,
                            fill=LATA, outline=O, width=6)
        for i in range(6):
            y = 720 + i * 80
            d.polygon([(cx, y), (cx + lado * 22, y + 40), (cx, y + 80)], fill=ALU2, outline=O)
        dedos(d, cx + lado * 110, 880, lado, 1.0)
    if t > 2.4:
        rotulo(d, 540, 600, "FEITO BISCOITO", 56, "white")
    elif t > 1.4:
        p = pop((t - 1.4) / 0.4)
        rotulo(d, 540, 590, "CRACK!", int(84 * max(0.3, p)), AMARELO)


def aviao(d, cx, cy, T, s=1.0):
    corpo = (225, 230, 240)
    d.rounded_rectangle([cx - 330 * s, cy - 50 * s, cx + 300 * s, cy + 50 * s], int(50 * s), fill=corpo, outline=O, width=6)
    d.polygon([(cx + 280 * s, cy - 40 * s), (cx + 380 * s, cy - 150 * s), (cx + 400 * s, cy - 150 * s), (cx + 350 * s, cy)], fill=corpo, outline=O)
    d.polygon([(cx - 40 * s, cy), (cx + 120 * s, cy + 200 * s), (cx + 180 * s, cy + 200 * s), (cx + 80 * s, cy)], fill=ALU2, outline=O)
    d.polygon([(cx - 40 * s, cy), (cx + 60 * s, cy - 170 * s), (cx + 110 * s, cy - 170 * s), (cx + 80 * s, cy)], fill=ALU, outline=O)
    for i in range(6):
        x = cx - 230 * s + i * 70 * s
        d.ellipse([x - 14 * s, cy - 24 * s, x + 14 * s, cy + 4 * s], fill=CIANO, outline=O, width=3)
    d.ellipse([cx - 360 * s, cy - 40 * s, cx - 300 * s, cy + 30 * s], fill=CIANO, outline=O, width=4)


def caixa_perigo(d, cx, cy, T):
    d.rectangle([cx - 110, cy - 90, cx + 110, cy + 90], fill=(200, 150, 90), outline=O, width=6)
    d.polygon([(cx, cy - 60), (cx + 60, cy), (cx, cy + 60), (cx - 60, cy)], fill="white", outline=O)
    d.polygon([(cx, cy - 60), (cx + 60, cy), (cx - 60, cy)], fill=(250, 250, 250), outline=O)
    d.polygon([(cx - 60, cy), (cx + 60, cy), (cx, cy + 60)], fill=O)
    a = 8 * math.sin(T * 6)
    d.ellipse([cx - 22, cy - 32 + a, cx + 22, cy + 4 + a], fill=PRATA, outline=O, width=3)


def c_aviao(d, img, t, T):
    selo(d)
    voo = 40 * math.sin(T * 1.5)
    aviao(d, 560, 720 + voo, T, 1.15)
    caixa_perigo(d, 540, 1140, T)
    if t > 1.2:
        rotulo(d, 820, 1140, "CARGA", 50, AMARELO)
        rotulo(d, 820, 1200, "PERIGOSA", 50, AMARELO)
    rotulo(d, 220, 1060, "GÁLIO", 46, PRATA)


def c_previsao(d, img, t, T):
    selo(d)
    # papel com a tabela e um quadradinho vazio que se acende
    d.polygon([(170, 560), (910, 540), (930, 1230), (150, 1250)], fill=PAPEL, outline=O)
    for r in range(4):
        for c in range(6):
            x, y = 230 + c * 110, 640 + r * 130
            vazio = (r, c) == (2, 3)
            if vazio:
                k = 0.5 + 0.5 * math.sin(T * 5)
                cor = AMARELO if t > 1.6 else (240, 230, 200)
                d.rectangle([x, y, x + 90, y + 100], fill=cor, outline=O, width=5)
                rotulo(d, x + 45, y + 50, "?", int(60 + 8 * k), O, traduzir=False)
            else:
                d.rectangle([x, y, x + 90, y + 100], fill=(210, 220, 235), outline=TINTA, width=3)
    rotulo(d, 330, 1180, "1871", 64, TINTA)
    seta(d, 450, 1180, 640, 1180, TINTA, 10)
    rotulo(d, 760, 1180, "1875", 64, (200, 40, 50))


def c_cta(d, img, t, T):
    g_lata(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="COME METAL", titulo_y=400, desenho=g_lata, fundo=((70, 60, 130), (25, 20, 60)),
         fala="Esse metal que derrete na mão destrói alumínio só de encostar! E o final é o mais louco."),
    dict(tipo="fato", titulo="LATA FRÁGIL", desenho=c_quebra, fundo=((60, 120, 160), (20, 55, 95)),
         fala="Uma gota de gálio entra no alumínio. Segue pra mais Ciência Bizarra: em horas, a lata quebra com os dedos."),
    dict(tipo="fato", titulo="NO AVIÃO", desenho=c_aviao, fundo=((120, 180, 230), (50, 100, 170)),
         fala="Por isso o gálio viaja como carga perigosa: avião é cheio de alumínio."),
    dict(tipo="fato", titulo="PREVISTO", desenho=c_previsao, fundo=((130, 90, 60), (70, 45, 30)),
         fala="E o mais louco: o químico Mendeleev previu esse metal quatro anos antes de ele ser descoberto, sem nunca ter visto."),
    dict(tipo="cta", titulo="COME METAL", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((70, 60, 130), (25, 20, 60)),
         fala="Segue pra ver a próxima Ciência Bizarra amanhã. Porque esse metal..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "galio_p2.mp4"))
