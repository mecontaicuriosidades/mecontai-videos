"""Você já teve rabo (CIÊNCIA BIZARRA #6). Formato v3 + ESTRATÉGIA DA SEMANA 23/11.
Fatos (Live Science "Why don't people have tails?"; Scientific American "How humans lost their tails";
Xia et al., Nature, fev/2024): o embrião humano tem por pouco tempo um rabo, com vértebras, no 1º mês e
pouco de desenvolvimento (quando mede menos de 1 cm); por volta da 8ª semana ele some por morte programada
de células (apoptose) e sobram umas 3 ou 4 vértebras fundidas: o cóccix. A perda do rabo nos ancestrais
de humanos e macacos (~25 milhões de anos) foi ligada a um "gene saltador" (elemento AluY) que entrou no
gene TBXT; camundongos com a mesma mudança nasceram com rabo curto ou sem rabo."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "CIÊNCIA BIZARRA #6"
PELE = (255, 175, 170); PELE2 = (230, 130, 135)
BOLSA = (255, 120, 150); LIQ = (120, 40, 70)
OSSO = (250, 245, 225)
FEIJAO = (150, 60, 40)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def embriao(d, cx, cy, s=1.0, T=0.0, rabo=1.0, vertebras=True):
    """Embrião enrolado em C: cabeção, corpo curvo, brotinhos de braço/perna e rabo (rabo 0..1)."""
    bal = math.sin(T * 1.5) * 6 * s
    cy = cy + bal
    # corpo (arco grosso)
    pts = []
    for j in range(14):
        a = -2.2 + j / 13 * 3.4
        pts.append((cx + math.cos(a) * 120 * s, cy + math.sin(a) * 140 * s))
    d.line(pts, fill=O, width=int(118 * s), joint="curve")
    d.line(pts, fill=PELE, width=int(104 * s), joint="curve")
    # rabo saindo do fim do corpo, enrolando para dentro
    if rabo > 0.02:
        ex, ey = pts[-1]
        rp = []
        n = 10
        for j in range(n):
            u = j / (n - 1) * rabo
            a = 1.2 + u * 2.2 + math.sin(T * 3) * 0.1 * u
            rp.append((ex + math.cos(a) * 90 * s * u - 30 * s * u, ey + math.sin(a) * 60 * s * u))
        larg = int(44 * s)
        for j in range(len(rp) - 1):
            w = max(6, int(larg * (1 - j / n)))
            d.line([rp[j], rp[j + 1]], fill=O, width=w + 10)
        for j in range(len(rp) - 1):
            w = max(4, int(larg * (1 - j / n)))
            d.line([rp[j], rp[j + 1]], fill=PELE2, width=w)
        if vertebras:
            for j in range(1, len(rp) - 1, 1):
                x, y = rp[j]
                r = max(3, int(9 * s * (1 - j / n)))
                d.ellipse([x - r, y - r, x + r, y + r], fill=OSSO, outline=O, width=2)
    # cabeção
    hx, hy = pts[0][0] - 10 * s, pts[0][1] - 20 * s
    d.ellipse([hx - 120 * s, hy - 110 * s, hx + 110 * s, hy + 110 * s], fill=PELE, outline=O, width=7)
    d.ellipse([hx - 60 * s, hy - 10 * s, hx - 20 * s, hy + 30 * s], fill=(60, 30, 40))
    # brotinhos de braço e perna
    for k, j in enumerate((5, 10)):
        x, y = pts[j]
        d.ellipse([x - 60 * s, y - 25 * s, x + 10 * s, y + 25 * s], fill=PELE, outline=O, width=5)


def bolsa(d, cx, cy, r, T):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIQ, outline=BOLSA, width=12)
    for i in range(10):
        a = i * 0.63 + T * 0.4
        x, y = cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(200, 110, 140))


def g_rabo(d, img, t, T, label=True):
    etiqueta(d)
    bolsa(d, 560, 880, 330, T)
    embriao(d, 600, 880, 1.25, T, rabo=1.0)
    if label:
        k = pop(min(1, max(0, t - 0.5) / 0.5))
        if k > 0.05:
            rotulo(d, 860, 1180, "RABO!", int(60 * k) + 1, AMARELO)
            seta(d, 830, 1140, 700, 1070, AMARELO, 12)
            rotulo(d, 240, 600, "VOCÊ", int(52 * k) + 1, CIANO)


def c_feijao(d, img, t, T):
    selo(d)
    # comparação de tamanho: embrião x grão de feijão
    k = ease(t / 0.8)
    embriao(d, 300, 870, 0.5 * k + 0.05, T)
    fx, fy = 760, 850
    d.ellipse([fx - 210, fy - 130, fx + 210, fy + 130], fill=FEIJAO, outline=O, width=7)
    d.arc([fx - 60, fy - 100, fx + 80, fy + 10], 200, 340, fill=(220, 220, 200), width=8)
    kk = pop(min(1, max(0, t - 0.6) / 0.5))
    if kk > 0.05:
        rotulo(d, 300, 1160, "MENOS DE 1 CM", int(48 * kk) + 1, AMARELO)
        rotulo(d, 760, 1160, "FEIJÃO", int(48 * kk) + 1, (255, 255, 255))
        rotulo(d, 540, 590, "NA BARRIGA DA MÃE", int(46 * kk) + 1, CIANO)


def c_coccix(d, img, t, T):
    selo(d)
    # coluna: rabo encolhendo até virar o cóccix
    k = ease(t / 2.0)
    x = 380
    for i in range(9):
        y = 560 + i * 62
        d.rounded_rectangle([x - 70, y, x + 70, y + 48], radius=14, fill=OSSO, outline=O, width=5)
    # cóccix + rabo que some
    n = int(round(10 - 6 * k))
    for i in range(n):
        y = 1120 + i * 22
        xx = x + i * 26
        r = max(10, 34 - i * 3)
        fill = (255, 230, 120) if i < 4 else (255, 200, 200, 255 - int(200 * k))
        d.ellipse([xx - r, y - r * 0.6, xx + r, y + r * 0.6], fill=fill, outline=O, width=4)
    kk = pop(min(1, max(0, t - 1.0) / 0.5))
    if kk > 0.05:
        rotulo(d, 780, 1120, "CÓCCIX", int(60 * kk) + 1, AMARELO)
        seta(d, 680, 1130, 520, 1160, AMARELO, 12)
        rotulo(d, 780, 700, "8ª SEMANA", int(54 * kk) + 1, CIANO)
        rotulo(d, 780, 770, "O RABO SOME", int(42 * kk) + 1, (255, 255, 255))


def c_gene(d, img, t, T):
    selo(d)
    # fita de DNA girando com um pedaço "saltador" entrando
    for i in range(13):
        y = 570 + i * 42
        a = T * 2 + i * 0.5
        x1, x2 = 540 + math.cos(a) * 170, 540 - math.cos(a) * 170
        d.line([(x1, y), (x2, y)], fill=(150, 150, 190), width=6)
        d.ellipse([x1 - 14, y - 14, x1 + 14, y + 14], fill=(90, 200, 255), outline=O, width=3)
        d.ellipse([x2 - 14, y - 14, x2 + 14, y + 14], fill=(255, 120, 180), outline=O, width=3)
    k = ease(t / 1.2)
    jx = 960 - 420 * k
    jy = 860 - 120 * math.sin(k * math.pi)
    d.rounded_rectangle([jx - 70, jy - 34, jx + 70, jy + 34], radius=16, fill=AMARELO, outline=O, width=5)
    kk = pop(min(1, max(0, t - 1.2) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 1160, "GENE SALTADOR", int(42 * kk) + 1, AMARELO)
        rotulo(d, 540, 1230, "25 MILHÕES DE ANOS", int(48 * kk) + 1, CIANO)


def c_cta(d, img, t, T):
    g_rabo(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="TEVE RABO!", titulo_y=400, desenho=g_rabo, fundo=((70, 20, 50), (20, 5, 18)),
         fala="Você já teve rabo, com ossinhos! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="NA BARRIGA", desenho=c_feijao, fundo=((60, 25, 70), (15, 5, 25)),
         fala="Foi na barriga da sua mãe, quando você era menor que um feijão. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="SUMIU!", desenho=c_coccix, fundo=((20, 40, 80), (5, 10, 30)),
         fala="lá pela oitava semana ele some, e sobra o cóccix, o ossinho do fim da coluna."),
    dict(tipo="fato", titulo="O CULPADO", desenho=c_gene, fundo=((25, 25, 70), (5, 5, 20)),
         fala="Culpa de um gene saltador, que entrou no nosso DNA há 25 milhões de anos. Um erro de digitação!"),
    dict(tipo="cta", titulo="TEVE RABO!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((70, 20, 50), (20, 5, 18)),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. E lembra: você já teve..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "rabo_embriao.mp4"))
