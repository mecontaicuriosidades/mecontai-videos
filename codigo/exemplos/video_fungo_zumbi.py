"""Fungo zumbi (Ophiocordyceps): transforma formigas em zumbis sem tocar no cérebro. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, sol, O

FORMIGA = (90, 45, 30); FORMIGA2 = (130, 70, 45); FUNGO = (235, 200, 120); FUNGO2 = (190, 140, 70)
FOLHA = (70, 170, 80); FOLHA2 = (40, 120, 55); ESPORO = (250, 240, 170); ROXO = (170, 110, 220)


def formiga(d, cx, cy, s, T, zumbi=False, ang=0.0, pernas=True):
    """Formiga de perfil virada para a direita. Retorna posição da cabeça."""
    ca, sa = math.cos(ang), math.sin(ang)

    def P(x, y):
        return (cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s)

    def bola(x, y, rx, ry, cor):
        px, py = P(x, y)
        d.ellipse([px - rx * s, py - ry * s, px + rx * s, py + ry * s], fill=cor, outline=O, width=max(3, int(6 * s)))
    if pernas:
        for i, x in enumerate((-20, 10, 40)):
            mov = math.sin(T * (4 if zumbi else 12) + i * 2) * 14
            a, b, c = P(x, 10), P(x - 30 + mov, 60), P(x - 45 + mov, 95)
            d.line([a, b, c], fill=O, width=max(3, int(7 * s)))
    bola(-95, 0, 70, 50, FORMIGA)        # abdômen
    bola(5, 0, 45, 28, FORMIGA2)          # tórax
    bola(90, -10, 45, 40, FORMIGA)        # cabeça
    hx, hy = P(90, -10)
    # antenas
    for k in (0, 1):
        a = math.sin(T * 5 + k) * 12
        d.line([P(110, -40), P(150, -100 + k * 20 + a), P(190, -90 + k * 20 + a)], fill=O, width=max(3, int(6 * s)))
    # olho
    ex, ey = P(110, -20)
    r = 12 * s
    if zumbi:
        for k in (-1, 1):
            d.line([(ex - r, ey - r * k), (ex + r, ey + r * k)], fill=ROXO, width=max(3, int(6 * s)))
    else:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill="white", outline=O, width=3)
        d.ellipse([ex - r * 0.4, ey - r * 0.4, ex + r * 0.5, ey + r * 0.5], fill=O)
    return hx, hy


def haste(d, x, y, alt, T, s=1.0):
    """Haste do fungo brotando de (x, y) para cima, com 'cabeça' de esporos."""
    if alt <= 2:
        return x, y
    bal = math.sin(T * 2) * 10 * s
    pts = [(x, y), (x + 10 * s + bal * 0.3, y - alt * 0.5), (x + bal, y - alt)]
    d.line(pts, fill=O, width=int(22 * s) + 6)
    d.line(pts, fill=FUNGO, width=int(22 * s))
    tx, ty = pts[-1]
    if alt > 60 * s:
        d.ellipse([tx - 28 * s, ty - 34 * s, tx + 28 * s, ty + 20 * s], fill=FUNGO2, outline=O, width=5)
        for i in range(5):
            a = i * 1.3
            d.ellipse([tx + math.cos(a) * 14 * s - 5, ty - 8 * s + math.sin(a) * 12 * s - 5,
                       tx + math.cos(a) * 14 * s + 5, ty - 8 * s + math.sin(a) * 12 * s + 5], fill=ESPORO)
    return tx, ty


def folha(d, x0, y0, x1, y1, larg, cor=FOLHA):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    n = math.hypot(nx, ny) or 1
    nx, ny = nx / n * larg, ny / n * larg
    d.polygon([(x0, y0), (mx + nx, my + ny), (x1, y1), (mx - nx, my - ny)], fill=cor, outline=O)
    d.line([(x0, y0), (x1, y1)], fill=FOLHA2, width=8)


def esporos(d, cx, cy, T, n=14, raio=300, queda=True):
    for i in range(n):
        x = cx + ((i * 97) % raio) - raio / 2 + math.sin(T * 2 + i) * 15
        y = cy + ((T * 120 + i * 53) % 420 if queda else (i * 31) % 200)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=ESPORO, outline=O, width=2)


# ---------------- cenas ----------------
def g_zumbi(d, img, t, T):
    # galho e folha, formiga presa mordendo a folha com haste saindo da cabeça
    d.line([(80, 1300), (480, 1020), (980, 880)], fill=(110, 70, 40), width=34)
    folha(d, 480, 1020, 860, 760, 110)
    hx, hy = formiga(d, 520, 960, 1.15, T, zumbi=True, ang=-0.55, pernas=True)
    alt = 170 + min(1, t / 1.2) * 70
    haste(d, hx - 10, hy - 30, alt, T, 1.1)
    esporos(d, 640, 700, T, n=10, raio=380)
    if t > 0.3:
        rotulo(d, 820, 1180, "ZUMBI!", 74, ROXO)


def c_invasao(d, img, t, T):
    formiga(d, 520, 860, 2.0, T, zumbi=False, pernas=True)
    # esporo caindo e grudando
    k = min(1, t / 0.9)
    sx, sy = 420, 520 + k * 260
    d.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=ESPORO, outline=O, width=4)
    if t > 1.0:
        # fios do fungo se espalhando pelo corpo
        m = min(1, (t - 1.0) / 2.0)
        for i in range(int(18 * m)):
            a = i * 0.9
            r = 30 + (i * 23) % 130
            x0, y0 = 360 + math.cos(a) * r * 0.9, 860 + math.sin(a) * r * 0.55
            d.line([(x0, y0), (x0 + 30 * math.cos(a + 1), y0 + 20 * math.sin(a + 1))], fill=FUNGO, width=7)
        rotulo(d, 540, 1150, "FUNGO NOS MÚSCULOS", 54, FUNGO)
    rotulo(d, 330, 470, "ESPORO", 44, ESPORO)


def c_sobe(d, img, t, T):
    # chão da floresta, caule, régua de 25 cm
    d.rectangle([0, 1180, 1080, 1300], fill=(80, 55, 35), outline=O, width=6)
    d.line([(600, 1185), (600, 560)], fill=FOLHA2, width=26)
    folha(d, 600, 600, 860, 520, 60)
    folha(d, 600, 760, 380, 690, 50)
    k = ease(t / 2.5)
    y = 1150 - k * 520
    formiga(d, 600, y, 0.75, T, zumbi=True, ang=-math.pi / 2)
    # régua
    d.rectangle([180, 600, 250, 1180], fill=(250, 230, 160), outline=O, width=5)
    for i in range(11):
        yy = 1180 - i * 58
        d.line([(180, yy), (215 if i % 5 else 240, yy)], fill=O, width=4)
    rotulo(d, 215, 560, "25 cm", 50, AMARELO, traduzir=False)
    # formigas da colônia indo embora no chão
    for i in range(3):
        formiga(d, 820 + i * 110 - (T * 30) % 60, 1150, 0.3, T + i)


def c_mordida(d, img, t, T):
    sol(d, 880, 560, 80, T)
    rotulo(d, 880, 700, "12:00", 50, AMARELO, traduzir=False)
    folha(d, 150, 700, 750, 900, 150)
    # formiga de cabeça para baixo mordendo a nervura
    aperta = 0.5 + 0.5 * math.sin(T * 10)
    hx, hy = formiga(d, 420, 980, 1.3, T, zumbi=True, ang=-0.4, pernas=False)
    for k in (-1, 1):
        d.line([(hx + 30, hy - 10 * k), (hx + 55 + aperta * 8, hy - 40 - 10 * k)], fill=O, width=12)
    if t > 0.9:
        rotulo(d, 540, 1200, "TRAVADA ATÉ MORRER", 56, (255, 120, 120))


def c_chuva(d, img, t, T):
    folha(d, 120, 780, 760, 860, 100)
    hx, hy = formiga(d, 420, 770, 0.9, T, zumbi=True, ang=0.05, pernas=False)
    tx, ty = haste(d, hx - 20, hy - 30, min(1, t / 1.0) * 180, T, 1.0)
    if t > 0.8:
        esporos(d, 450, 880, T, n=14, raio=520)
    # formigas passando embaixo
    d.rectangle([0, 1190, 1080, 1300], fill=(80, 55, 35), outline=O, width=6)
    for i in range(4):
        formiga(d, ((T * 90 + i * 280) % 1300) - 120, 1150, 0.45, T + i)
    if t > 1.5:
        rotulo(d, 820, 1000, "PRÓXIMA VÍTIMA", 46, ESPORO)


CENAS = [
    dict(tipo="gancho", titulo="FORMIGA ZUMBI", desenho=g_zumbi, fundo=((40, 90, 50), (10, 35, 20)),
         fala="Esse fungo transforma formigas em zumbis. E faz isso sem nem tocar no cérebro delas!"),
    dict(tipo="fato", titulo="A INVASÃO", desenho=c_invasao, fundo=((90, 60, 120), (30, 15, 50)),
         fala="O esporo gruda na formiga, entra pela casca e se espalha pelo corpo, enrolando os músculos."),
    dict(tipo="fato", titulo="SOBE 25 CM", desenho=c_sobe, fundo=((60, 120, 90), (15, 45, 30)),
         fala="Aí ela abandona a colônia e sobe numa planta, até uns vinte e cinco centímetros do chão, a altura perfeita pro fungo."),
    dict(tipo="fato", titulo="MORDIDA FINAL", desenho=c_mordida, fundo=((110, 150, 60), (35, 60, 20)),
         fala="Perto do meio-dia, ela morde a nervura de uma folha com toda a força e morre ali, travada."),
    dict(tipo="fato", titulo="CHUVA DE ESPOROS", desenho=c_chuva, fundo=((70, 50, 30), (25, 15, 10)),
         fala="Dias depois, uma haste brota da cabeça dela e solta esporos nas formigas que passam embaixo."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Assustador ou genial?",
         fala="Comenta: isso é assustador ou genial? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "fungo_zumbi.mp4"))
