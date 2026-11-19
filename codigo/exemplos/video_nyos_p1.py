"""Lago Nyos, Parte 1 (LUGARES MORTAIS #4). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, O

SERIE = "LUGARES MORTAIS #4"
MORRO = (60, 110, 70); MORRO2 = (40, 80, 55); LAGO = (40, 90, 150); LAGO2 = (25, 60, 110)
NEVOA = (190, 210, 200); CASA = (190, 140, 90); TELHA = (140, 80, 50); VACA = (240, 240, 235)


def etiqueta(d, parte):
    rotulo(d, 540, 300, f"{SERIE} · {parte}", 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def lua(d, x, y, r=50):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 245, 210))
    d.ellipse([x - r + 22, y - r - 6, x + r + 22, y + r - 6], fill=(15, 20, 45))


def casinha(d, x, y, s=1.0):
    d.rectangle([x - 50 * s, y - 60 * s, x + 50 * s, y], fill=CASA, outline=O, width=4)
    d.polygon([(x - 70 * s, y - 60 * s), (x, y - 120 * s), (x + 70 * s, y - 60 * s)], fill=TELHA, outline=O)
    d.rectangle([x - 14 * s, y - 36 * s, x + 14 * s, y], fill=(60, 40, 30))


def nuvem_gas(d, cx, cy, w, h, T, alfa=170, n=7):
    """Nuvem baixa e pesada de gás (bolhas claras ondulando)."""
    for i in range(n):
        f = i / max(1, n - 1)
        x = cx - w / 2 + f * w
        r = h * (0.55 + 0.25 * math.sin(T * 2 + i * 1.3))
        d.ellipse([x - r, cy - r * 0.8, x + r, cy + r * 0.8], fill=NEVOA + (alfa,))


def cratera(d, T, y=1050):
    d.polygon([(-50, 1920), (-50, y - 120), (260, y - 260), (420, y - 40), (660, y - 40), (820, y - 260), (1130, y - 120), (1130, 1920)],
              fill=MORRO, outline=O)
    d.ellipse([300, y - 90, 780, y + 40], fill=LAGO, outline=O, width=5)
    d.ellipse([360, y - 70, 720, y + 10], fill=LAGO2)


def g_lago(d, img, t, T, parte="P1"):
    etiqueta(d, parte)
    lua(d, 900, 560)
    cratera(d, T, 1060)
    casinha(d, 150, 1260, 0.9)
    casinha(d, 930, 1290, 0.9)
    # nuvem de gás subindo do lago e transbordando
    sobe = 0.5 + 0.5 * math.sin(T * 1.5)
    nuvem_gas(d, 540, 960 - 40 * sobe, 520, 90, T, 190)
    nuvem_gas(d, 540, 1080, 900, 70, T + 1, 120, 9)
    rotulo(d, 540, 820, "SEM FOGO", 46, "white")


def mapa_africa(d, T):
    pts = [(380, 640), (560, 600), (700, 680), (760, 760), (720, 860), (780, 960), (700, 1180), (600, 1300),
           (540, 1240), (520, 1060), (420, 960), (300, 900), (290, 760)]
    d.polygon(pts, fill=(160, 140, 90), outline=O, width=5)
    x, y = 520, 930
    a = 30 + 8 * math.sin(T * 4)
    d.ellipse([x - a, y - a, x + a, y + a], outline=AMARELO, width=7)
    rotulo(d, 540, 1380, "CAMARÕES", 60, AMARELO)


def c_erupcao(d, img, t, T):
    selo(d)
    if t < 2.0:
        mapa_africa(d, T)
        return
    k = ease((t - 2.0) / 1.6)
    d.rectangle([0, 1150, 1080, 1920], fill=MORRO2)
    d.ellipse([200, 1080, 880, 1240], fill=LAGO, outline=O, width=5)
    # coluna de gás explodindo para cima
    for i in range(6):
        y = 1120 - k * (110 + i * 80)
        r = 60 + i * 16
        d.ellipse([540 - r, y - r * 0.7, 540 + r, y + r * 0.7], fill=NEVOA + (200,))
    if t > 2.6:
        rotulo(d, 860, 760, "GÁS CARBÔNICO", 44, "white")
        rotulo(d, 210, 760, "1986", 70, AMARELO)


def c_desce(d, img, t, T):
    selo(d)
    # encosta descendo da esquerda para a direita
    d.polygon([(0, 700), (0, 1920), (1080, 1920), (1080, 1250)], fill=MORRO)
    for x, y in ((520, 1080), (720, 1150), (900, 1210)):
        casinha(d, x, y, 0.8)
    k = ease(t / 3.0)
    frente = 100 + 900 * k
    for i in range(8):
        x = 60 + i * (frente - 60) / 7
        y = 760 + (x / 1080) * 520 - 30
        r = 90 + 15 * math.sin(T * 2 + i)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=NEVOA + (180,))
    seta(d, 300, 640, 760, 900)
    if t > 1.4:
        rotulo(d, 330, 1190, "ATÉ 25 KM", 72, AMARELO)
    rotulo(d, 540, 560, "MAIS PESADO QUE O AR", 44, "white")


def vaquinha(d, x, y, s=1.0):
    d.ellipse([x - 90 * s, y - 45 * s, x + 90 * s, y + 35 * s], fill=VACA, outline=O, width=4)
    d.ellipse([x - 30 * s, y - 30 * s, x + 20 * s, y + 5 * s], fill=O)
    d.ellipse([x + 70 * s, y - 50 * s, x + 140 * s, y + 5 * s], fill=VACA, outline=O, width=4)


def c_silencio(d, img, t, T):
    selo(d)
    d.rectangle([0, 1250, 1080, 1920], fill=MORRO2)
    lua(d, 160, 620, 45)
    casinha(d, 330, 1250, 1.6)
    # Zzz saindo da casa
    for i in range(3):
        f = (T * 0.6 + i / 3) % 1
        rotulo(d, 420 + f * 120, 1000 - f * 200, "Z", int(40 + 30 * f), "white", traduzir=False)
    for i, x in enumerate((690, 900)):
        vaquinha(d, x, 1320 + i * 60, 0.9)
    nuvem_gas(d, 540, 1230, 1100, 60, T, 110, 9)
    rotulo(d, 780, 720, "SEM CHEIRO", 52, "white")
    rotulo(d, 780, 800, "SEM COR", 52, "white")
    if t > 2.2:
        p = pop((t - 2.2) / 0.4)
        rotulo(d, 540, 560, "3.500 ANIMAIS", int(70 * max(0.3, p)), AMARELO)


def c_cta(d, img, t, T):
    g_lago(d, img, t, T, "P1")


CENAS = [
    dict(tipo="gancho", titulo="MATOU 1.746", titulo_y=400, desenho=g_lago, fundo=((20, 30, 70), (5, 10, 30)), estrelas=True,
         fala="Esse lago matou mil e setecentas pessoas numa só noite, sem fogo! E o último fato é o pior."),
    dict(tipo="fato", titulo="O LAGO NYOS", desenho=c_erupcao, fundo=((40, 60, 110), (15, 25, 60)),
         fala="É o Lago Nyos, em Camarões. Segue a Maia, que piora: em 1986 ele soltou uma nuvem gigante de gás carbônico."),
    dict(tipo="fato", titulo="A NUVEM", desenho=c_desce, fundo=((60, 70, 120), (25, 30, 70)),
         fala="O gás é mais pesado que o ar: desceu pelos vales e cobriu vilas inteiras."),
    dict(tipo="fato", titulo="EM SILÊNCIO", desenho=c_silencio, fundo=((25, 30, 70), (8, 10, 35)), estrelas=True,
         fala="Sem cheiro e sem cor. Muita gente morreu dormindo, e uns três mil e quinhentos animais também."),
    dict(tipo="cta", titulo="MATOU 1.746", titulo_y=400, subtitulo="PARTE 2 ÀS 18H", subtitulo_y=520, desenho=c_cta,
         fundo=((20, 30, 70), (5, 10, 30)), estrelas=True,
         fala="E o pior: o gás ainda se junta lá no fundo. Segue a Maia pra ver a parte dois às seis da tarde. Porque esse lago..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "nyos_p1.mp4"))
