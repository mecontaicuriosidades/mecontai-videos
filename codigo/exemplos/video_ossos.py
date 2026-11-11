"""Ossos: bebê tem ~300, adulto 206, você é mais alto de manhã."""
import math, sys
from motor import render, pop, ease, fnt, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, seta, O

OSSO = (245, 238, 220)


def osso(d, x0, y0, x1, y1, w=34, cor=OSSO):
    d.line([(x0, y0), (x1, y1)], fill=O, width=w + 10)
    for (x, y) in ((x0, y0), (x1, y1)):
        ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        for s in (-1, 1):
            cx, cy = x + math.cos(ang) * w * 0.55 * s, y + math.sin(ang) * w * 0.55 * s
            d.ellipse([cx - w * 0.75, cy - w * 0.75, cx + w * 0.75, cy + w * 0.75], fill=cor, outline=O, width=5)
    d.line([(x0, y0), (x1, y1)], fill=cor, width=w)


def c_bebe(d, img, t, T):
    # bebezinho
    d.ellipse([400, 520, 680, 800], fill=(252, 214, 188), outline=O, width=8)
    olhos(d, 540, 640, T, 90, 20); sorriso(d, 540, 710, 34)
    d.ellipse([360, 790, 720, 1050], fill=(255, 200, 220), outline=O, width=8)
    contador(d, 540, 1170, 300, t, 2.2, 110, "", AMARELO)
    rotulo(d, 540, 1240, "OSSOS (MAIS OU MENOS)", 36)


def c_fundem(d, img, t, T):
    k = ease((t - 0.8) / 2.5)
    gap = 120 * (1 - k)
    osso(d, 240, 760, 540 - gap, 760, 44)
    osso(d, 540 + gap, 760, 840, 760, 44)
    if t > 1: seta(d, 200, 900, 880, 900, CIANO, 12)
    if t > 2.8: rotulo(d, 540, 1050, "VIRAM UM SÓ!", 64, AMARELO)


def c_adulto(d, img, t, T):
    # esqueleto simplificado
    cx = 540
    d.ellipse([cx - 80, 440, cx + 80, 600], fill=OSSO, outline=O, width=7)
    d.ellipse([cx - 45, 495, cx - 15, 525], fill=O); d.ellipse([cx + 15, 495, cx + 45, 525], fill=O)
    for k in range(7): d.arc([cx - 110, 620 + k * 32, cx + 110, 700 + k * 32], 200, 340, fill=OSSO, width=12)
    osso(d, cx, 610, cx, 900, 26)
    for s in (-1, 1):
        osso(d, cx + s * 100, 640, cx + s * 220, 840, 22)
        osso(d, cx + s * 50, 920, cx + s * 80, 1150, 26)
    contador(d, 840, 1170, 206, t, 2, 100, "", CIANO)


def c_maos(d, img, t, T):
    # mão: palma + dedos com articulações
    d.rounded_rectangle([380, 760, 700, 1060], 70, fill=(252, 214, 188), outline=O, width=8)
    for i in range(4):
        x = 410 + i * 80
        d.rounded_rectangle([x, 480 + abs(i - 1.5) * 40, x + 64, 790], 32, fill=(252, 214, 188), outline=O, width=8)
        for k in range(3): d.ellipse([x + 22, 540 + abs(i - 1.5) * 40 + k * 80, x + 42, 560 + abs(i - 1.5) * 40 + k * 80], fill=OSSO, outline=O, width=3)
    d.rounded_rectangle([660, 800, 860, 870], 32, fill=(252, 214, 188), outline=O, width=8)
    if t > 1.0: rotulo(d, 540, 1150, "106 DOS 206 OSSOS", 58, AMARELO)


