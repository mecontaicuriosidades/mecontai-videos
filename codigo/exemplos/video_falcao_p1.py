"""Falcão-peregrino, Parte 1 (BICHOS INSANOS #1). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, O

SERIE = "BICHOS INSANOS #1"
CINZA = (80, 95, 125); CINZA2 = (50, 60, 90); PEITO = (245, 235, 210); BICO = (255, 200, 40)
CEU1, CEU2 = (90, 170, 230), (30, 80, 160)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def _rot(pts, cx, cy, ang, s):
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + (x * c - y * sn) * s, cy + (x * sn + y * c) * s) for x, y in pts]


def _oval(a, b, n=24, dx=0, dy=0):
    return [(dx + a * math.cos(i / n * 2 * math.pi), dy + b * math.sin(i / n * 2 * math.pi)) for i in range(n)]


def falcao(d, cx, cy, s, ang, T, asas=0.0, palpebra=0.0):
    """Falcão-peregrino de perfil, bico apontando na direção 'ang' (rad). asas 0 = fechadas (mergulho), 1 = abertas."""
    P = lambda pts: _rot(pts, cx, cy, ang, s)
    # cauda
    d.polygon(P([(-100, -16), (-200, -34), (-205, 26), (-100, 16)]), fill=CINZA2, outline=O)
    # asa de trás (abre um pouco quando asas>0)
    ab = asas * 120
    d.polygon(P([(30, -20), (-170, -70 - ab), (-120, -10)]), fill=CINZA2, outline=O)
    # corpo
    d.polygon(P(_oval(115, 52)), fill=CINZA, outline=O)
    d.polygon(P(_oval(70, 34, dx=30, dy=18)), fill=PEITO)
    for k in range(4):  # listras do peito
        x = -10 + k * 22
        d.line(P([(x, 14), (x + 8, 40)]), fill=CINZA2, width=max(2, int(5 * s)))
    # asa da frente
    d.polygon(P([(50, -12), (-190, -40 - ab * 1.3), (-150, 20), (-20, 30)]), fill=CINZA, outline=O)
    for k in range(3):
        d.line(P([(-60 - k * 35, -10 - ab * 0.4), (-100 - k * 35, 10)]), fill=CINZA2, width=max(2, int(5 * s)))
    # cabeça com "capacete" escuro e bigode
    d.polygon(P(_oval(48, 44, dx=118, dy=-14)), fill=PEITO, outline=O)
    d.polygon(P([(80, -50), (150, -60), (168, -20), (130, -10), (118, 30), (95, 20)]), fill=CINZA2)
    # bico
    d.polygon(P([(158, -20), (200, -8), (182, 10), (160, 4)]), fill=BICO, outline=O)
    # olho
    ex, ey = P([(140, -22)])[0]
    r = 15 * s
    d.ellipse([ex - r * 1.3, ey - r * 1.3, ex + r * 1.3, ey + r * 1.3], fill=BICO, outline=O, width=3)
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=O)
    d.ellipse([ex - r * 0.4, ey - r * 0.6, ex, ey - r * 0.2], fill="white")
    if palpebra > 0:
        d.ellipse([ex - r * 1.3, ey - r * 1.3, ex - r * 1.3 + 2.6 * r * palpebra, ey + r * 1.3], fill=(220, 240, 255, 150))


def linhas_vel(d, cx, cy, ang, T, n=9, comp=260):
    for i in range(n):
        off = (i - n / 2) * 34
        fase = (T * 6 + i * 0.37) % 1
        bx = cx - math.cos(ang) * (180 + fase * 160) - math.sin(ang) * off
        by = cy - math.sin(ang) * (180 + fase * 160) + math.cos(ang) * off
        d.line([(bx, by), (bx - math.cos(ang) * comp, by - math.sin(ang) * comp)], fill=(255, 255, 255, 170), width=6)


def nuvem(d, x, y, s):
    for dx, dy, r in ((-60, 10, 50), (0, -15, 65), (65, 10, 50)):
        d.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s], fill=(255, 255, 255, 220))


# ---------------- cenas ----------------
def g_mergulho(d, img, t, T, parte="P1"):
    for i in range(3):
        nuvem(d, (200 + i * 330 + T * -120) % 1300 - 110, 640 + i * 190, 0.8)
    ang = math.radians(62)
    k = (T * 0.55) % 1
    cx, cy = 260 + k * 420, 700 + k * 440
    linhas_vel(d, cx, cy, ang, T, comp=180)
    falcao(d, cx, cy, 1.15, ang, T)
    etiqueta(d, parte)
    # velocímetro
    rotulo(d, 780, 1200, "390 KM/H", 84, AMARELO)


def g_mergulho_cta(d, img, t, T):
    g_mergulho(d, img, t, T)


def aviaozinho(d, x, y, s):
    d.rounded_rectangle([x - 160 * s, y - 40 * s, x + 160 * s, y + 40 * s], 40, fill=(240, 240, 245), outline=O, width=6)
    d.polygon([(x - 40 * s, y), (x - 110 * s, y - 130 * s), (x - 20 * s, y - 130 * s), (x + 40 * s, y)], fill=(220, 60, 60), outline=O)
    d.polygon([(x - 150 * s, y - 20 * s), (x - 200 * s, y - 90 * s), (x - 150 * s, y - 90 * s), (x - 110 * s, y - 20 * s)], fill=(220, 60, 60), outline=O)
    for i in range(3):
        d.ellipse([x + (10 + i * 40) * s, y - 20 * s, x + (40 + i * 40) * s, y + 5 * s], fill=(120, 200, 255), outline=O, width=3)
    d.line([(x + 175 * s, y - 50 * s), (x + 175 * s, y + 50 * s)], fill=O, width=6)


def c_aviao(d, img, t, T):
    selo(d)
    aviaozinho(d, 360 + math.sin(T) * 20, 580, 0.9)
    q = ease((t - 0.4) / 2.5) if t > 0.4 else 0
    ang = math.radians(75)
    fx, fy = 400 + q * 140, 680 + q * 470
    if q > 0.05:
        linhas_vel(d, fx, fy, ang, T, n=6, comp=180)
    falcao(d, fx, fy, 0.75, ang if q > 0.05 else 0, T)
    rotulo(d, 820, 640, "1999", 70, (255, 255, 255))
    if t > 0.6:
        contador(d, 780, 960, 389, t - 0.6, dur=2.5, tam=110, sufixo=" km/h")


def carro_f1(d, x, y, s, T):
    d.polygon([(x - 220 * s, y), (x - 200 * s, y - 50 * s), (x + 40 * s, y - 60 * s), (x + 230 * s, y - 20 * s), (x + 240 * s, y + 10 * s), (x - 220 * s, y + 10 * s)],
              fill=(230, 40, 50), outline=O)
    d.rectangle([x - 240 * s, y - 100 * s, x - 190 * s, y - 50 * s], fill=(230, 40, 50), outline=O, width=5)
    d.ellipse([x - 40 * s, y - 95 * s, x + 30 * s, y - 45 * s], fill=(250, 210, 40), outline=O, width=5)
    for wx in (-150, 150):
        cx, cy = x + wx * s, y + 15 * s
        d.ellipse([cx - 50 * s, cy - 50 * s, cx + 50 * s, cy + 50 * s], fill=(30, 30, 35), outline=O, width=5)
        a = T * 25
        d.line([(cx, cy), (cx + math.cos(a) * 35 * s, cy + math.sin(a) * 35 * s)], fill=(160, 160, 170), width=6)


def c_f1(d, img, t, T):
    selo(d)
    # pista
    d.rectangle([0, 1020, 1080, 1260], fill=(70, 72, 80))
    for i in range(7):
        x = (i * 200 - T * 900) % 1400 - 200
        d.rectangle([x, 1135, x + 110, 1150], fill="white")
    k = min(1, t / 3.0)
    carro_f1(d, 250 + k * 180, 1100, 0.85, T)
    rotulo(d, 250 + k * 180, 1230, "FÓRMULA 1", 44, (255, 255, 255))
    ang = math.radians(8)
    fx = 420 + k * 330
    linhas_vel(d, fx, 760, ang, T, n=5, comp=200)
    falcao(d, fx, 760, 0.9, ang, T)
    rotulo(d, fx, 900, "FALCÃO", 48, AMARELO)


def c_palpebra(d, img, t, T):
    selo(d)
    for i in range(10):  # vento
        y = 560 + i * 70
        x = (T * 700 + i * 137) % 1300 - 200
        d.line([(x, y), (x + 220, y)], fill=(255, 255, 255, 120), width=8)
    # olho gigante
    cx, cy, r = 540, 860, 230
    d.ellipse([cx - r - 40, cy - r - 40, cx + r + 40, cy + r + 40], fill=CINZA2, outline=O, width=8)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BICO, outline=O, width=8)
    d.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78], fill=(30, 20, 15))
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx - r * 0.1, cy - r * 0.2], fill="white")
    ciclo = (t % 1.6) / 1.6
    p = math.sin(ciclo * math.pi) if ciclo < 0.6 else 0
    p = min(1, p * 1.4)
    if p > 0:
        x1 = cx - r + 2 * r * p
        pts = []
        for i in range(41):
            a = math.pi / 2 + i / 40 * math.pi
            pts.append((cx + math.cos(a) * r, cy - math.sin(a) * r))
        borda = [(min(x1, cx + math.sqrt(max(0, r * r - (y - cy) ** 2))), y) for _, y in reversed(pts)]
        d.polygon(pts + borda, fill=(210, 235, 255, 140))
        d.line(borda, fill=(255, 255, 255), width=6)
    if t > 0.5:
        rotulo(d, 540, 1170, "3ª PÁLPEBRA", 72, (210, 235, 255))


def c_cta(d, img, t, T):
    g_mergulho(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="390 KM/H", titulo_y=400, desenho=g_mergulho, fundo=(CEU1, CEU2),
         fala="Esse pássaro mergulha a quase 390 por hora! E o último fato é o pior."),
    dict(tipo="fato", titulo="O FALCÃO", desenho=c_aviao, fundo=((110, 180, 235), (40, 100, 180)),
         fala="É o falcão-peregrino. Segue a Maia, que piora: num teste, uma fêmea saltou de um avião e passou de 380!"),
    dict(tipo="fato", titulo="VENCE A F1", desenho=c_f1, fundo=((120, 190, 240), (60, 130, 200)),
         fala="Isso é mais rápido que um carro de Fórmula 1 na reta. É o animal mais rápido do planeta."),
    dict(tipo="fato", titulo="OLHO BLINDADO", desenho=c_palpebra, fundo=((60, 90, 150), (20, 35, 80)),
         fala="E pra não cegar, ele tem uma terceira pálpebra transparente que limpa o olho no mergulho."),
    dict(tipo="cta", titulo="390 KM/H", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta, fundo=(CEU1, CEU2),
         fala="Mas um veneno quase apagou ele do mapa. Segue a Maia pra ver a parte dois às seis da tarde. Porque esse pássaro..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "falcao_p1.mp4"))
