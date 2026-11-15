"""Pé de Elefante de Chernobyl: a lava nuclear que matava em minutos. Formato v2 (35–50 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

LAVA = (60, 50, 45); LAVA2 = (95, 80, 70); BRILHO = (170, 255, 80); LARANJA = (255, 140, 40)
CONCRETO = (150, 150, 160); CONCRETO2 = (110, 110, 125)


def ondas_radiacao(d, cx, cy, r0, T, cor=BRILHO, n=4):
    for i in range(n):
        r = r0 + ((T * 120 + i * 60) % 240)
        a = max(0, 220 - int((r - r0) * 0.9))
        d.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75], outline=cor + (a,), width=8)


def simbolo_radiacao(d, cx, cy, r, T, cor=AMARELO):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor, outline=O, width=6)
    rot = T * 40
    for k in range(3):
        a0 = rot + k * 120 - 30
        d.pieslice([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85], a0, a0 + 60, fill=O)
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=cor)
    d.ellipse([cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13], fill=O)


def pe_elefante(d, cx, cy, s, T, rachado=0.0):
    """Massa enrugada e escura, com brilho esverdeado nas rugas."""
    pts = []
    for i in range(40):
        u = i / 39
        a = math.pi + u * math.pi
        rx = 230 * s * (1 + 0.06 * math.sin(u * 23))
        ry = 300 * s * (1 + 0.05 * math.sin(u * 17 + 1))
        pts.append((cx + math.cos(a) * rx, cy + 120 * s + math.sin(a) * ry))
    pts += [(cx + 260 * s, cy + 150 * s), (cx - 260 * s, cy + 150 * s)]
    d.polygon(pts, fill=LAVA, outline=O)
    d.line(pts[:40], fill=O, width=8)
    pulso = 0.5 + 0.5 * math.sin(T * 5)
    g = tuple(int(c * (0.6 + 0.4 * pulso)) for c in BRILHO)
    for k in range(6):  # rugas brilhando
        y = cy - 120 * s + k * 48 * s
        w = 150 * s * (0.6 + 0.4 * math.sin(k * 1.7))
        d.arc([cx - w, y - 18 * s, cx + w, y + 18 * s], 10, 170, fill=g, width=max(3, int(7 * s)))
    for k in range(3):  # "dedos" na base
        x = cx - 160 * s + k * 160 * s
        d.ellipse([x - 60 * s, cy + 110 * s, x + 60 * s, cy + 170 * s], fill=LAVA2, outline=O, width=5)
    if rachado > 0:
        for k in range(4):
            x0 = cx - 120 * s + k * 80 * s
            d.line([(x0, cy - 160 * s), (x0 + 30 * s, cy - 60 * s * rachado), (x0 - 10 * s, cy + 40 * s * rachado)],
                   fill=(20, 20, 20), width=6)


def contador_geiger(d, x, y, T, alarme=True):
    d.rounded_rectangle([x - 90, y - 120, x + 90, y + 120], 20, fill=(240, 200, 40), outline=O, width=6)
    d.rectangle([x - 65, y - 95, x + 65, y - 10], fill=(230, 240, 220), outline=O, width=4)
    ang = -150 + 120 * (0.8 + 0.2 * math.sin(T * 30)) if alarme else -120
    a = math.radians(ang)
    d.line([(x, y - 20), (x + math.cos(a) * 60, y - 20 + math.sin(a) * 60)], fill=(220, 30, 30), width=6)
    d.ellipse([x - 25, y + 30, x + 25, y + 80], fill=(220, 30, 30) if int(T * 8) % 2 else (120, 20, 20), outline=O, width=4)
    d.line([(x + 90, y + 40), (x + 150, y + 100)], fill=O, width=10)
    d.ellipse([x + 130, y + 80, x + 190, y + 140], fill=(200, 200, 200), outline=O, width=5)


# ---------------- cenas ----------------
def g_pe(d, img, t, T):
    k = pop(t / 0.4) if t < 0.4 else 1
    ondas_radiacao(d, 640, 900, 200, T)
    pe_elefante(d, 640, 820, 1.0 * max(0.3, k), T)
    contador_geiger(d, 170, 640, T)
    if t > 0.3:
        rotulo(d, 640, 1215, "5 MINUTOS", 70, (255, 90, 80))


def c_reator(d, img, t, T):
    # corte do prédio: lava escorrendo do reator até o porão
    d.rectangle([180, 480, 900, 1220], fill=CONCRETO, outline=O, width=8)
    for yy in (720, 960):
        d.rectangle([180, yy, 900, yy + 30], fill=CONCRETO2, outline=O, width=4)
    d.rounded_rectangle([380, 520, 700, 700], 30, fill=(90, 90, 100), outline=O, width=6)
    fogo = 0.5 + 0.5 * math.sin(T * 9)
    d.ellipse([440, 560, 640, 680], fill=(255, int(120 + 80 * fogo), 40))
    k = ease(t / 2.4)
    for i, x in enumerate((470, 560, 620)):  # filetes de lava descendo
        fim = 700 + k * (480 - i * 40)
        d.line([(x, 690), (x + math.sin(T * 2 + i) * 12, fim)], fill=LARANJA, width=30)
        d.ellipse([x - 26, fim - 20, x + 26, fim + 26], fill=LARANJA, outline=O, width=3)
    if k > 0.9:
        d.ellipse([400, 1150, 700, 1215], fill=LAVA, outline=O, width=5)
    rotulo(d, 800, 610, "1986", 58, AMARELO)


def ingrediente(d, x, y, nome, cor, forma):
    if forma == "barra":
        d.rounded_rectangle([x - 30, y - 80, x + 30, y + 60], 14, fill=cor, outline=O, width=5)
    elif forma == "monte":
        d.polygon([(x - 80, y + 60), (x, y - 60), (x + 80, y + 60)], fill=cor, outline=O)
    elif forma == "bloco":
        d.rectangle([x - 70, y - 50, x + 70, y + 60], fill=cor, outline=O, width=5)
    else:
        d.polygon([(x - 70, y + 40), (x - 30, y - 60), (x + 70, y - 30), (x + 40, y + 60)], fill=cor, outline=O)
    rotulo(d, x, y + 105, nome, 38)


def c_mistura(d, img, t, T):
    itens = [("URÂNIO", BRILHO, "barra"), ("AREIA", (230, 200, 120), "monte"),
             ("CONCRETO", CONCRETO, "bloco"), ("METAL", (190, 200, 215), "chapa")]
    for i, (n, c, f) in enumerate(itens):
        if t > i * 0.35:
            ingrediente(d, 150 + i * 260, 580, n, c, f)
    if t > 1.5:
        seta(d, 540, 790, 540, 880, cor=AMARELO, w=14)
        pe_elefante(d, 540, 1010, 0.7 * pop((t - 1.5) / 0.4), T)


def c_hoje(d, img, t, T):
    pe_elefante(d, 480, 860, 0.85, T, rachado=ease(t / 2.0))
    for k in range(12):  # poeira saindo
        x = 300 + k * 35 + math.sin(T * 2 + k) * 20
        y = 1060 - ((T * 70 + k * 37) % 300)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(150, 140, 130, 180))
    simbolo_radiacao(d, 860, 600, 85, T)
    rotulo(d, 540, 1200, "AINDA RADIOATIVO", 54, BRILHO)


CENAS = [
    dict(tipo="gancho", titulo="LAVA MORTAL", desenho=g_pe, fundo=((70, 90, 40), (15, 25, 15)),
         fala="Ficar cinco minutos perto disso podia te matar. E ninguém fez isso de propósito."),
    dict(tipo="fato", titulo="REATOR DERRETEU", desenho=c_reator, fundo=((150, 70, 40), (50, 20, 20)),
         fala="É o Pé de Elefante, em Chernobyl. Em mil novecentos e oitenta e seis, o reator derreteu e virou uma lava que escorreu pelo prédio."),
    dict(tipo="fato", titulo="RECEITA DO MAL", desenho=c_mistura, fundo=((60, 70, 110), (20, 25, 45)),
         fala="Essa lava misturou combustível nuclear com areia, concreto e metal, e endureceu no porão, com a cara enrugada de um pé de elefante."),
    dict(tipo="fato", titulo="E HOJE?", desenho=c_hoje, fundo=((50, 60, 60), (15, 20, 20)),
         fala="Hoje ela está bem mais fraca, mas continua radioativa e está rachando, virando poeira."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Você chegaria perto?",
         fala="Comenta: você chegaria perto do Pé de Elefante? E segue a Maia, todo dia tem uma dessas!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "pe_de_elefante.mp4"))