def c_estribo(d, img, t, T):
    # orelha + estribo ampliado
    d.ellipse([140, 520, 420, 900], fill=(252, 214, 188), outline=O, width=8)
    d.arc([190, 580, 370, 840], 120, 400, fill=O, width=8)
    if t > 0.8:
        s = pop((t - 0.8) / 0.5)
        x, y = 720, 720
        d.polygon([(x - 120 * s, y + 110 * s), (x + 120 * s, y + 110 * s), (x + 40 * s, y - 110 * s), (x - 40 * s, y - 110 * s)],
                  outline=O, fill=OSSO, width=8)
        d.polygon([(x - 70 * s, y + 85 * s), (x + 70 * s, y + 85 * s), (x + 22 * s, y - 70 * s), (x - 22 * s, y - 70 * s)],
                  fill=(250, 200, 190))
        d.ellipse([x - 50 * s, y - 150 * s, x + 50 * s, y - 90 * s], fill=OSSO, outline=O, width=6)
        seta(d, 420, 720, 570, 720, CIANO, 10)
    if t > 1.8: rotulo(d, 720, 1000, "≈ 3 mm".replace("≈", "~"), 70, AMARELO)


def c_altura(d, img, t, T):
    # régua + boneco de manhã/noite
    d.rectangle([150, 450, 230, 1200], fill=(255, 230, 120), outline=O, width=6)
    for k in range(16): d.line([(150, 470 + k * 46), (190 if k % 2 else 210, 470 + k * 46)], fill=O, width=4)
    manha = (t % 4) < 2
    topo = 560 if manha else 600
    d.ellipse([480, topo, 620, topo + 140], fill=(252, 214, 188), outline=O, width=7)
    olhos(d, 550, topo + 60, T, 50, 13)
    d.rounded_rectangle([460, topo + 140, 640, 1000], 50, fill=CIANO, outline=O, width=7)
    for s in (-1, 1): d.line([(550 + s * 50, 1000), (550 + s * 60, 1200)], fill=O, width=36)
    d.line([(240, topo), (470, topo)], fill=(255, 80, 80), width=6)
    rotulo(d, 830, 700, "MANHÃ" if manha else "NOITE", 64, AMARELO if manha else CIANO)
    if t > 1: rotulo(d, 830, 820, "+1 cm", 80, (120, 255, 120))


CENAS = [
    dict(tipo="gancho", titulo="VOCÊ JÁ TEVE MAIS OSSOS", desenho=lambda d, img, t, T: c_adulto(d, img, 99, T), fundo=((40, 60, 120), (12, 18, 50)),
         fala="Você sabia que já teve quase cem ossos a mais do que tem hoje? E de manhã você é mais alto do que à noite! Eu explico."),
    dict(tipo="fato", titulo="BEBÊ: CERCA DE 300 OSSOS", desenho=c_bebe, fundo=((255, 190, 210), (200, 120, 170)),
         fala="Um bebê nasce com cerca de trezentos ossos. Muitos deles ainda são pedacinhos separados, em parte feitos de cartilagem."),
    dict(tipo="fato", titulo="ELES SE JUNTAM", desenho=c_fundem, fundo=((60, 80, 140), (25, 35, 80)),
         fala="Conforme a gente cresce, vários desses ossos se fundem e viram um só. É o que acontece no crânio, na bacia e na base da coluna."),
    dict(tipo="fato", titulo="ADULTO: 206 OSSOS", desenho=c_adulto, fundo=((30, 40, 80), (10, 15, 40)), estrelas=True,
         fala="No fim, um adulto fica com duzentos e seis ossos. E eles são vivos: o esqueleto inteiro vai sendo renovado aos pouquinhos ao longo da vida."),
    dict(tipo="fato", titulo="MAIS DA METADE NAS MÃOS E PÉS", desenho=c_maos, fundo=((255, 170, 90), (220, 100, 60)),
         fala="E sabe onde fica mais da metade deles? Nas mãos e nos pés! São cento e seis ossos só ali."),
    dict(tipo="fato", titulo="O MENOR OSSO DO CORPO", desenho=c_estribo, fundo=((120, 90, 200), (50, 30, 110)),
         fala="O menor osso do corpo fica dentro da orelha. Se chama estribo e tem uns três milímetros. Ele ajuda a levar o som até o ouvido interno."),
    dict(tipo="fato", titulo="MAIS ALTO DE MANHÃ", desenho=c_altura, fundo=((150, 210, 255), (90, 150, 230)),
         fala="E o mais bizarro: você fica até um centímetro mais alto de manhã. Durante o dia, os discos entre as vértebras são comprimidos pelo peso do corpo. À noite, deitado, eles se recuperam."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Já sabia disso?",
         fala="Você já sabia que fica mais alto de manhã? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "ossos.mp4"))
