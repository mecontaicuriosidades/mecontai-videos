"""Capa 1280x720 do vídeo longo Bichos Insanos. Uso: python3 capa_longo_bichos_insanos.py capa.jpg"""
import sys
from PIL import Image, ImageDraw
import motor_longo as ML
from motor_longo import fnt, AMARELO, ESCURO, CIANO
from maia import maia_pose
import video_tardigrado as ta, video_camarao_pistola as cp
img = ML.degrade((30, 20, 90), (5, 5, 25))
d = ImageDraw.Draw(img, "RGBA"); ML.estrelas(d, 1.0)
for fn, caixa, cor in ((cp.g_tiro, (1000, 80, 1880, 1000), ((20, 90, 130), (5, 30, 60))),):
    ML.painel_vertical(img, dict(vert=fn, fundo=cor), 2.5, 2.5, caixa=caixa)
d = ImageDraw.Draw(img, "RGBA")
d.text((80, 300), "10 BICHOS", font=fnt(190), fill=(255, 255, 255), anchor="lm", stroke_width=14, stroke_fill=ESCURO)
d.text((80, 520), "INSANOS", font=fnt(220), fill=AMARELO, anchor="lm", stroke_width=16, stroke_fill=ESCURO)
d.rounded_rectangle([80, 680, 760, 790], 30, fill=(230, 40, 60), outline=ESCURO, width=6)
d.text((420, 735), "O #1 SOBREVIVEU AO ESPAÇO", font=fnt(40), fill="white", anchor="mm")
m = maia_pose(1.2, 0.6, escala=0.5)
img.alpha_composite(m, (760, 1080 - m.height + 30))
img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(sys.argv[1], quality=90)
