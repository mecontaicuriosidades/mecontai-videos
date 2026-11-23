"""ENIAC, o computador de 30 toneladas (TECNOLOGIA INSANA #2). Formato v3 + estratégia 23/11."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "TECNOLOGIA INSANA #2"
PAINEL = (60, 64, 72); PAINEL2 = (38, 40, 48); LUZV = (255, 90, 70); LUZA = (255, 210, 80); VALV = (255, 160, 60)
PISO = (120, 95, 70); CABO = [(240, 80, 80), (80, 200, 255), (255, 220, 60), (120, 230, 120)]


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def armario(d, x, y, w, h, T, sem=0):
    d.rectangle([x, y, x + w, y + h], fill=PAINEL, outline=O, width=5)
    cols, rows = max(2, int(w // 34)), max(3, int(h // 40))
    for i in range(cols):
        for j in range(rows):
            on = math.sin(T * 6 + i * 1.7 + j * 2.3 + sem) > 0.2
            cx, cy = x + (i + 0.5) * w / cols, y + 20 + j * (h - 40) / max(1, rows - 1)
            r = max(3, w / cols * 0.18)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(LUZV if (i + j) % 3 else LUZA) if on else PAINEL2)


def sala(d, T, y0=560, y1=1220):
    """Parede de armários em perspectiva (vista de canto)."""
    d.polygon([(0, y1), (1080, y1), (1080, 1300), (0, 1300)], fill=PISO)
    x = 40
    for k in range(6):
        w = 150 - k * 12; h = (y1 - y0) - k * 30
        armario(d, x, y0 + k * 15, w, h, T, k)
        x += w + 8


def celular(d, cx, cy, s=1.0, T=0):
    d.rounded_rectangle([cx - 55 * s, cy - 100 * s, cx + 55 * s, cy + 100 * s], int(18 * s), fill=(30, 30, 40), outline=O, width=6)
    d.rounded_rectangle([cx - 44 * s, cy - 84 * s, cx + 44 * s, cy + 84 * s], int(10 * s), fill=(60, 160, 230))
    for j in range(3):
        for i in range(3):
            x, y = cx - 28 * s + i * 28 * s, cy - 55 * s + j * 32 * s
            d.rounded_rectangle([x - 10 * s, y - 10 * s, x + 10 * s, y + 10 * s], int(4 * s), fill=(255, 255, 255))


def g_sala(d, img, t, T):
    etiqueta(d)
    sala(d, T, 610)
    k = pop(min(1, max(0, t - 0.2) / 0.5))
    if k > 0.05:
        rotulo(d, 400, 565, "30 TONELADAS", int(52 * k) + 1, AMARELO)
    celular(d, 930, 1080, 0.9, T)
    if t > 1.2:
        rotulo(d, 930, 900, "MILHÕES DE VEZES", 30, CIANO)
        rotulo(d, 930, 940, "MAIS RÁPIDO", 30, CIANO)


def valvula(d, x, y, s, T, i):
    acesa = math.sin(T * 3 + i) > -0.6
    d.rounded_rectangle([x - 22 * s, y - 70 * s, x + 22 * s, y + 20 * s], int(20 * s), fill=(255, 230, 190) if acesa else (150, 150, 160), outline=O, width=4)
    if acesa:
        d.line([(x - 8 * s, y - 30 * s), (x, y - 50 * s), (x + 8 * s, y - 30 * s)], fill=VALV, width=int(6 * s))
    d.rectangle([x - 26 * s, y + 20 * s, x + 26 * s, y + 45 * s], fill=(60, 60, 70), outline=O, width=4)


def c_eniac(d, img, t, T):
    armario(d, 60, 520, 420, 640, T)
    rotulo(d, 270, 1210, "ENIAC", 70, AMARELO, traduzir=False)
    for j in range(3):
        for i in range(4):
            n = j * 4 + i
            if t > 0.12 * n:
                valvula(d, 620 + i * 110, 640 + j * 190, 1.0, T, n)
    rotulo(d, 780, 1150, "~18 MIL VÁLVULAS", 44, VALV)
    rotulo(d, 780, 520, "1946 · EUA", 48, (255, 255, 255))


def c_somas(d, img, t, T):
    contador(d, 540, 700, 5000, t, 1.6, 150)
    rotulo(d, 540, 820, "SOMAS POR SEGUNDO", 46, (255, 255, 255))
    for i in range(5):
        valvula(d, 220 + i * 160, 1080, 1.1, T * 0 + (9 if i == 2 and t > 2.0 else 0), i)
    if t > 2.0:
        k = pop(min(1, (t - 2.0) / 0.4))
        rotulo(d, 540, 940, "PUF!", int(70 * k) + 1, (255, 90, 70))
        d.rounded_rectangle([500, 1010, 580, 1140], 30, fill=(150, 150, 160), outline=O, width=4)
        rotulo(d, 540, 1230, "QUEIMAVAM TODO DIA", 40, AMARELO)


def pessoa(d, x, y, cor, T, i):
    bob = 6 * math.sin(T * 3 + i)
    d.ellipse([x - 26, y - 120 + bob, x + 26, y - 68 + bob], fill=(240, 200, 170), outline=O, width=4)
    d.chord([x - 32, y - 132 + bob, x + 32, y - 80 + bob], 180, 360, fill=(70, 45, 30))
    d.polygon([(x - 22, y - 68 + bob), (x + 22, y - 68 + bob), (x + 48, y + 40), (x - 48, y + 40)], fill=cor, outline=O)
    d.line([(x + 20, y - 40 + bob), (x + 50, y - 110)], fill=O, width=9)


def c_cabos(d, img, t, T):
    # painel de tomadas com cabos coloridos
    d.rectangle([90, 500, 990, 880], fill=PAINEL, outline=O, width=6)
    for j in range(4):
        for i in range(12):
            x, y = 140 + i * 72, 550 + j * 90
            d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(20, 20, 25))
    for k in range(6):
        if t > 0.3 * k:
            a = (140 + (k * 2) * 72, 550 + (k % 4) * 90)
            b = (140 + (11 - k) * 72, 550 + ((k + 2) % 4) * 90)
            mid = ((a[0] + b[0]) / 2, max(a[1], b[1]) + 120)
            d.line([a, mid, b], fill=CABO[k % 4], width=10, joint="curve")
    cores = [(200, 70, 90), (90, 120, 200), (70, 160, 120), (200, 150, 60), (150, 90, 180), (60, 170, 190)]
    for i in range(6):
        pessoa(d, 150 + i * 156, 1120, cores[i], T, i)
    rotulo(d, 540, 1230, "6 PROGRAMADORAS", 46, AMARELO)


def c_cta(d, img, t, T):
    etiqueta(d)
    sala(d, T, 610)
    celular(d, 930, 1080, 0.9, T)


CENAS = [
    dict(tipo="gancho", titulo="UMA SALA!", titulo_y=400, desenho=g_sala, fundo=((40, 45, 70), (15, 15, 30)),
         fala="Esse computador pesava trinta toneladas... e seu celular é milhões de vezes mais rápido!"),
    dict(tipo="fato", titulo="O ENIAC", desenho=c_eniac, fundo=((50, 40, 60), (18, 14, 26)),
         fala="É o ENIAC: uma sala inteira, com quase dezoito mil válvulas."),
    dict(tipo="fato", titulo="5 MIL SOMAS", desenho=c_somas, fundo=((30, 50, 70), (10, 18, 30)),
         fala="Cinco mil somas por segundo, e as válvulas queimavam toda hora. Que paciência!"),
    dict(tipo="fato", titulo="SEM TECLADO", desenho=c_cabos, fundo=((60, 40, 50), (20, 12, 18)),
         fala="Sem teclado: seis mulheres programavam trocando cabos. E foram esquecidas por décadas."),
    dict(tipo="cta", titulo="UMA SALA!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 45, 70), (15, 15, 30)),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana! Esse computador..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "eniac.mp4"))
