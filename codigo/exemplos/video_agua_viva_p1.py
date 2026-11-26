"""Água-viva imortal (Turritopsis dohrnii), Parte 1 (BICHOS INSANOS #11). Formato v3 + ESTRATÉGIA DA SEMANA 23/11
(20–28 s, fato chocante no 1º segundo, 1 frase de opinião da MAIA). Convite sem a palavra proibida.
Fatos (Natural History Museum de Londres; AMNH; NYT 2012): a Turritopsis dohrnii tem sino de ~4,5 mm; quando
envelhece, se fere ou passa fome, encolhe, vira uma bolinha (cisto) e se transforma de novo em pólipo (a fase
"bebê" fixa no fundo), recomeçando o ciclo de vida; o pesquisador Shin Kubota (Univ. de Kyoto) relatou ter visto
a mesma colônia rejuvenescer 10 vezes em 2 anos."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O
import idioma

SERIE = "BICHOS INSANOS #11"
SINO = (255, 205, 225); SINO2 = (240, 160, 195); ESTOM = (225, 40, 70)
TENT = (255, 225, 235)
MAR1 = (10, 60, 110); MAR2 = (3, 15, 45)
POLIPO = (240, 120, 150); TALO = (200, 150, 120)


def etiqueta(d, parte="P1"):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def agua_viva(d, cx, cy, s=1.0, T=0.0, encolhe=0.0):
    """Água-viva em sino com estômago vermelho em cruz e tentáculos ondulando. encolhe 0..1 recolhe os tentáculos."""
    w = 170 * s * (1 - 0.35 * encolhe); h = 130 * s * (1 - 0.35 * encolhe)
    pulso = 1 + math.sin(T * 4) * 0.05
    w *= pulso
    nt = 14
    L = 260 * s * (1 - encolhe)
    for i in range(nt):
        x = cx - w * 0.9 + i * (w * 1.8) / (nt - 1)
        pts = []
        for k in range(8):
            yy = cy + h * 0.15 + k * L / 7
            pts.append((x + math.sin(T * 3 + k * 0.8 + i) * 14 * s * (k / 7), yy))
        if L > 5:
            d.line(pts, fill=TENT, width=max(2, int(5 * s)))
    d.chord([cx - w, cy - h, cx + w, cy + h * 0.6], 180, 360, fill=SINO, outline=O, width=max(3, int(7 * s)))
    d.rectangle([cx - w + 4, cy - h * 0.2 + 2, cx + w - 4, cy + h * 0.25], fill=SINO2)
    d.line([(cx - w, cy - h * 0.2 + 1), (cx - w, cy + h * 0.25), (cx + w, cy + h * 0.25), (cx + w, cy - h * 0.2 + 1)],
           fill=O, width=max(3, int(7 * s)))
    # estômago vermelho em cruz
    r = 38 * s * (1 - 0.3 * encolhe)
    d.ellipse([cx - r, cy - h * 0.55 - r * 0.5, cx + r, cy - h * 0.55 + r * 1.3], fill=ESTOM, outline=O, width=max(2, int(4 * s)))
    for a in (0, 1.57, 3.14, 4.71):
        d.line([(cx, cy - h * 0.35), (cx + math.cos(a) * r * 1.6, cy - h * 0.35 + math.sin(a) * r * 0.6)], fill=ESTOM, width=max(3, int(8 * s)))
    # olhinhos
    for dx in (-0.35, 0.35):
        ex, ey = cx + w * dx, cy - h * 0.05
        d.ellipse([ex - 13 * s, ey - 13 * s, ex + 13 * s, ey + 13 * s], fill=(255, 255, 255), outline=O, width=3)
        d.ellipse([ex - 5 * s, ey - 5 * s, ex + 5 * s, ey + 5 * s], fill=O)


def polipo(d, x, y, s=1.0, T=0.0):
    """Pólipo: talinho fixo no chão com cabecinhas cheias de tentáculos curtos (a fase 'bebê')."""
    d.line([(x - 70 * s, y), (x + 70 * s, y)], fill=O, width=max(4, int(10 * s)))
    for k, (dx, hh) in enumerate([(-40, 120), (0, 170), (45, 110)]):
        bx = x + dx * s + math.sin(T * 2 + k) * 6 * s
        by = y - hh * s
        d.line([(x + dx * s * 0.5, y), (bx, by)], fill=O, width=max(6, int(16 * s)))
        d.line([(x + dx * s * 0.5, y), (bx, by)], fill=TALO, width=max(3, int(9 * s)))
        for j in range(8):
            a = -3.14 + j * 0.45 + math.sin(T * 3 + j) * 0.1
            d.line([(bx, by), (bx + math.cos(a) * 34 * s, by + math.sin(a) * 34 * s)], fill=POLIPO, width=max(2, int(5 * s)))
        d.ellipse([bx - 16 * s, by - 14 * s, bx + 16 * s, by + 14 * s], fill=POLIPO, outline=O, width=3)


def g_bebe(d, img, t, T, label=True):
    etiqueta(d)
    # água-viva adulta à esquerda, seta curva, pólipo bebê à direita — já em ação no 1º quadro
    agua_viva(d, 330, 700, 0.95, T)
    k = min(1.0, 0.6 + t / 0.8)
    seta(d, 520, 760, 520 + 220 * k, 760 + 240 * k, AMARELO, 16)
    d.rectangle([640, 1150, 1000, 1180], fill=(120, 90, 70), outline=O, width=5)
    polipo(d, 830, 1150, 1.3, T)
    brilhos(d, 830, 990, 120, T, 8, AMARELO)
    if label:
        kk = pop(min(1, max(0, t - 0.4) / 0.5))
        if kk > 0.05:
            rotulo(d, 330, 1080, "ADULTA", int(46 * kk) + 1, (255, 255, 255))
            rotulo(d, 830, 1225, "BEBÊ DE NOVO", int(46 * kk) + 1, AMARELO)


def c_unha(d, img, t, T):
    selo(d)
    # dedo gigante com a unha e a água-viva minúscula do lado
    pele = (240, 190, 150)
    d.rounded_rectangle([150, 640, 560, 1260], radius=190, fill=pele, outline=O, width=8)
    d.rounded_rectangle([230, 680, 480, 920], radius=80, fill=(255, 225, 215), outline=O, width=6)
    k = ease(t / 0.8)
    agua_viva(d, 780, 1000 - 60 * k, 0.32, T)
    seta(d, 780, 830, 780, 920, CIANO, 10)
    kk = pop(min(1, max(0, t - 0.3) / 0.5))
    if kk > 0.05:
        rotulo(d, 780, 760, idioma.num(4.5, 1) + " MM", int(64 * kk) + 1, CIANO, traduzir=False)
        rotulo(d, 355, 1000, "UNHA", int(48 * kk) + 1, (255, 255, 255))


def c_renasce(d, img, t, T):
    selo(d)
    # 3 etapas: adulta → bolinha → pólipo
    e1 = pop(min(1, t / 0.5)); e2 = pop(min(1, max(0, t - 1.0) / 0.5)); e3 = pop(min(1, max(0, t - 2.0) / 0.5))
    agua_viva(d, 200, 700, 0.55, T, encolhe=0.0)
    rotulo(d, 200, 900, "VELHA", 40, (255, 255, 255))
    rotulo(d, 200, 950, "OU COM FOME", 34, (255, 255, 255))
    if e2 > 0.05:
        seta(d, 310, 720, 430, 720, AMARELO, 12)
        r = 55 * e2
        d.ellipse([540 - r, 720 - r, 540 + r, 720 + r], fill=SINO2, outline=O, width=6)
        d.ellipse([540 - r * 0.4, 720 - r * 0.4, 540 + r * 0.4, 720 + r * 0.4], fill=ESTOM)
        rotulo(d, 540, 900, "BOLINHA", 40, SINO)
    if e3 > 0.05:
        seta(d, 650, 720, 770, 720, AMARELO, 12)
        d.rectangle([780, 1010, 1040, 1035], fill=(120, 90, 70), outline=O, width=4)
        polipo(d, 900, 1010, 0.9 * e3 + 0.05, T)
        rotulo(d, 900, 1090, "PÓLIPO", 44, AMARELO)
        rotulo(d, 900, 1140, "(FASE BEBÊ)", 34, AMARELO)


def c_dez(d, img, t, T):
    selo(d)
    # seta circular de "reiniciar" girando, com a água-viva no centro e o contador
    cx, cy, R = 540, 820, 270
    ang = T * 90
    d.arc([cx - R, cy - R, cx + R, cy + R], int(ang) % 360, int(ang + 300) % 360, fill=CIANO, width=30)
    a = math.radians(ang + 300)
    px, py = cx + math.cos(a) * R, cy + math.sin(a) * R
    d.polygon([(px + math.cos(a) * 45, py + math.sin(a) * 45), (px - math.cos(a) * 45, py - math.sin(a) * 45),
               (px + math.cos(a + 1.57) * 60, py + math.sin(a + 1.57) * 60)], fill=CIANO, outline=O)
    agua_viva(d, cx, cy - 40, 0.55, T)
    contador(d, cx, 1150, 10, t, 1.4, 96, "x", AMARELO)
    kk = pop(min(1, max(0, t - 1.2) / 0.5))
    if kk > 0.05:
        rotulo(d, cx, 1240, "EM 2 ANOS · JAPÃO", int(42 * kk) + 1, (255, 255, 255))


def c_cta(d, img, t, T):
    g_bebe(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="VIRA BEBÊ!", titulo_y=400, desenho=g_bebe, fundo=(MAR1, MAR2),
         fala="Essa água-viva não morre de velhice: vira bebê de novo! E o fim é o mais louco."),
    dict(tipo="fato", titulo="TURRITOPSIS", desenho=c_unha, fundo=((12, 80, 120), MAR2),
         fala="É a Turritopsis, menor que uma unha. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="RENASCE", desenho=c_renasce, fundo=((40, 30, 90), (10, 8, 35)),
         fala="velha ou com fome, ela encolhe, vira uma bolinha e renasce bebê."),
    dict(tipo="fato", titulo="10 VEZES", desenho=c_dez, fundo=((70, 20, 70), (20, 5, 25)),
         fala="No Japão, um cientista viu ela renascer dez vezes em dois anos. Ela reinicia a vida!"),
    dict(tipo="cta", titulo="VIRA BEBÊ!", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue a Maia pra ver a parte dois às seis da tarde, ainda mais louca! Tudo por causa dessa água-viva..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "agua_viva_p1.mp4"))
