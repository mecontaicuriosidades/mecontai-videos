"""Fábrica de sangue: 2 milhões de hemácias por segundo (CIÊNCIA BIZARRA #7). Formato v3 + ESTRATÉGIA DA SEMANA 23/11
(20–28 s, abertura com número no 1º segundo, 1 frase de opinião da MAIA).
Fatos (Britannica "erythropoiesis"; Sender, Fuchs & Milo, PLoS Biology 2016): a medula óssea (tutano) produz cerca
de 2 a 3 milhões de hemácias por segundo; a hemácia madura dos mamíferos expulsa o núcleo (não tem DNA), o que deixa
mais espaço para a hemoglobina, e vive ~120 dias; das ~30 trilhões de células humanas, ~25 trilhões (≈84%) são
hemácias — umas 8 em cada 10 (em número, não em peso)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "CIÊNCIA BIZARRA #7"
HEM = (225, 45, 60); HEM2 = (170, 20, 40)
OSSO = (245, 235, 210); TUTANO = (200, 70, 80)
F1 = (90, 10, 30); F2 = (25, 3, 12)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def hemacia(d, x, y, r=34, ang=0.0):
    """Disco bicôncavo visto um pouco de lado (rosquinha sem furo)."""
    ry = r * (0.55 + 0.45 * abs(math.cos(ang)))
    d.ellipse([x - r, y - ry, x + r, y + ry], fill=HEM, outline=O, width=max(2, int(r / 9)))
    d.ellipse([x - r * 0.45, y - ry * 0.45, x + r * 0.45, y + ry * 0.45], fill=HEM2)


def osso(d, cx, cy, s=1.0, corte=True):
    """Osso deitado com as duas pontas e um corte no meio mostrando o tutano."""
    L = 330 * s; h = 70 * s
    d.rectangle([cx - L, cy - h, cx + L, cy + h], fill=OSSO, outline=O, width=max(3, int(7 * s)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = cx + sx * L, cy + sy * h * 0.9
            d.ellipse([x - 75 * s, y - 75 * s, x + 75 * s, y + 75 * s], fill=OSSO, outline=O, width=max(3, int(7 * s)))
    d.rectangle([cx - L + 10 * s, cy - h + 5 * s, cx + L - 10 * s, cy + h - 5 * s], fill=OSSO)
    if corte:
        d.rounded_rectangle([cx - L * 0.6, cy - h * 0.6, cx + L * 0.6, cy + h * 0.6], radius=int(30 * s), fill=TUTANO, outline=O, width=4)
        for i in range(12):
            x = cx - L * 0.5 + (i * 53 * s) % (L * 1.0)
            y = cy - h * 0.3 + (i * 29 * s) % (h * 0.6)
            d.ellipse([x - 9 * s, y - 9 * s, x + 9 * s, y + 9 * s], fill=(240, 120, 120))


def fluxo(d, x0, y0, T, n=14, dx=1.0, spread=1.0, r=30):
    for i in range(n):
        f = (T * 0.6 + i / n) % 1
        x = x0 + dx * f * 520 + math.sin(i * 7.3) * 50 * spread
        y = y0 - f * 120 * spread + math.cos(i * 3.1) * 140 * spread * f
        hemacia(d, x, y, r * (0.6 + 0.4 * f), T * 2 + i)


def g_fabrica(d, img, t, T, label=True):
    etiqueta(d)
    osso(d, 360, 980, 0.8)
    fluxo(d, 480, 980, T, 16, 1.0, 0.7, 34)
    if label:
        contador(d, 640, 640, 2000000, t + 0.6, 1.2, 84, "", AMARELO)
        kk = pop(min(1, max(0, t - 0.3) / 0.5))
        if kk > 0.05:
            rotulo(d, 640, 720, "POR SEGUNDO", int(52 * kk) + 1, (255, 255, 255))
            rotulo(d, 360, 1180, "SEU OSSO", int(46 * kk) + 1, OSSO)


def c_tutano(d, img, t, T):
    selo(d)
    k = ease(t / 0.8)
    osso(d, 540, 820, 1.1 + 0.15 * k)
    seta(d, 300, 1150, 400, 900, AMARELO, 12)
    kk = pop(min(1, max(0, t - 0.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 300, 1210, "TUTANO", int(54 * kk) + 1, AMARELO)
        rotulo(d, 760, 1210, "MEDULA ÓSSEA", int(40 * kk) + 1, (255, 255, 255))
    for i in range(6):
        f = (T * 0.5 + i / 6) % 1
        hemacia(d, 540 + (i - 2.5) * 70, 820 - f * 260, 22, T + i)


def c_nucleo(d, img, t, T):
    selo(d)
    # célula jovem expulsando o núcleo → vira hemácia
    k = ease(t / 1.4)
    cx, cy = 360, 820
    if k < 0.6:
        d.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill=(235, 110, 120), outline=O, width=7)
    else:
        hemacia(d, cx, cy, 140, 0.0)
    nx = cx + 300 * k; ny = cy - 40 * k
    d.ellipse([nx - 60, ny - 60, nx + 60, ny + 60], fill=(120, 80, 200), outline=O, width=6)
    rotulo(d, nx, ny, "DNA", 34, (255, 255, 255))
    if k > 0.7:
        rotulo(d, nx, ny + 110, "TCHAU!", 42, AMARELO)
    kk = pop(min(1, max(0, t - 1.4) / 0.5))
    if kk > 0.05:
        # calendário 120 dias
        x, y = 820, 1080
        d.rounded_rectangle([x - 110, y - 90, x + 110, y + 90], radius=16, fill=(255, 255, 255), outline=O, width=6)
        d.rectangle([x - 110, y - 90, x + 110, y - 45], fill=(230, 60, 60), outline=O, width=6)
        rotulo(d, x, y + 22, "120", int(70 * kk) + 1, O if False else HEM, traduzir=False)
        rotulo(d, x, y + 140, "DIAS DE VIDA", int(40 * kk) + 1, CIANO)
        rotulo(d, 360, 1120, "MAIS OXIGÊNIO", int(44 * kk) + 1, (255, 255, 255))


def c_oito(d, img, t, T):
    selo(d)
    # 10 células: 8 hemácias e 2 outras
    for i in range(10):
        col, row = i % 5, i // 5
        x, y = 160 + col * 190, 700 + row * 230
        k = pop(min(1, max(0, t * 2.5 - i * 0.2)))
        if k < 0.05:
            continue
        if i < 8:
            hemacia(d, x, y, int(70 * k) + 1, T + i)
        else:
            r = 65 * k
            d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 170, 240) if i == 8 else (160, 220, 120), outline=O, width=5)
            d.ellipse([x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4], fill=(80, 60, 160))
    kk = pop(min(1, max(0, t - 1.6) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1150, "8 EM CADA 10", int(70 * kk) + 1, AMARELO)
        rotulo(d, 540, 1230, "SÃO HEMÁCIAS", int(46 * kk) + 1, (255, 255, 255))


def c_cta(d, img, t, T):
    etiqueta(d)
    osso(d, 360, 980, 0.8)
    fluxo(d, 480, 980, T, 16, 1.0, 0.7, 34)


CENAS = [
    dict(tipo="gancho", titulo="2 MILHÕES!", titulo_y=400, desenho=g_fabrica, fundo=(F1, F2),
         fala="Dois milhões de células de sangue novas, por segundo, no seu corpo! E o fim é o mais louco."),
    dict(tipo="fato", titulo="NO TUTANO", desenho=c_tutano, fundo=((110, 30, 50), (30, 5, 15)),
         fala="Elas nascem dentro dos seus ossos, no tutano. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="SEM NÚCLEO", desenho=c_nucleo, fundo=((60, 20, 80), (15, 5, 25)),
         fala="pra levar mais oxigênio, ela joga fora o núcleo e vive sem DNA."),
    dict(tipo="fato", titulo="8 EM CADA 10", desenho=c_oito, fundo=((100, 15, 35), (25, 3, 10)),
         fala="De cada dez células suas, umas oito são essas. Em número, você é quase só sangue!"),
    dict(tipo="cta", titulo="2 MILHÕES!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(F1, F2),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. Lembra: dois milhões..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "fabrica_sangue.mp4"))
