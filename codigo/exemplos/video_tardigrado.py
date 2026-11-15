"""Tardígrado (urso-d'água): o bicho que sobreviveu ao vácuo do espaço. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, olhos, seta, brilhos, terra, termometro, O

CORPO = (235, 200, 160); CORPO2 = (200, 160, 120); MUSGO = (90, 160, 70); MUSGO2 = (60, 120, 50)
GELO = (190, 230, 255); FOGO = (255, 120, 40)


def tardigrado(d, cx, cy, s, T, cor=CORPO, cor2=CORPO2, seco=0.0):
    """Urso-d'água gordinho de lado, 8 patinhas (4 visíveis de cada lado ~ desenhamos 4 pares em fila).
    seco=1 vira 'barrilzinho' (tun) encolhido."""
    k = 1 - 0.45 * seco
    w, h = 260 * s * k, 120 * s * (1 - 0.1 * seco)
    if seco < 0.5:
        for i in range(4):  # patinhas
            px = cx - w * 0.75 + i * w * 0.5
            bal = math.sin(T * 6 + i * 1.4) * 10 * s * (1 - seco)
            d.rounded_rectangle([px - 20 * s, cy + h * 0.4, px + 20 * s, cy + h * 0.4 + 70 * s * (1 - seco)],
                                int(18 * s), fill=cor2, outline=O, width=4)
            for g in (-1, 0, 1):
                d.line([(px + g * 10 * s, cy + h * 0.4 + 70 * s * (1 - seco)),
                        (px + g * 14 * s + bal * 0.3, cy + h * 0.4 + 88 * s * (1 - seco))], fill=O, width=max(2, int(4 * s)))
    d.ellipse([cx - w, cy - h, cx + w, cy + h * 0.8], fill=cor, outline=O, width=6)
    for i in range(1, 5):  # gomos
        x = cx - w + i * w * 0.4
        d.arc([x - 30 * s, cy - h * 0.95, x + 30 * s, cy + h * 0.75], 250, 290, fill=cor2, width=max(3, int(5 * s)))
    # cabeça (direita) com boquinha em tubo
    hx = cx + w * 0.85
    d.ellipse([hx - 70 * s * k, cy - 75 * s, hx + 60 * s * k, cy + 55 * s], fill=cor, outline=O, width=5)
    d.ellipse([hx + 40 * s * k, cy - 18 * s, hx + 72 * s * k, cy + 14 * s], fill=cor2, outline=O, width=4)
    if seco < 0.5:
        d.ellipse([hx - 10 * s, cy - 40 * s, hx + 8 * s, cy - 22 * s], fill=O)
    else:
        d.line([(hx - 12 * s, cy - 30 * s), (hx + 10 * s, cy - 30 * s)], fill=O, width=max(3, int(5 * s)))


def foguete(d, cx, cy, s, T):
    d.polygon([(cx, cy - 200 * s), (cx - 70 * s, cy - 60 * s), (cx + 70 * s, cy - 60 * s)], fill=(230, 60, 60), outline=O)
    d.rectangle([cx - 70 * s, cy - 60 * s, cx + 70 * s, cy + 140 * s], fill=(240, 240, 245), outline=O, width=5)
    d.ellipse([cx - 35 * s, cy - 20 * s, cx + 35 * s, cy + 50 * s], fill=(120, 200, 255), outline=O, width=5)
    for sx in (-1, 1):
        d.polygon([(cx + sx * 70 * s, cy + 60 * s), (cx + sx * 130 * s, cy + 170 * s), (cx + sx * 70 * s, cy + 140 * s)],
                  fill=(230, 60, 60), outline=O)
    f = 60 + 25 * math.sin(T * 20)
    d.polygon([(cx - 45 * s, cy + 140 * s), (cx, cy + (140 + f) * s), (cx + 45 * s, cy + 140 * s)], fill=FOGO)


# ---------------- cenas ----------------
def g_espaco(d, img, t, T):
    terra(d, 860, 1150, 260, T, rosto=False)
    flut = math.sin(T * 1.5) * 25
    tardigrado(d, 560, 780 + flut, 1.25, T)
    d.ellipse([300, 560 + flut, 820, 1010 + flut], outline=(180, 220, 255), width=6)  # bolha de "vácuo"
    if t > 0.2:
        brilhos(d, 560, 780 + flut, 330, T, n=6, cor=(255, 255, 255))


def c_musgo(d, img, t, T):
    for i in range(9):  # musgo
        x = 60 + i * 120
        d.ellipse([x - 90, 1040 - (i % 3) * 30, x + 90, 1200], fill=MUSGO if i % 2 else MUSGO2, outline=O, width=4)
    # lupa
    cx, cy, r = 560, 760, 250
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 245, 255), outline=O, width=12)
    d.line([(cx - r * 0.7, cy + r * 0.7), (cx - r * 1.1, cy + r * 1.15)], fill=O, width=40)
    tardigrado(d, cx - 20, cy, 0.75, T)
    if t > 1.0:
        rotulo(d, 560, 1130, __import__("idioma").num(0.5, 1) + " mm", 66, AMARELO, traduzir=False)


def c_barril(d, img, t, T):
    seco = ease((t - 0.6) / 1.4)
    tardigrado(d, 380, 860, 0.95, T, seco=seco)
    # gota de água sumindo
    g = 1 - seco
    if g > 0.05:
        d.ellipse([780 - 60 * g, 800 - 80 * g, 780 + 60 * g, 800 + 80 * g], fill=(90, 180, 255), outline=O, width=5)
    if t > 2.0:
        rotulo(d, 540, 1130, "MODO BARRIL", 62, AMARELO)


def c_extremos(d, img, t, T):
    termometro(d, 260, 1060, 0.08, cor=(80, 160, 255), h=440)
    termometro(d, 820, 1060, 0.95, cor=(235, 60, 40), h=440)
    rotulo(d, 260, 520, "-272 °C", 54, GELO, traduzir=False)
    rotulo(d, 820, 520, "150 °C", 54, (255, 180, 140), traduzir=False)
    tardigrado(d, 540, 900, 0.55, T, seco=1.0)
    if t > 1.4:
        rotulo(d, 540, 1150, "SOBREVIVE", 62, (255, 255, 255))


def c_foguete(d, img, t, T):
    k = ease(t / 2.0)
    foguete(d, 330, 1000 - k * 260, 1.0, T)
    terra(d, 1000, 560, 130, T, rosto=False)
    # cápsula aberta no espaço com tardígrados
    d.rounded_rectangle([640, 700, 980, 900], 30, fill=(200, 200, 215), outline=O, width=6)
    for i in range(3):
        tardigrado(d, 700 + i * 110, 800, 0.25, T + i, seco=1.0)
    if t > 1.0:
        rotulo(d, 810, 980, "10 DIAS", 60, AMARELO)
    if t > 1.8:
        rotulo(d, 810, 1080, "NO ESPAÇO", 56, (255, 255, 255))


CENAS = [
    dict(tipo="gancho", titulo="SOBREVIVE A TUDO", desenho=g_espaco, fundo=((20, 20, 70), (5, 5, 25)),
         fala="Esse bichinho já foi jogado no vácuo do espaço e voltou vivo! E o truque dele é ainda mais estranho."),
    dict(tipo="fato", titulo="URSO-D'ÁGUA", desenho=c_musgo, fundo=((120, 190, 130), (40, 90, 60)),
         fala="É o tardígrado, o urso-d'água. Tem oito patinhas, mede meio milímetro e pode estar no musgo do seu quintal."),
    dict(tipo="fato", titulo="VIRA UM BARRIL", desenho=c_barril, fundo=((220, 170, 90), (110, 70, 30)),
         fala="Quando falta água, ele se seca quase inteiro, encolhe as patas e vira um barrilzinho, quase sem metabolismo."),
    dict(tipo="fato", titulo="GELO E FOGO", desenho=c_extremos, fundo=((100, 80, 160), (30, 20, 60)),
         fala="Assim, aguenta frio perto do zero absoluto e mais de cento e cinquenta graus, por alguns minutos."),
    dict(tipo="fato", titulo="TESTE NO ESPAÇO", desenho=c_foguete, fundo=((10, 15, 50), (0, 0, 15)),
         estrelas=True,
         fala="Em dois mil e sete, cientistas deixaram tardígrados dez dias expostos ao espaço. Muitos voltaram vivos e até tiveram filhotes!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Ele é fofo ou assustador?",
         fala="Comenta: ele é fofo ou assustador? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "tardigrado.mp4"))
