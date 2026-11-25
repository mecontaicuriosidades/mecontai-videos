"""Caramujo-cone, Parte 2 (BICHOS INSANOS #10). Importa desenhos de video_caramujo_cone_p1.
Fatos: Conus geographus solta insulina (parecida com a de peixe) na água junto com o veneno; o açúcar
no sangue dos peixes cai e eles ficam lentos/tontos; o caracol engole o peixe com a boca em funil
que abre feito rede (Safavi-Hemami et al., PNAS 2015; Science News 19/01/2015). Do veneno de outro
cone (Conus magus) saiu a ziconotida (Prialt), remédio para dor crônica forte aprovado nos EUA (FDA) em
dez/2004, descrito como muito mais potente que a morfina."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_caramujo_cone_p1 import etiqueta, selo, areia, concha, CORPO, TROMBA, VENENO, MAR1, MAR2

INSU = (130, 220, 255)
PEIXE = (255, 170, 60); PEIXE2 = (255, 130, 40)


def peixe(d, cx, cy, s=1.0, T=0.0, tonto=False):
    ond = 0 if tonto else math.sin(T * 6) * 8 * s
    d.ellipse([cx - 90 * s, cy - 50 * s, cx + 90 * s, cy + 50 * s], fill=PEIXE, outline=O, width=6)
    d.polygon([(cx + 80 * s, cy), (cx + 150 * s, cy - 55 * s + ond), (cx + 150 * s, cy + 55 * s + ond)], fill=PEIXE2, outline=O)
    ex, ey = cx - 45 * s, cy - 5 * s
    d.ellipse([ex - 18 * s, ey - 18 * s, ex + 18 * s, ey + 18 * s], fill=(255, 255, 255), outline=O, width=3)
    if tonto:  # olho em espiral
        for k in range(3):
            r = (4 + k * 5) * s
            d.arc([ex - r, ey - r, ex + r, ey + r], int(T * 300 + k * 90) % 360, int(T * 300 + k * 90 + 250) % 360, fill=O, width=3)
        for k in range(3):  # estrelinhas girando
            a = T * 3 + k * 2.1
            sx, sy = cx - 20 * s + math.cos(a) * 70 * s, cy - 90 * s + math.sin(a) * 18 * s
            rotulo(d, sx, sy, "*", int(40 * s), AMARELO, traduzir=False)
    else:
        d.ellipse([ex - 6 * s, ey - 6 * s, ex + 6 * s, ey + 6 * s], fill=O)


def nuvem_insulina(d, cx, cy, r, T, n=16):
    for i in range(n):
        a = i / n * 6.283 + T * 0.5
        rr = r * (0.4 + 0.6 * ((i * 37) % 10) / 10)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.6
        q = 10 + (i % 3) * 5
        d.ellipse([x - q, y - q, x + q, y + q], outline=INSU, width=4)


def g_insulina(d, img, t, T, label=True):
    etiqueta(d, "P2")
    areia(d, 1180)
    concha(d, 300, 990, 0.9, T)
    nuvem_insulina(d, 720, 760, 260, T)
    peixe(d, 740, 760, 1.4, T, tonto=t > 0.6 or not label)
    if label:
        k = pop(min(1, max(0, t - 0.4) / 0.5))
        if k > 0.05:
            rotulo(d, 640, 1225, "INSULINA NA ÁGUA", int(46 * k) + 1, INSU)


def c_acucar(d, img, t, T):
    selo(d)
    # medidor de açúcar despencando + peixe
    x0, y0, y1 = 220, 560, 1150
    d.rounded_rectangle([x0 - 60, y0, x0 + 60, y1], radius=40, fill=(30, 30, 50), outline=O, width=6)
    nivel = 0.9 - 0.75 * ease(t / 1.6)
    yt = y1 - (y1 - y0 - 20) * nivel
    d.rounded_rectangle([x0 - 46, yt, x0 + 46, y1 - 14], radius=30, fill=(255, 220, 120))
    seta(d, x0 + 110, 640, x0 + 110, 1000, (255, 90, 90), 16)
    rotulo(d, x0, y1 + 50, "AÇÚCAR", 46, AMARELO)
    peixe(d, 700, 830, 1.3, T, tonto=t > 1.2)
    nuvem_insulina(d, 700, 830, 300, T, 12)
    k = pop(min(1, max(0, t - 1.0) / 0.5))
    if k > 0.05:
        rotulo(d, 700, 1080, "DESPENCA!", int(56 * k) + 1, (255, 100, 100))


def c_rede(d, img, t, T):
    selo(d)
    areia(d, 1190)
    concha(d, 260, 1040, 0.8, T)
    # boca em funil abrindo feito rede e engolindo o peixe tonto
    k = ease(t / 1.2)
    bx, by = 470, 920
    abre = 120 + 200 * k
    d.polygon([(bx, by), (bx + 380, by - abre), (bx + 380, by + abre * 0.6)], fill=TROMBA, outline=O)
    for j in range(5):  # trama de rede
        u = (j + 1) / 6
        d.line([(bx + 380 * u, by - abre * u), (bx + 380 * u, by + abre * 0.6 * u)], fill=CORPO, width=6)
    d.ellipse([bx + 340, by - abre, bx + 420, by + abre * 0.6], outline=O, width=7)
    g = ease(max(0, t - 1.2) / 1.2)
    peixe(d, 830 - 300 * g, 760 + 120 * g, 1.0 - 0.5 * g, T, tonto=True)
    kk = pop(min(1, max(0, t - 0.3) / 0.5))
    if kk > 0.05:
        rotulo(d, 640, 580, "BOCA DE REDE", int(52 * kk) + 1, AMARELO)


def c_remedio(d, img, t, T):
    selo(d)
    # gota de veneno vira frasco de remédio
    k = ease(t / 1.0)
    gx = 260 + 0 * k
    d.ellipse([gx - 70, 760, gx + 70, 920], fill=VENENO, outline=O, width=6)
    d.polygon([(gx - 55, 800), (gx, 680), (gx + 55, 800)], fill=VENENO, outline=O)
    rotulo(d, gx, 980, "VENENO", 44, VENENO)
    seta(d, 380, 820, 560 + 40 * k, 820, AMARELO, 16)
    fx = 800
    d.rounded_rectangle([fx - 110, 660, fx + 110, 1000], radius=26, fill=(240, 245, 255), outline=O, width=7)
    d.rectangle([fx - 80, 610, fx + 80, 660], fill=(60, 150, 230), outline=O, width=6)
    d.rectangle([fx - 110, 760, fx + 110, 880], fill=(60, 150, 230))
    d.line([(fx, 785), (fx, 855)], fill=(255, 255, 255), width=16)
    d.line([(fx - 35, 820), (fx + 35, 820)], fill=(255, 255, 255), width=16)
    brilhos(d, fx, 820, 170, T, 8, AMARELO)
    kk = pop(min(1, max(0, t - 0.8) / 0.5))
    if kk > 0.05:
        rotulo(d, fx, 1060, "REMÉDIO", int(50 * kk) + 1, CIANO)
        rotulo(d, 540, 1180, "MAIS FORTE QUE MORFINA", int(44 * kk) + 1, AMARELO)


def c_cta(d, img, t, T):
    g_insulina(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="INSULINA!", titulo_y=400, desenho=g_insulina, fundo=(MAR1, MAR2),
         fala="Esse caracol do arpão de veneno caça peixe com insulina! E o final surpreende."),
    dict(tipo="fato", titulo="ARMA DOCE", desenho=c_acucar, fundo=((20, 50, 100), (5, 12, 35)),
         fala="Ele solta insulina na água, e o açúcar do peixe despenca. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="ENGOLE!", desenho=c_rede, fundo=((10, 90, 110), MAR2),
         fala="o peixe fica tonto, e o caracol abre a boca feito rede e engole ele inteiro."),
    dict(tipo="fato", titulo="REMÉDIO!", desenho=c_remedio, fundo=((40, 30, 90), (12, 8, 35)),
         fala="E o veneno virou remédio pra dor forte, mais potente que morfina. Do veneno à cura!"),
    dict(tipo="cta", titulo="INSULINA!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. Tudo isso vem desse caracol..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "caramujo_cone_p2.mp4"))
