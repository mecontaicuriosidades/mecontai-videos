"""Projeto Natick (TECNOLOGIA INSANA #6). Formato v3 + ESTRATÉGIA DA SEMANA 23/11.
Fatos (Microsoft News 14/09/2020; BBC; GCN): em 2018 a Microsoft afundou um data center (cilindro de ~12 m,
864 servidores) a ~36 m (117 pés) de profundidade perto das Ilhas Órcadas, na Escócia; foi retirado em 2020,
depois de 2 anos; a taxa de falhas foi 1/8 da de servidores iguais em terra; a Microsoft atribui isso à
atmosfera de nitrogênio (menos corrosiva que o oxigênio) e à ausência de pessoas mexendo/esbarrando nos
equipamentos."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O
import idioma

SERIE = "TECNOLOGIA INSANA #6"
MAR1 = (10, 70, 110); MAR2 = (3, 18, 40)
TUBO = (215, 225, 235); TUBO2 = (160, 175, 190); AREIA = (150, 130, 90)
LED = [(60, 255, 120), (35, 210, 225), (255, 196, 30)]


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def tubo(d, cx, cy, s=1.0, T=0.0, corte=False):
    """Cilindro deitado sobre uma base, com tampas redondas. corte mostra os racks com luzes por dentro."""
    w, h = 330 * s, 110 * s
    d.rectangle([cx - w * 0.8, cy + h, cx + w * 0.8, cy + h + 40 * s], fill=(90, 90, 100), outline=O, width=5)
    for dx in (-0.6, 0, 0.6):
        d.line([(cx + w * dx, cy + h), (cx + w * dx, cy + h + 40 * s)], fill=O, width=5)
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=int(h), fill=TUBO, outline=O, width=max(4, int(8 * s)))
    if corte:
        d.rounded_rectangle([cx - w + 50 * s, cy - h + 22 * s, cx + w - 50 * s, cy + h - 22 * s], radius=20,
                            fill=(25, 30, 45), outline=O, width=5)
        cols = 9
        for i in range(cols):
            x = cx - w + 75 * s + i * (2 * w - 150 * s) / (cols - 1)
            d.rectangle([x - 18 * s, cy - h + 35 * s, x + 18 * s, cy + h - 35 * s], fill=(55, 60, 80), outline=O, width=2)
            for j in range(5):
                y = cy - h + 50 * s + j * (2 * h - 100 * s) / 4
                on = math.sin(T * 7 + i * 1.7 + j * 2.3) > -0.2
                if on:
                    d.ellipse([x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s], fill=LED[(i + j) % 3])
    else:
        for i in range(5):
            x = cx - w * 0.6 + i * w * 0.3
            d.line([(x, cy - h + 8), (x, cy + h - 8)], fill=TUBO2, width=max(3, int(6 * s)))
        d.ellipse([cx + w - 70 * s, cy - 45 * s, cx + w - 10 * s, cy + 45 * s], fill=TUBO2, outline=O, width=5)


def peixinho(d, x, y, s, cor, lado=1):
    d.ellipse([x - 40 * s, y - 20 * s, x + 40 * s, y + 20 * s], fill=cor, outline=O, width=3)
    d.polygon([(x - 40 * s * lado, y), (x - 70 * s * lado, y - 22 * s), (x - 70 * s * lado, y + 22 * s)], fill=cor, outline=O)
    d.ellipse([x + 18 * s * lado - 5, y - 9, x + 18 * s * lado + 5, y + 1], fill=O)


def fundo_mar(d, T):
    d.rectangle([0, 1120, 1080, 1290], fill=AREIA)
    for i in range(6):
        x = 80 + i * 190
        d.line([(x, 1120), (x + math.sin(T * 2 + i) * 20, 1010)], fill=(60, 150, 80), width=10)
    for i in range(8):
        y = 1100 - ((T * 120 + i * 140) % 560)
        x = 160 + (i * 113) % 760
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(170, 225, 255), width=3)


def g_tubo(d, img, t, T, label=True):
    etiqueta(d)
    fundo_mar(d, T)
    tubo(d, 540, 900, 1.15, T, corte=True)
    peixinho(d, (T * 90) % 1300 - 110, 640, 0.9, (255, 150, 60))
    peixinho(d, 1180 - (T * 70) % 1300, 1240, 0.7, (255, 210, 80), lado=-1)
    if label:
        kk = pop(min(1, max(0, t - 0.3) / 0.5))
        if kk > 0.05:
            rotulo(d, 540, 720, "2 ANOS NO MAR", int(50 * kk) + 1, (255, 255, 255))
            rotulo(d, 540, 1080, "8x MENOS DEFEITOS", int(50 * kk) + 1, AMARELO)


def c_escocia(d, img, t, T):
    selo(d)
    # superfície com navio-guindaste baixando o tubo
    d.rectangle([0, 700, 1080, 1290], fill=(15, 80, 130))
    for i in range(10):
        x = (i * 130 + T * 40) % 1180 - 50
        d.arc([x, 685, x + 80, 715], 180, 360, fill=(160, 220, 255), width=5)
    d.polygon([(560, 640), (1000, 640), (960, 720), (600, 720)], fill=(200, 60, 50), outline=O)
    d.line([(900, 640), (760, 520), (700, 520)], fill=AMARELO, width=12)
    k = ease(t / 1.6)
    y = 760 + 340 * k
    d.line([(700, 520), (700, y - 70)], fill=(230, 230, 230), width=5)
    tubo(d, 700, y, 0.5, T)
    kk = pop(min(1, max(0, t - 0.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 260, 590, "ESCÓCIA · 2018", int(46 * kk) + 1, CIANO)
        rotulo(d, 260, 660, "MICROSOFT", int(46 * kk) + 1, (255, 255, 255), traduzir=False)


def c_servidores(d, img, t, T):
    selo(d)
    tubo(d, 540, 830, 1.2, T, corte=True)
    seta(d, 120, 1010, 960, 1010, (255, 255, 255), 8)
    seta(d, 960, 1010, 120, 1010, (255, 255, 255), 8)
    rotulo(d, 540, 1060, "12 METROS", 44, (255, 255, 255))
    contador(d, 540, 640, 864, t, 1.3, 110, "", AMARELO)
    kk = pop(min(1, max(0, t - 1.0) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1150, "SERVIDORES", int(48 * kk) + 1, AMARELO)
        rotulo(d, 540, 1230, "A 36 M DE FUNDO", int(44 * kk) + 1, CIANO)


def pessoa(d, x, y, s=1.0):
    d.ellipse([x - 35 * s, y - 150 * s, x + 35 * s, y - 80 * s], fill=(240, 190, 150), outline=O, width=5)
    d.rounded_rectangle([x - 50 * s, y - 75 * s, x + 50 * s, y + 60 * s], 20, fill=(70, 120, 200), outline=O, width=5)


def c_segredo(d, img, t, T):
    selo(d)
    # metade esquerda: moléculas de nitrogênio flutuando; direita: pessoa riscada
    d.rounded_rectangle([60, 560, 520, 1180], 40, fill=(25, 35, 60), outline=CIANO, width=6)
    for i in range(7):
        x = 150 + (i * 173) % 280 + math.sin(T * 2 + i) * 25
        y = 640 + (i * 211) % 440 + math.cos(T * 1.7 + i) * 25
        d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(120, 150, 255), outline=O, width=4)
        d.ellipse([x + 14, y - 26, x + 66, y + 26], fill=(120, 150, 255), outline=O, width=4)
    rotulo(d, 290, 1230, "NITROGÊNIO", 46, (150, 180, 255))
    pessoa(d, 790, 920, 1.6)
    kk = pop(min(1, max(0, t - 1.0) / 0.4))
    if kk > 0.05:
        d.ellipse([610, 640, 970, 1100], outline=(255, 60, 60), width=int(18 * kk) + 1)
        d.line([(670, 1040), (910, 700)], fill=(255, 60, 60), width=int(18 * kk) + 1)
        rotulo(d, 790, 1230, "SEM GENTE", int(50 * kk) + 1, (255, 120, 120))


def c_cta(d, img, t, T):
    g_tubo(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="AFUNDADO!", titulo_y=400, desenho=g_tubo, fundo=(MAR1, MAR2),
         fala="Esse computador ficou dois anos no fundo do mar e quebrou oito vezes menos! O motivo vem no fim."),
    dict(tipo="fato", titulo="PROJETO NATICK", desenho=c_escocia, fundo=((70, 130, 190), (20, 50, 90)),
         fala="Foi um teste da Microsoft, na Escócia. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="864 MÁQUINAS", desenho=c_servidores, fundo=((20, 40, 80), (5, 10, 25)),
         fala="um tubo de doze metros, com oitocentos e sessenta e quatro servidores lá dentro."),
    dict(tipo="fato", titulo="O SEGREDO", desenho=c_segredo, fundo=((40, 30, 80), (10, 8, 25)),
         fala="O segredo: nitrogênio no lugar do ar, e ninguém esbarrando nas máquinas. Genial!"),
    dict(tipo="cta", titulo="AFUNDADO!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(MAR1, MAR2),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana. E lembra: esse computador..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "natick.mp4"))
