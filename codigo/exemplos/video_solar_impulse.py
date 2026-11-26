"""Solar Impulse 2 (TECNOLOGIA INSANA #5). Formato v3 + ESTRATÉGIA DA SEMANA 23/11 (20–28 s, 1 frase de opinião).
Fatos (Solar Impulse Foundation; CBC/NBC/Fox 2015–2016): deu a volta ao mundo em 17 etapas (mar/2015 a 26/07/2016,
Abu Dhabi→Abu Dhabi, ~40 mil km) só com energia solar; envergadura de 72 m (maior que a do Boeing 747, ~68 m) e
~2.300 kg (peso de um carro); 17.248 células solares carregavam baterias de lítio para voar à noite; André Borschberg
voou de Nagoya (Japão) ao Havaí em 117 h 52 min (quase 5 dias), recorde de voo solo mais longo, cochilando ~20 min
por vez."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, sol, contador, O

SERIE = "TECNOLOGIA INSANA #5"
CEU1 = (40, 120, 200); CEU2 = (10, 40, 100)
CEL = (25, 45, 110); CEL2 = (70, 110, 200); BRANCO = (240, 240, 245)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def aviao(d, cx, cy, s=1.0, T=0.0):
    """Avião solar visto de frente-cima: asa enorme coberta de células, 4 hélices girando, cabine pequena."""
    W = 470 * s
    d.polygon([(cx - W, cy - 18 * s), (cx + W, cy - 18 * s), (cx + W - 10 * s, cy + 22 * s), (cx - W + 10 * s, cy + 22 * s)],
              fill=CEL, outline=O)
    n = 24
    for i in range(1, n):
        x = cx - W + i * 2 * W / n
        d.line([(x, cy - 16 * s), (x, cy + 20 * s)], fill=CEL2, width=max(1, int(2 * s)))
    d.line([(cx - W, cy + 2 * s), (cx + W, cy + 2 * s)], fill=CEL2, width=max(1, int(2 * s)))
    # motores e hélices
    for dx in (-0.62, -0.25, 0.25, 0.62):
        mx = cx + W * dx
        d.ellipse([mx - 16 * s, cy + 10 * s, mx + 16 * s, cy + 60 * s], fill=BRANCO, outline=O, width=max(2, int(4 * s)))
        a = T * 25 + dx * 10
        L = 45 * s
        d.line([(mx - math.cos(a) * L, cy + 62 * s - math.sin(a) * 8 * s), (mx + math.cos(a) * L, cy + 62 * s + math.sin(a) * 8 * s)],
               fill=O, width=max(3, int(7 * s)))
    # cabine/fuselagem
    d.ellipse([cx - 40 * s, cy - 10 * s, cx + 40 * s, cy + 70 * s], fill=BRANCO, outline=O, width=max(2, int(5 * s)))
    d.ellipse([cx - 22 * s, cy + 5 * s, cx + 22 * s, cy + 35 * s], fill=(120, 200, 240), outline=O, width=3)
    d.line([(cx, cy + 70 * s), (cx, cy + 180 * s)], fill=O, width=max(4, int(12 * s)))
    d.line([(cx, cy + 70 * s), (cx, cy + 180 * s)], fill=BRANCO, width=max(2, int(6 * s)))
    d.polygon([(cx - 90 * s, cy + 170 * s), (cx + 90 * s, cy + 170 * s), (cx + 70 * s, cy + 190 * s), (cx - 70 * s, cy + 190 * s)],
              fill=CEL, outline=O)


def g_sol(d, img, t, T, label=True):
    etiqueta(d)
    sol(d, 860, 640, 80, T, rosto=True)
    bob = math.sin(T * 1.5) * 12
    aviao(d, 540, 860 + bob, 1.0, T)
    # bomba de combustível riscada
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05 and label:
        bx, by = 230, 1140
        d.rounded_rectangle([bx - 55, by - 80, bx + 55, by + 80], radius=14, fill=(230, 60, 60), outline=O, width=6)
        d.rectangle([bx - 35, by - 60, bx + 35, by - 20], fill=(255, 255, 255), outline=O, width=4)
        L = 95 * k
        d.line([(bx - L, by - L), (bx + L, by + L)], fill=(255, 255, 255), width=16)
        d.line([(bx - L, by - L), (bx + L, by + L)], fill=(230, 30, 30), width=9)
        rotulo(d, 640, 1150, "0 COMBUSTÍVEL", int(52 * k) + 1, AMARELO)
    # rastro de energia do sol para a asa
    for i in range(3):
        f = (T * 0.8 + i / 3) % 1
        x, y = 860 + (700 - 860) * f, 700 + (850 - 700) * f
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=AMARELO, outline=O, width=2)


def c_jumbo(d, img, t, T):
    selo(d)
    # comparação de envergadura: jumbo (contorno) x avião solar; carro na balança
    aviao(d, 540, 640, 1.0, T)
    k = ease(t / 0.8)
    w747 = 470 * 68 / 72
    y = 880
    d.line([(540 - w747, y), (540 + w747, y)], fill=(255, 255, 255), width=6)
    d.line([(540 - 470, y + 40), (540 + 470, y + 40)], fill=AMARELO, width=6)
    rotulo(d, 540, y - 30, "JUMBO: 68 M", 36, (255, 255, 255))
    rotulo(d, 540, y + 75, "SOLAR: 72 M", 40, AMARELO)
    # balança com carro x avião
    kk = pop(min(1, max(0, t - 1.0) / 0.5))
    if kk > 0.05:
        cx, cy = 540, 1110
        d.polygon([(cx - 20, cy + 80), (cx + 20, cy + 80), (cx, cy + 20)], fill=(200, 200, 210), outline=O)
        d.line([(cx - 300, cy + 20), (cx + 300, cy + 20)], fill=O, width=12)
        # carro à esquerda
        d.rounded_rectangle([cx - 380, cy - 60, cx - 200, cy + 5], radius=18, fill=(230, 70, 70), outline=O, width=5)
        d.rounded_rectangle([cx - 345, cy - 105, cx - 240, cy - 55], radius=14, fill=(230, 70, 70), outline=O, width=5)
        for wx in (cx - 345, cx - 235):
            d.ellipse([wx - 22, cy - 10, wx + 22, cy + 30], fill=O)
        aviao(d, cx + 290, cy - 50, 0.3, T)
        rotulo(d, cx, cy + 115, "~2,3 TONELADAS", int(48 * kk) + 1, CIANO)
        rotulo(d, cx, cy - 10, "=", 70, AMARELO, traduzir=False)


def c_celulas(d, img, t, T):
    selo(d)
    # metade dia (sol carrega) e metade noite (bateria descarrega)
    d.rectangle([0, 520, 540, 1260], fill=(70, 150, 220))
    d.rectangle([540, 520, 1080, 1260], fill=(15, 20, 60))
    sol(d, 180, 640, 60, T, rosto=False)
    d.ellipse([870, 590, 970, 690], fill=(240, 240, 210), outline=O, width=4)
    d.ellipse([900, 580, 990, 670], fill=(15, 20, 60))
    for i in range(6):
        x, y = 640 + (i * 73) % 380, 760 + (i * 37) % 60
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 255))
    # painel grande de células à esquerda, bateria à direita
    for r in range(4):
        for c in range(5):
            x, y = 60 + c * 82, 820 + r * 70
            d.rectangle([x, y, x + 74, y + 62], fill=CEL, outline=CEL2, width=3)
    lvl = 0.25 + 0.75 * ease(t / 2.5)
    bx, by = 760, 840
    d.rounded_rectangle([bx - 110, by, bx + 110, by + 300], radius=20, fill=(30, 30, 40), outline=(255, 255, 255), width=8)
    d.rectangle([bx - 40, by - 30, bx + 40, by], fill=(255, 255, 255))
    d.rectangle([bx - 90, by + 280 - 260 * lvl, bx + 90, by + 280], fill=(90, 230, 110))
    seta(d, 480, 990, 620, 990, AMARELO, 14)
    contador(d, 270, 1160, 17000, t, 1.6, 80, "", AMARELO)
    rotulo(d, 270, 1245, "CÉLULAS SOLARES", 38, (255, 255, 255))
    rotulo(d, 760, 1200, "VOA DE NOITE", 44, CIANO)


def c_havai(d, img, t, T):
    selo(d)
    # mapa simplificado: Japão à esquerda, Havaí à direita, rota tracejada + relógio
    d.polygon([(120, 650), (170, 610), (200, 700), (160, 800), (110, 760)], fill=(110, 190, 110), outline=O)
    for k, (x, y, r) in enumerate([(880, 760, 16), (920, 785, 12), (960, 810, 22), (1000, 835, 30)]):
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(110, 190, 110), outline=O, width=3)
    rotulo(d, 160, 880, "JAPÃO", 42, (255, 255, 255))
    rotulo(d, 940, 900, "HAVAÍ", 42, (255, 255, 255))
    k = ease(t / 2.0)
    for i in range(20):
        f = i / 20
        if f > k: break
        x = 200 + 680 * f; y = 720 - math.sin(f * 3.14) * 90
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=AMARELO)
    x = 200 + 680 * k; y = 720 - math.sin(k * 3.14) * 90
    aviao(d, x, y - 30, 0.14, T)
    # relógio
    cx, cy = 360, 1080
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(255, 255, 255), outline=O, width=8)
    a = T * 6
    d.line([(cx, cy), (cx + math.cos(a) * 90, cy + math.sin(a) * 90)], fill=O, width=8)
    d.line([(cx, cy), (cx + math.cos(a / 12) * 60, cy + math.sin(a / 12) * 60)], fill=(230, 50, 50), width=10)
    rotulo(d, cx, cy + 165, "QUASE 5 DIAS", 42, AMARELO)
    # piloto cochilando
    px, py = 800, 1080
    d.ellipse([px - 70, py - 70, px + 70, py + 70], fill=(240, 190, 150), outline=O, width=6)
    d.arc([px - 40, py - 15, px - 10, py + 10], 0, 180, fill=O, width=5)
    d.arc([px + 10, py - 15, px + 40, py + 10], 0, 180, fill=O, width=5)
    for i in range(3):
        f = (T * 0.7 + i / 3) % 1
        rotulo(d, px + 80 + f * 60, py - 50 - f * 60, "z", int(30 + f * 30), (255, 255, 255), traduzir=False)
    rotulo(d, px, py + 165, "COCHILOS DE 20 MIN", 36, CIANO)


def c_cta(d, img, t, T):
    g_sol(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="SÓ COM SOL!", titulo_y=400, desenho=g_sol, fundo=(CEU1, CEU2),
         fala="Esse avião deu a volta ao mundo sem uma gota de combustível! E o fim é o mais louco."),
    dict(tipo="fato", titulo="SOLAR IMPULSE", desenho=c_jumbo, fundo=((30, 90, 170), (8, 30, 80)),
         fala="Asa maior que a de um jumbo e peso de carro! Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="17 MIL PLACAS", desenho=c_celulas, fundo=((20, 60, 120), (5, 15, 50)),
         fala="dezessete mil células solares enchiam as baterias pra voar de noite."),
    dict(tipo="fato", titulo="5 DIAS NO AR", desenho=c_havai, fundo=((15, 80, 140), (5, 25, 60)),
         fala="Do Japão ao Havaí: quase cinco dias sem pousar, só com cochilos de vinte minutos. Eu não aguentava!"),
    dict(tipo="cta", titulo="SÓ COM SOL!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(CEU1, CEU2),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana. Tudo com esse avião..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "solar_impulse.mp4"))
