"""Câmera que filma a luz andando — femto-fotografia do MIT Media Lab (TECNOLOGIA INSANA #4).
Fatos (web.media.mit.edu/~raskar/trillionfps; MIT Media Lab, 2011–2012): cerca de meio trilhão de quadros
por segundo (exposição efetiva ~1,7 picossegundo); entre um quadro e outro o pulso de luz anda menos de
meio milímetro; a luz cruza uma garrafa de ~30 cm em cerca de 1 nanossegundo; o vídeo é montado com
pulsos de laser repetidos (média de muitos pulsos), não com um disparo só; a mesma técnica foi usada
para reconstruir objetos escondidos atrás de uma esquina ("looking around corners", MIT 2012)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, contador, O

SERIE = "TECNOLOGIA INSANA #4"
FUNDO1 = (15, 15, 45); FUNDO2 = (3, 3, 15)
LASER = (255, 60, 90); LUZ = (255, 240, 150)
CAM = (70, 75, 95); CAM2 = (45, 48, 62)
VIDRO = (150, 230, 160)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def camera(d, cx, cy, s=1.0, T=0.0):
    """Câmera científica: caixa com lente grande e luz vermelha piscando."""
    d.rounded_rectangle([cx - 150 * s, cy - 90 * s, cx + 110 * s, cy + 90 * s], radius=int(20 * s), fill=CAM, outline=O, width=7)
    d.rectangle([cx - 120 * s, cy - 120 * s, cx - 30 * s, cy - 90 * s], fill=CAM2, outline=O, width=5)
    d.rectangle([cx + 110 * s, cy - 60 * s, cx + 200 * s, cy + 60 * s], fill=CAM2, outline=O, width=6)
    d.ellipse([cx + 160 * s, cy - 75 * s, cx + 250 * s, cy + 75 * s], fill=(40, 80, 140), outline=O, width=7)
    d.ellipse([cx + 185 * s, cy - 40 * s, cx + 225 * s, cy + 0 * s], fill=(200, 230, 255))
    if (T * 2) % 1 < 0.5:
        d.ellipse([cx - 120 * s, cy - 60 * s, cx - 90 * s, cy - 30 * s], fill=(255, 50, 50), outline=O, width=3)
    for k in range(3):
        d.line([(cx - 130 * s, cy + (10 + k * 22) * s), (cx + 60 * s, cy + (10 + k * 22) * s)], fill=CAM2, width=max(3, int(6 * s)))


def garrafa(d, x0, cy, L=600, h=120):
    """Garrafa deitada (só contorno, vidro), gargalo à direita."""
    d.rounded_rectangle([x0, cy - h, x0 + L * 0.7, cy + h], radius=40, outline=VIDRO, width=8)
    d.polygon([(x0 + L * 0.7, cy - h), (x0 + L * 0.85, cy - h * 0.35), (x0 + L * 0.85, cy + h * 0.35), (x0 + L * 0.7, cy + h)],
              outline=VIDRO)
    d.line([(x0 + L * 0.7, cy - h), (x0 + L * 0.85, cy - h * 0.35)], fill=VIDRO, width=8)
    d.line([(x0 + L * 0.7, cy + h), (x0 + L * 0.85, cy + h * 0.35)], fill=VIDRO, width=8)
    d.rectangle([x0 + L * 0.85, cy - h * 0.35, x0 + L, cy + h * 0.35], outline=VIDRO, width=8)


def pulso(d, x, y, r=34):
    """'Bala' de luz: núcleo claro com halo."""
    for k, c in enumerate([(120, 40, 60), (220, 70, 90), LUZ]):
        rr = r * (1.8 - k * 0.5)
        d.ellipse([x - rr * 1.6, y - rr, x + rr * 1.6, y + rr], fill=c)


def g_camera(d, img, t, T, label=True):
    etiqueta(d)
    # garrafa com a bala de luz andando dentro; câmera filmando de baixo
    garrafa(d, 150, 700, 780, 120)
    u = ((T * 0.35) % 1)
    pulso(d, 190 + u * 700, 700)
    camera(d, 380, 1060, 0.9, T)
    # cone de visão da câmera
    d.line([(600, 1030), (900, 820)], fill=(255, 255, 255, 120), width=4)
    d.line([(600, 1030), (300, 820)], fill=(255, 255, 255, 120), width=4)
    if label:
        k = pop(min(1, max(0, t - 0.4) / 0.5))
        if k > 0.05:
            rotulo(d, 820, 1180, "REC", int(56 * k) + 1, (255, 70, 70))


def c_quadros(d, img, t, T):
    selo(d)
    # tira de filme com quadros passando, cada um com o pulso um pouquinho à frente
    off = (T * 220) % 230
    d.rectangle([0, 600, 1080, 960], fill=(25, 25, 30), outline=O, width=6)
    for i in range(7):
        x = -230 + i * 230 + off
        d.rectangle([x + 20, 640, x + 210, 920], fill=(10, 10, 40), outline=(200, 200, 200), width=4)
        pulso(d, x + 40 + (i * 23) % 150, 780, 18)
        for j in range(4):
            d.rectangle([x + 20 + j * 50, 612, x + 50 + j * 50, 628], fill=(200, 200, 200))
            d.rectangle([x + 20 + j * 50, 932, x + 50 + j * 50, 948], fill=(200, 200, 200))
    k = pop(min(1, max(0, t - 0.3) / 0.5))
    if k > 0.05:
        rotulo(d, 540, 1040, "QUADROS POR SEGUNDO", int(46 * k) + 1, CIANO)
        rotulo(d, 540, 1120, "500.000.000.000", int(58 * k) + 1, AMARELO, traduzir=False)


def c_garrafa(d, img, t, T):
    selo(d)
    garrafa(d, 120, 800, 840, 140)
    # rastro: o pulso avançando bem devagar (câmera lenta extrema)
    u = min(1, t / 3.5)
    x = 170 + u * 640
    for k in range(6):
        d.ellipse([x - 60 - k * 40, 785, x - 40 - k * 40, 815], fill=(255, 220, 140, 255 - k * 40))
    pulso(d, x, 800, 40)
    # régua: menos de meio milímetro por quadro
    kk = pop(min(1, max(0, t - 0.5) / 0.5))
    if kk > 0.05:
        rotulo(d, 540, 560, "MENOS DE 0,5 MM", int(48 * kk) + 1, AMARELO)
        rotulo(d, 540, 625, "POR QUADRO", int(40 * kk) + 1, (255, 255, 255))
        rotulo(d, 540, 1035, "1 NANOSSEGUNDO", int(48 * kk) + 1, CIANO)
        rotulo(d, 540, 1095, "PRA CRUZAR A GARRAFA", int(38 * kk) + 1, (255, 255, 255))


def c_esquina(d, img, t, T):
    selo(d)
    # parede em L: câmera de um lado, boneco escondido do outro, luz ricocheteando
    d.rectangle([520, 560, 600, 1180], fill=(120, 110, 140), outline=O, width=6)
    d.rectangle([0, 1180, 1080, 1260], fill=(90, 85, 110), outline=O, width=6)
    camera(d, 230, 1000, 0.7, T)
    # boneco escondido
    bx, by = 860, 1000
    d.ellipse([bx - 45, by - 210, bx + 45, by - 120], fill=(255, 210, 120), outline=O, width=6)
    d.line([(bx, by - 120), (bx, by + 40)], fill=O, width=16)
    d.line([(bx - 70, by - 60), (bx + 70, by - 60)], fill=O, width=14)
    d.line([(bx, by + 40), (bx - 50, by + 160)], fill=O, width=14)
    d.line([(bx, by + 40), (bx + 50, by + 160)], fill=O, width=14)
    # ricochete: câmera -> teto/parede de trás -> boneco
    k = ease(t / 1.4)
    p0, p1, p2 = (380, 990), (560, 620), (860, 820)
    if k < 0.5:
        q = k / 0.5
        d.line([p0, (p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q)], fill=LASER, width=10)
    else:
        q = (k - 0.5) / 0.5
        d.line([p0, p1], fill=LASER, width=10)
        d.line([p1, (p1[0] + (p2[0] - p1[0]) * q, p1[1] + (p2[1] - p1[1]) * q)], fill=LASER, width=10)
    kk = pop(min(1, max(0, t - 1.4) / 0.5))
    if kk > 0.05:
        rotulo(d, 860, 640, "ESCONDIDO!", int(46 * kk) + 1, AMARELO)
        brilhos(d, 860, 880, 120, T, 8, LUZ)


def c_cta(d, img, t, T):
    g_camera(d, img, t, T, label=False)


CENAS = [
    dict(tipo="gancho", titulo="FILMA A LUZ", titulo_y=400, desenho=g_camera, fundo=(FUNDO1, FUNDO2),
         fala="Essa câmera filma a luz andando! E o último fato parece mágica."),
    dict(tipo="fato", titulo="MIT, EUA", desenho=c_quadros, fundo=((40, 20, 60), (10, 5, 20)),
         fala="No MIT, ela grava meio trilhão de quadros por segundo. Segue a Maia, que tem mais:"),
    dict(tipo="fato", titulo="CÂMERA LENTA", desenho=c_garrafa, fundo=((10, 40, 50), (3, 12, 18)),
         fala="de um quadro pro outro, a luz anda menos de meio milímetro dentro da garrafa!"),
    dict(tipo="fato", titulo="VÊ ATRÁS", desenho=c_esquina, fundo=((50, 20, 30), (15, 5, 10)),
         fala="E com os ecos da luz, eles viram um objeto escondido atrás da parede. Visão de super-herói!"),
    dict(tipo="cta", titulo="FILMA A LUZ", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=(FUNDO1, FUNDO2),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana. E tudo começa com essa câmera..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "camera_luz.mp4"))
