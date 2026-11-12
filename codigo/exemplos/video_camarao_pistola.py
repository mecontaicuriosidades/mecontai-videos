"""Camarão-pistola: o tiro de bolha que chega a ~4.700 °C. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, brilhos, seta, termometro, sol, O

CASCA = (240, 110, 90); CASCA2 = (200, 70, 60); GARRA = (250, 150, 70)
AGUA = (120, 220, 255); LARANJA = (255, 140, 30); VERMELHO = (230, 60, 60)


def camarao(d, cx, cy, s, T, aberta=1.0):
    """Camarão-pistola virado para a direita; aberta 0..1 controla a garra grande."""
    # cauda em leque
    for k in (-1, 0, 1):
        d.polygon([(cx - 210 * s, cy), (cx - 330 * s, cy - 70 * s + k * 60 * s), (cx - 300 * s, cy + 40 * s + k * 60 * s)],
                  fill=CASCA2, outline=O)
    # segmentos do corpo
    for i in range(5):
        x = cx - 190 * s + i * 60 * s
        r = (55 + i * 6) * s
        d.ellipse([x - r, cy - r * 0.8, x + r, cy + r * 0.8], fill=CASCA if i % 2 else CASCA2, outline=O, width=5)
    # cabeça
    hx = cx + 110 * s
    d.ellipse([hx - 95 * s, cy - 80 * s, hx + 95 * s, cy + 70 * s], fill=CASCA, outline=O, width=6)
    # antenas
    for k, fase in ((-1, 0), (1, 1.5)):
        a = math.sin(T * 3 + fase) * 30 * s
        d.line([(hx + 60 * s, cy - 60 * s), (hx + 260 * s, cy - 220 * s + a), (hx + 380 * s, cy - 180 * s + a * 1.5)],
               fill=O, width=5)
    # perninhas
    for i in range(5):
        x = cx - 150 * s + i * 50 * s
        mov = math.sin(T * 10 + i) * 10 * s
        d.line([(x, cy + 40 * s), (x + 10 * s + mov, cy + 110 * s)], fill=CASCA2, width=int(10 * s) + 2)
    olhos(d, hx + 30 * s, cy - 55 * s, T, esp=55 * s, r=17 * s)
    # garra grande: base + "martelo" que abre/fecha
    gx, gy = hx + 120 * s, cy + 40 * s
    d.ellipse([gx - 50 * s, gy - 60 * s, gx + 190 * s, gy + 60 * s], fill=GARRA, outline=O, width=6)
    ang = -0.9 * aberta
    px = gx + 170 * s
    ex, ey = px + math.cos(ang) * 120 * s, gy - 30 * s + math.sin(ang) * 120 * s
    d.line([(px - 30 * s, gy - 30 * s), (ex, ey)], fill=O, width=int(46 * s) + 6)
    d.line([(px - 30 * s, gy - 30 * s), (ex, ey)], fill=GARRA, width=int(36 * s))
    return gx + 300 * s, gy  # ponta da garra (de onde sai o tiro)


def bolha(d, x, y, r, quente=0.0):
    cor = tuple(int(AGUA[i] * (1 - quente) + (255, 250, 200)[i] * quente) for i in range(3))
    d.ellipse([x - r, y - r, x + r, y + r], fill=cor, outline=O, width=5)
    d.ellipse([x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.25], fill="white")


def flash(d, x, y, r, T):
    for i in range(10):
        a = i / 10 * 2 * math.pi + T
        d.line([(x, y), (x + math.cos(a) * r, y + math.sin(a) * r)], fill=(255, 240, 150), width=12)
    d.ellipse([x - r * 0.45, y - r * 0.45, x + r * 0.45, y + r * 0.45], fill=(255, 255, 220), outline=LARANJA, width=8)


def peixinho(d, x, y, s, tonto=False, T=0):
    d.polygon([(x - 60 * s, y), (x - 110 * s, y - 40 * s), (x - 110 * s, y + 40 * s)], fill=(120, 200, 120), outline=O)
    d.ellipse([x - 70 * s, y - 40 * s, x + 60 * s, y + 40 * s], fill=(150, 230, 140), outline=O, width=5)
    if tonto:
        for sx in (-1,):
            ex, ey = x + 25 * s, y - 10 * s
            d.line([(ex - 12, ey - 12), (ex + 12, ey + 12)], fill=O, width=6)
            d.line([(ex - 12, ey + 12), (ex + 12, ey - 12)], fill=O, width=6)
        for i in range(3):
            a = T * 4 + i * 2.1
            sx_, sy_ = x + math.cos(a) * 60 * s, y - 80 * s + math.sin(a) * 18 * s
            d.ellipse([sx_ - 10, sy_ - 10, sx_ + 10, sy_ + 10], fill=AMARELO, outline=O, width=3)
    else:
        d.ellipse([x + 15 * s, y - 22 * s, x + 40 * s, y + 3 * s], fill="white", outline=O, width=4)
        d.ellipse([x + 24 * s, y - 14 * s, x + 36 * s, y - 2 * s], fill=O)


# ---------------- cenas ----------------
def g_tiro(d, img, t, T):
    ciclo = (t % 1.6) / 1.6
    aberta = 1.0 if ciclo < 0.5 else 0.0
    px, py = camarao(d, 350, 820, 0.95, T, aberta)
    if ciclo >= 0.5:
        k = (ciclo - 0.5) / 0.5
        bx = px + 80 + k * 260
        if k < 0.6:
            bolha(d, bx, py, 30 + k * 60, quente=k)
        else:
            flash(d, bx, py, 150, T)
            peixinho(d, 900, py + 170, 0.9, tonto=True, T=T)
    if ciclo < 0.5 or (ciclo - 0.5) / 0.5 < 0.6:
        peixinho(d, 900, py + 150, 0.9, T=T)
    if t > 0.5:
        rotulo(d, 680, 1180, "4.700 °C", 80, LARANJA)


def c_garra(d, img, t, T):
    fecha = ease((t - 0.8) / 0.15) if t > 0.8 else 0
    px, py = camarao(d, 380, 780, 1.15, T, aberta=1 - fecha)
    if fecha >= 1:
        k = min(1, (t - 0.95) / 1.0)
        for i in range(6):  # jato de água
            x = px + 30 + i * 60 * k
            d.ellipse([x - 22, py - 14 + math.sin(T * 9 + i) * 6, x + 22, py + 14], fill=AGUA, outline=O, width=3)
        bolha(d, px + 40 + 380 * k, py, 40 + 30 * k)
    if t > 1.6:
        rotulo(d, 540, 1170, "JATO + BOLHA", 60, AGUA)


def c_sol(d, img, t, T):
    sol(d, 270, 690, 140, T)
    rotulo(d, 270, 930, "SOL ~5.500 °C", 46, AMARELO)
    if t > 0.6:
        s = pop((t - 0.6) / 0.5)
        flash(d, 810, 690, 200 * s, T)
        rotulo(d, 810, 930, "BOLHA ~4.700 °C", 46, LARANJA)
    termometro(d, 540, 1100, min(1, t / 2.0), cor=LARANJA, h=300)
    if t > 2.0:
        rotulo(d, 540, 1240, "E SOLTA LUZ!", 60, (255, 250, 200))


def c_barulho(d, img, t, T):
    px, py = camarao(d, 270, 720, 0.7, T, aberta=0.0)
    # ondas de choque
    for i in range(4):
        r = ((T * 200 + i * 80) % 320) + 40
        d.arc([px - r, py - r, px + r, py + r], -60, 60, fill=(255, 255, 255), width=10)
    # barras de volume
    for i in range(7):
        h = 40 + i * 45 * min(1, t / 1.2)
        x = 170 + i * 80
        d.rounded_rectangle([x, 1130 - h, x + 56, 1130], 10, fill=(80, 230, 120) if i < 4 else (VERMELHO if i > 5 else AMARELO),
                            outline=O, width=4)
    peixinho(d, 860, 900, 1.1, tonto=t > 0.8, T=T)
    if t > 1.5:
        rotulo(d, 860, 1050, "ATORDOADO", 46, AMARELO)


def submarino(d, cx, cy, s, cor=(240, 200, 40)):
    d.ellipse([cx - 280 * s, cy - 90 * s, cx + 280 * s, cy + 90 * s], fill=cor, outline=O, width=7)
    d.rounded_rectangle([cx - 60 * s, cy - 170 * s, cx + 80 * s, cy - 70 * s], 20, fill=cor, outline=O, width=7)
    d.line([(cx + 30 * s, cy - 170 * s), (cx + 30 * s, cy - 240 * s), (cx + 80 * s, cy - 240 * s)], fill=O, width=10)
    for i in range(3):
        x = cx - 150 * s + i * 110 * s
        d.ellipse([x - 30 * s, cy - 30 * s, x + 30 * s, cy + 30 * s], fill=AGUA, outline=O, width=5)
    d.polygon([(cx - 280 * s, cy), (cx - 360 * s, cy - 70 * s), (cx - 360 * s, cy + 70 * s)], fill=cor, outline=O)


def c_sonar(d, img, t, T):
    sy = 640 + math.sin(T * 1.5) * 12
    submarino(d, 560, sy, 1.0)
    # tela de sonar bagunçada
    d.rounded_rectangle([260, 820, 820, 1110], 24, fill=(10, 40, 30), outline=O, width=8)
    for i in range(40):
        x = 280 + i * 13
        h = abs(math.sin(i * 1.7 + T * 12)) * 110 * min(1, t / 0.8)
        d.line([(x, 965 - h), (x, 965 + h)], fill=(80, 255, 140), width=6)
    if t > 0.8:
        rotulo(d, 540, 790, "???", 70, VERMELHO)
    # camarõezinhos no fundo
    for i in range(5):
        camarao(d, 150 + i * 200, 1220, 0.22, T + i, aberta=(1 if (T * 3 + i) % 1 < 0.5 else 0))


CENAS = [
    dict(tipo="gancho", titulo="TIRO DE 4.700°C", desenho=g_tiro, fundo=((20, 90, 130), (5, 30, 60)),
         fala="Esse camarão dispara bolhas de quatro mil e setecentos graus. E ele nem encosta na presa!"),
    dict(tipo="fato", titulo="A GARRA-PISTOLA", desenho=c_garra, fundo=((30, 140, 160), (10, 60, 90)),
         fala="É o camarão-pistola. Ele fecha a garra tão rápido que dispara um jato de água e cria uma bolha."),
    dict(tipo="fato", titulo="QUASE UM SOL", desenho=c_sol, fundo=((120, 50, 20), (40, 15, 10)),
         fala="Quando a bolha estoura, ela fica quase tão quente quanto a superfície do Sol, e ainda solta um flash de luz."),
    dict(tipo="fato", titulo="BARULHO ABSURDO", desenho=c_barulho, fundo=((40, 40, 110), (10, 10, 45)),
         fala="O estalo é um dos sons mais fortes do oceano, e a onda de choque deixa peixinhos atordoados na hora."),
    dict(tipo="fato", titulo="CEGA SUBMARINO", desenho=c_sonar, fundo=((15, 70, 80), (5, 25, 35)),
         fala="Na Segunda Guerra, colônias desses camarões faziam tanto barulho que atrapalhavam o sonar dos submarinos!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Qual bicho é mais insano?",
         fala="Comenta: você conhecia esse atirador? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "camarao_pistola.mp4"))
