"""Vespa-do-mar (Chironex fleckeri): água-viva que pode matar em minutos. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, brilhos, seta, O

GEL = (170, 230, 255, 150); GEL_O = (90, 170, 230); TENT = (200, 160, 255); VERMELHO = (235, 55, 60)
ROXO = (160, 90, 230); VINAGRE = (240, 220, 140)


def vespa(d, cx, cy, s, T, olhinhos=False, n_tent=4, comp=1.0):
    """Água-viva-caixa: sino cúbico translúcido + tentáculos nos 4 cantos."""
    pulso = 1 + 0.05 * math.sin(T * 4)
    w, h = 170 * s * pulso, 190 * s / pulso
    # tentáculos (ondulados)
    for i in range(n_tent):
        bx = cx - w * 0.85 + i * (w * 1.7 / max(1, n_tent - 1))
        for f in range(3):
            pts = []
            for k in range(14):
                yy = cy + h * 0.5 + k * 32 * s * comp
                xx = bx + (f - 1) * 10 * s + math.sin(T * 3 + k * 0.6 + i + f) * 14 * s * (k / 14 + 0.3)
                pts.append((xx, yy))
            d.line(pts, fill=TENT, width=max(3, int(6 * s)))
    # sino quadrado
    d.rounded_rectangle([cx - w, cy - h * 0.6, cx + w, cy + h * 0.55], int(70 * s), fill=GEL, outline=GEL_O, width=7)
    d.rounded_rectangle([cx - w * 0.6, cy - h * 0.35, cx + w * 0.6, cy + h * 0.3], int(40 * s), outline=(220, 245, 255), width=4)
    if olhinhos:
        for lado in (-1, 1):
            for j in range(3):
                ex, ey = cx + lado * w * 0.78, cy + h * 0.15 + j * 26 * s - 26 * s
                d.ellipse([ex - 9 * s, ey - 9 * s, ex + 9 * s, ey + 9 * s], fill="white", outline=O, width=3)
                d.ellipse([ex - 4 * s, ey - 3 * s, ex + 4 * s, ey + 5 * s], fill=O)


def caveira(d, x, y, s):
    d.ellipse([x - s, y - s, x + s, y + s * 0.8], fill=(245, 245, 245), outline=O, width=5)
    d.rounded_rectangle([x - s * 0.55, y + s * 0.5, x + s * 0.55, y + s * 1.1], 8, fill=(245, 245, 245), outline=O, width=5)
    for sx in (-1, 1):
        d.ellipse([x + sx * s * 0.45 - s * 0.28, y - s * 0.15, x + sx * s * 0.45 + s * 0.28, y + s * 0.35], fill=O)


def relogio(d, x, y, r, T):
    d.ellipse([x - r, y - r, x + r, y + r], fill="white", outline=O, width=7)
    a = T * 4
    d.line([(x, y), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)], fill=VERMELHO, width=8)
    d.line([(x, y), (x, y - r * 0.55)], fill=O, width=8)


# ---------------- cenas ----------------
def g_vespa(d, img, t, T):
    vespa(d, 600, 600 + math.sin(T * 1.5) * 15, 1.25, T, comp=1.3)
    caveira(d, 880, 980, 60)
    relogio(d, 220, 1000, 80, T)
    if t > 0.7:
        rotulo(d, 600, 1220, "QUASE INVISÍVEL", 56, CIANO)


def c_olhos(d, img, t, T):
    vespa(d, 540, 640, 1.5, T, olhinhos=True, comp=0.6)
    if t > 0.5:
        # cérebro riscado
        bx, by = 220, 1050
        d.ellipse([bx - 90, by - 65, bx + 90, by + 65], fill=(255, 170, 190), outline=O, width=6)
        d.arc([bx - 50, by - 40, bx + 10, by + 30], 200, 340, fill=O, width=5)
        d.arc([bx - 10, by - 30, bx + 60, by + 40], 200, 340, fill=O, width=5)
        e = ease((t - 0.5) / 0.4)
        d.line([(bx - 110, by - 90), (bx - 110 + 220 * e, by - 90 + 180 * e)], fill=VERMELHO, width=18)
    if t > 1.4:
        rotulo(d, 720, 1050, "24 OLHOS", 72, AMARELO)


def c_tentaculos(d, img, t, T):
    k = ease(t / 1.5)
    vespa(d, 330, 520, 0.8, T, comp=0.4 + 1.6 * k, n_tent=4)
    # régua de 3 metros e pessoa para comparar
    d.rounded_rectangle([640, 470, 700, 1230], 10, fill=AMARELO, outline=O, width=5)
    for i in range(7):
        y = 470 + i * 126
        d.line([(640, y), (670, y)], fill=O, width=5)
    rotulo(d, 770, 500, "3 m", 60, AMARELO)
    px, py = 860, 900
    d.ellipse([px - 50, py - 50, px + 50, py + 50], fill=(252, 214, 188), outline=O, width=6)
    olhos(d, px, py - 5, T, esp=40, r=11)
    d.line([(px, py + 50), (px, py + 220)], fill=(60, 140, 220), width=34)
    for sx in (-1, 1):
        d.line([(px, py + 90), (px + sx * 70, py + 180)], fill=(60, 140, 220), width=20)
        d.line([(px, py + 220), (px + sx * 40, py + 330)], fill=(40, 50, 90), width=22)
    rotulo(d, px, py - 90, "1,7 m", 40, (255, 255, 255))
    if t > 1.6:
        brilhos(d, 330, 1000, 160, T, n=8, cor=ROXO)


def c_coracao(d, img, t, T):
    b = 1 + 0.12 * abs(math.sin(T * (6 if t < 1.5 else 14)))
    cx, cy, s = 540, 780, 150 * b
    d.ellipse([cx - s, cy - s * 0.9, cx, cy + s * 0.1], fill=VERMELHO, outline=O, width=7)
    d.ellipse([cx, cy - s * 0.9, cx + s, cy + s * 0.1], fill=VERMELHO, outline=O, width=7)
    d.polygon([(cx - s * 0.97, cy - s * 0.3), (cx + s * 0.97, cy - s * 0.3), (cx, cy + s * 1.0)], fill=VERMELHO)
    d.line([(cx - s * 0.97, cy - s * 0.3), (cx, cy + s * 1.0), (cx + s * 0.97, cy - s * 0.3)], fill=O, width=7)
    # raio de veneno roxo
    if t > 0.6:
        z = [(820, 470), (720, 640), (790, 650), (660, 850)]
        d.line(z, fill=ROXO, width=26)
        d.line(z, fill=(230, 200, 255), width=8)
    # gráfico de batimento
    pts = []
    for i in range(60):
        x = 150 + i * 13
        fase = (i + T * 30) % 20
        y = 1150 - (90 if 9 < fase < 11 else 0) * (1 if i % 2 else -0.5)
        pts.append((x, y))
    d.line(pts, fill=(90, 255, 140), width=6)
    if t > 1.8:
        rotulo(d, 540, 1240, "EM MINUTOS", 56, AMARELO)


def c_vinagre(d, img, t, T):
    # placa de praia com garrafa de vinagre
    d.rectangle([180, 460, 220, 1250], fill=(120, 80, 50), outline=O, width=5)
    d.rounded_rectangle([90, 500, 520, 700], 20, fill=(255, 250, 240), outline=O, width=7)
    rotulo(d, 305, 600, "VINAGRE", 60, (200, 60, 40))
    gx, gy = 720, 870
    d.rounded_rectangle([gx - 110, gy - 140, gx + 110, gy + 260], 40, fill=VINAGRE, outline=O, width=7)
    d.rectangle([gx - 45, gy - 230, gx + 45, gy - 135], fill=VINAGRE, outline=O, width=6)
    d.rectangle([gx - 55, gy - 270, gx + 55, gy - 225], fill=VERMELHO, outline=O, width=6)
    d.rounded_rectangle([gx - 90, gy - 20, gx + 90, gy + 120], 14, fill="white", outline=O, width=4)
    rotulo(d, gx, gy + 50, "5%", 56, (200, 60, 40), traduzir=False)
    # areia e ondas
    d.rectangle([0, 1180, 1080, 1260], fill=(240, 210, 140))
    for i in range(6):
        x = (i * 200 + T * 80) % 1200 - 100
        d.arc([x, 1130, x + 200, 1220], 180, 360, fill=(120, 210, 255), width=10)
    if t > 1.2:
        brilhos(d, gx, gy + 40, 200, T, n=8)


CENAS = [
    dict(tipo="gancho", titulo="MATA EM MINUTOS", desenho=g_vespa, fundo=((10, 90, 150), (5, 25, 60)),
         fala="Essa água-viva quase transparente pode matar uma pessoa em minutos. E ela nem tem cérebro!"),
    dict(tipo="fato", titulo="SEM CÉREBRO", desenho=c_olhos, fundo=((20, 120, 140), (5, 40, 60)),
         fala="É a vespa-do-mar, da Austrália. Ela não tem cérebro, mas tem vinte e quatro olhos."),
    dict(tipo="fato", titulo="3 METROS DE VENENO", desenho=c_tentaculos, fundo=((60, 40, 130), (15, 10, 50)),
         fala="Os tentáculos chegam a três metros e têm milhões de arpõezinhos cheios de veneno."),
    dict(tipo="fato", titulo="ATACA O CORAÇÃO", desenho=c_coracao, fundo=((120, 20, 50), (40, 5, 20)),
         fala="O veneno ataca o coração tão rápido que tem vítima que nem consegue sair da água."),
    dict(tipo="fato", titulo="SALVO PELO VINAGRE", desenho=c_vinagre, fundo=((30, 140, 200), (10, 60, 110)),
         fala="Por isso, nas praias da Austrália tem vinagre: ele desarma os arpões que ainda não dispararam."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você entraria nesse mar?",
         fala="Comenta: você entraria nesse mar? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "vespa_do_mar.mp4"))
