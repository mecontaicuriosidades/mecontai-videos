"""Besouro-bombardeiro, Parte 2 (BICHOS INSANOS #12). Importa desenhos de video_besouro_p1.
Fatos: Sugiura & Sato 2018 (Biology Letters; National Geographic; Smithsonian): sapos japoneses (Bufo japonicus)
engoliram besouros-bombardeiros (Pheropsophus jessoensis); dentro do estômago o besouro dispara o jato quente;
43% dos sapos vomitaram o besouro, entre 12 e 107 minutos depois, e todos os besouros vomitados estavam vivos
e ativos (a maioria sobreviveu semanas depois)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_besouro_p1 import etiqueta, selo, besouro, jato, chao, TERRA1, TERRA2, JATO, JATO2

SAPO = (120, 160, 70); SAPO2 = (90, 125, 50); BARRIGA = (225, 215, 160)


def sapo(d, cx, cy, s=1.0, T=0.0, boca=0.0, raiox=False):
    """Sapo sentado de frente. boca 0..1 abre a boca. raiox mostra a barriga como janela."""
    infla = 1 + math.sin(T * 3) * 0.02
    w, h = 260 * s * infla, 200 * s
    # patas
    for dx in (-1, 1):
        d.ellipse([cx + dx * w * 0.75 - 70 * s, cy + h * 0.55, cx + dx * w * 0.75 + 70 * s, cy + h * 0.85], fill=SAPO2, outline=O, width=6)
    d.ellipse([cx - w, cy - h * 0.6, cx + w, cy + h * 0.8], fill=SAPO, outline=O, width=max(4, int(8 * s)))
    # verrugas
    for i in range(7):
        a = i * 0.9 + 0.4
        d.ellipse([cx + math.cos(a) * w * 0.7 - 10 * s, cy - h * 0.2 + math.sin(a) * h * 0.3 - 10 * s,
                   cx + math.cos(a) * w * 0.7 + 10 * s, cy - h * 0.2 + math.sin(a) * h * 0.3 + 10 * s], fill=SAPO2)
    # barriga
    bw, bh = w * 0.55, h * 0.5
    d.ellipse([cx - bw, cy + h * 0.05, cx + bw, cy + h * 0.05 + bh * 1.4], fill=BARRIGA if not raiox else (60, 25, 25), outline=O, width=6)
    # olhos
    for dx in (-1, 1):
        ex, ey = cx + dx * w * 0.5, cy - h * 0.62
        d.ellipse([ex - 50 * s, ey - 50 * s, ex + 50 * s, ey + 50 * s], fill=SAPO, outline=O, width=6)
        d.ellipse([ex - 30 * s, ey - 30 * s, ex + 30 * s, ey + 30 * s], fill=(255, 220, 60), outline=O, width=4)
        d.rectangle([ex - 22 * s, ey - 6 * s, ex + 22 * s, ey + 6 * s], fill=O)
    # boca
    if boca > 0.05:
        d.chord([cx - w * 0.6, cy - h * 0.35, cx + w * 0.6, cy - h * 0.35 + 160 * s * boca], 0, 180, fill=(170, 40, 60), outline=O, width=6)
    else:
        d.arc([cx - w * 0.6, cy - h * 0.6, cx + w * 0.6, cy - h * 0.1], 20, 160, fill=O, width=6)
    return (cx, cy + h * 0.05 + bh * 0.7, bw, bh)


def g_dentro(d, img, t, T, label=True):
    etiqueta(d, "P2")
    chao(d)
    bx, by, bw, bh = sapo(d, 540, 870, 1.15, T, raiox=True)
    besouro(d, bx + 20, by, 0.5, T, lado=1)
    jato(d, bx - 45, by - 5, math.pi + math.sin(T * 2) * 0.6, 0.35, T, comp=0.6)
    if label:
        kk = pop(min(1, max(0, t - 0.3) / 0.5))
        if kk > 0.05:
            rotulo(d, 540, 1210, "DENTRO DO SAPO", int(52 * kk) + 1, AMARELO)


def c_engole(d, img, t, T):
    selo(d)
    chao(d)
    k = ease(t / 1.0)
    sapo(d, 330, 900, 0.85, T, boca=0.7 if k < 0.95 else 0.0)
    # língua puxando o besouro
    bx = 900 - 500 * k
    if k < 0.95:
        d.line([(340, 830), (bx - 60, 1020)], fill=(230, 90, 120), width=22)
        besouro(d, bx, 1020, 0.6, T, lado=-1)
    else:
        kk = pop(min(1, (t - 1.0) / 0.4))
        rotulo(d, 720, 700, "GLUP!", int(90 * kk) + 1, AMARELO)


def c_barriga(d, img, t, T):
    selo(d)
    # corte da barriga: besouro disparando dentro, ondas de calor
    cx, cy = 540, 880
    d.ellipse([cx - 330, cy - 260, cx + 330, cy + 300], fill=(150, 50, 60), outline=O, width=10)
    d.ellipse([cx - 280, cy - 210, cx + 280, cy + 250], fill=(95, 25, 35))
    besouro(d, cx + 60, cy + 20, 0.85, T, lado=1)
    jato(d, cx - 60, cy + 10, math.pi + math.sin(T * 3) * 0.8, 0.6, T, comp=0.65)
    for i in range(4):
        y = cy - 180 + i * 110
        pts = [(cx + 300 + math.sin(T * 6 + i + k * 0.7) * 12, y + k * 12) for k in range(8)]
        d.line(pts, fill=(255, 150, 60), width=6)
    kk = pop(min(1, max(0, t - 0.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1240, "JATO QUENTE LÁ DENTRO", int(44 * kk) + 1, (255, 120, 80))


def c_vomita(d, img, t, T):
    selo(d)
    chao(d)
    k = min(1.0, t / 1.3)
    sapo(d, 360, 930, 0.85, T, boca=0.9 if k > 0.35 else 0.2)
    if k > 0.35:
        f = ease((k - 0.35) / 0.65)
        bx, by = 420 + 430 * f, 780 - 200 * math.sin(f * 3.14)
        besouro(d, bx, by, 0.6, T, lado=1)
        for i in range(5):
            r = 14 + i * 4
            px, py = bx - 70 - i * 55, by + 20 + i * 10
            d.ellipse([px - r, py - r, px + r, py + r], fill=(200, 230, 120), outline=O, width=3)
        kk = pop(min(1, (t - 0.6) / 0.4))
        rotulo(d, 830, 600, "VIVO!", int(90 * kk) + 1, AMARELO)
    kk = pop(min(1, max(0, t - 1.6) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1190, "QUASE METADE DOS SAPOS", int(42 * kk) + 1, (255, 255, 255))
        rotulo(d, 540, 1245, "ATÉ QUASE 2 HORAS DEPOIS", int(38 * kk) + 1, CIANO)


def c_cta(d, img, t, T):
    g_dentro(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="DENTRO!", titulo_y=400, desenho=g_dentro, fundo=(TERRA1, TERRA2),
         fala="Esse besouro do jato fervendo sobrevive até dentro de um sapo! E o fim é o mais louco."),
    dict(tipo="fato", titulo="ENGOLIDO", desenho=c_engole, fundo=((40, 80, 60), (10, 25, 18)),
         fala="O sapo engole ele inteiro. Segue a Maia, porque fica mais louco:"),
    dict(tipo="fato", titulo="NA BARRIGA", desenho=c_barriga, fundo=((80, 25, 40), (20, 5, 10)),
         fala="lá dentro, o besouro dispara o jato quente na barriga do sapo."),
    dict(tipo="fato", titulo="VOMITADO!", desenho=c_vomita, fundo=((30, 60, 90), (8, 15, 30)),
         fala="Num estudo no Japão, quase metade dos sapos vomitou o besouro, vivo! Eu nunca mais comia nada!"),
    dict(tipo="cta", titulo="DENTRO!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=(TERRA1, TERRA2),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. E lembra: esse besouro..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "besouro_p2.mp4"))
