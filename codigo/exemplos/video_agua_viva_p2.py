"""Água-viva imortal (Turritopsis dohrnii), Parte 2 (BICHOS INSANOS #11). Importa desenhos de video_agua_viva_p1.
Fatos: Miglietta & Lessios 2009 (Biological Invasions, "A silent invasion"): a T. dohrnii se espalhou pelos
oceanos do mundo, provavelmente levada na água de lastro dos navios. Pascual-Torner et al. 2022 (PNAS): o genoma
da T. dohrnii tem cópias extras (genes duplicados) ligados a reparo e proteção do DNA e manutenção dos telômeros.
NHM/AMNH: ela não é imortal de verdade — morre comida por predadores ou por doenças."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, terra, O
from video_agua_viva_p1 import etiqueta, selo, agua_viva, polipo, SINO, ESTOM, MAR1, MAR2

CASCO = (200, 50, 50); CASCO2 = (240, 240, 240); AGUA = (40, 130, 200)


def navio(d, cx, cy, s=1.0, T=0.0, tanque=False):
    bal = math.sin(T * 1.5) * 6 * s
    d.polygon([(cx - 300 * s, cy - 40 * s + bal), (cx + 300 * s, cy - 40 * s + bal), (cx + 240 * s, cy + 90 * s + bal),
               (cx - 260 * s, cy + 90 * s + bal)], fill=CASCO, outline=O)
    d.rectangle([cx - 300 * s, cy - 70 * s + bal, cx + 300 * s, cy - 40 * s + bal], fill=CASCO2, outline=O, width=5)
    for i, c in enumerate([(255, 196, 30), (35, 210, 225), (120, 200, 90), (255, 120, 90)]):
        x = cx - 250 * s + i * 95 * s
        d.rectangle([x, cy - 140 * s + bal, x + 85 * s, cy - 72 * s + bal], fill=c, outline=O, width=4)
    d.rectangle([cx + 150 * s, cy - 200 * s + bal, cx + 260 * s, cy - 72 * s + bal], fill=CASCO2, outline=O, width=5)
    if tanque:
        d.rectangle([cx - 200 * s, cy - 25 * s + bal, cx + 120 * s, cy + 70 * s + bal], fill=AGUA, outline=O, width=5)
        for k in range(3):
            agua_viva(d, cx - 140 * s + k * 110 * s, cy + 10 * s + bal, 0.17 * s, T + k)


def g_mundo(d, img, t, T, label=True):
    etiqueta(d, "P2")
    terra(d, 540, 880, 230, T, rosto=False)
    # águas-vivas aparecendo em volta do planeta
    for i in range(6):
        a = i / 6 * 6.283 + T * 0.4
        k = pop(min(1, max(0, t * 1.5 + 0.6 - i * 0.12)))
        if k > 0.05:
            agua_viva(d, 540 + math.cos(a) * 340, 860 + math.sin(a) * 215, 0.25 * k + 0.01, T + i)
    if label:
        kk = pop(min(1, max(0, t - 0.5) / 0.5))
        if kk > 0.05:
            rotulo(d, 540, 1225, "NO MUNDO TODO", int(50 * kk) + 1, AMARELO)


def c_navio(d, img, t, T):
    selo(d)
    d.rectangle([0, 1000, 1080, 1260], fill=(20, 90, 150))
    for i in range(10):
        x = (i * 130 + T * 40) % 1180 - 50
        d.arc([x, 985, x + 80, 1015], 180, 360, fill=(160, 220, 255), width=5)
    k = ease(t / 1.2)
    navio(d, 1300 - 760 * k, 960, 1.0, T, tanque=True)
    kk = pop(min(1, max(0, t - 0.8) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 640, "CARONA NO NAVIO", int(56 * kk) + 1, CIANO)
        rotulo(d, 540, 1200, "ÁGUA DO TANQUE", int(44 * kk) + 1, (255, 255, 255))


def c_dna(d, img, t, T):
    selo(d)
    # dupla hélice com pedaços destacados "x2"
    cx = 540
    for i in range(20):
        y = 560 + i * 30
        a = T * 2 + i * 0.5
        x1 = cx + math.sin(a) * 170; x2 = cx - math.sin(a) * 170
        cor = AMARELO if i in (6, 7, 14, 15) else (180, 140, 255)
        d.line([(x1, y), (x2, y)], fill=cor, width=8)
        d.ellipse([x1 - 14, y - 14, x1 + 14, y + 14], fill=(35, 210, 225), outline=O, width=3)
        d.ellipse([x2 - 14, y - 14, x2 + 14, y + 14], fill=(255, 120, 160), outline=O, width=3)
    kk = pop(min(1, max(0, t - 0.6) / 0.5))
    if kk > 0.05:
        rotulo(d, 870, 770, "x2", int(80 * kk) + 1, AMARELO, traduzir=False)
        rotulo(d, 870, 1010, "x2", int(80 * kk) + 1, AMARELO, traduzir=False)
        rotulo(d, 540, 1235, "GENES QUE CONSERTAM", int(44 * kk) + 1, AMARELO)
    rotulo(d, 200, 600, "2022", 56, (255, 255, 255), traduzir=False)


def c_peixe(d, img, t, T):
    selo(d)
    # peixe grande de boca aberta engolindo a água-viva
    k = ease(t / 1.4)
    jx = 760 - 160 * k
    if k < 0.95:
        agua_viva(d, jx, 760, 0.45, T)
    px, py = 370, 820
    abre = 0.6 if k < 0.9 else 0.15
    d.pieslice([px - 230, py - 170, px + 230, py + 170], int(abre * 40), int(360 - abre * 40), fill=(90, 170, 90), outline=O, width=8)
    d.polygon([(px - 210, py), (px - 330, py - 120), (px - 330, py + 120)], fill=(70, 140, 70), outline=O)
    d.ellipse([px + 20, py - 110, px + 80, py - 50], fill=(255, 255, 255), outline=O, width=4)
    d.ellipse([px + 40, py - 90, px + 62, py - 68], fill=O)
    if k >= 0.9:
        kk = pop(min(1, (t - 1.3) / 0.4))
        rotulo(d, 720, 700, "NHAC!", int(80 * kk) + 1, AMARELO)
        rotulo(d, 540, 1180, "NÃO É INVENCÍVEL", int(46 * kk) + 1, (255, 120, 120))


def c_cta(d, img, t, T):
    g_mundo(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="INVASORA!", titulo_y=400, desenho=g_mundo, fundo=(MAR1, MAR2),
         fala="Essa água-viva que vira bebê está invadindo o mundo! E o segredo está no DNA."),
    dict(tipo="fato", titulo="NOS NAVIOS", desenho=c_navio, fundo=((15, 70, 120), MAR2),
         fala="Ela pega carona na água dos navios. Segue a Maia, porque fica mais louco:"),
    dict(tipo="fato", titulo="NO DNA", desenho=c_dna, fundo=((40, 25, 90), (10, 6, 35)),
         fala="em 2022, leram o DNA dela: vários genes que consertam o DNA vêm em dobro!"),
    dict(tipo="fato", titulo="MAS...", desenho=c_peixe, fundo=((20, 70, 60), (5, 20, 20)),
         fala="Mas imortal não é invencível: se um peixe comer, acabou. Eu queria uma armadura!"),
    dict(tipo="cta", titulo="INVASORA!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. E lembra: essa água-viva..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "agua_viva_p2.mp4"))
