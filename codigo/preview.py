"""python3 preview.py modulo saida.jpg  -> folha com 1 quadro por cena"""
import sys, importlib, motor
from PIL import Image
v = importlib.import_module(sys.argv[1]); C = v.CENAS; tot = 0
voz = motor.escolher_voz(C); print('voz:', voz)
for c in C:
    pcm, pal = motor.tts(c['fala'], voz); c['_pcm'], c['_pal'] = pcm, pal
    c['_dur'] = len(pcm) / motor.SR + c.get('pausa', 0.45); c['_ini'] = tot; tot += c['_dur']
print('total', round(tot, 1), [round(c['_dur'], 1) for c in C])
ims = []
for c in C[:8]:
    t = min(3.4, c['_dur'] - 0.5); ims.append(motor.frame(c, t, c['_ini'] + t, 0.5, tot).resize((270, 480)))
s = Image.new('RGB', (1080, 960)); [s.paste(im, ((i % 4) * 270, (i // 4) * 480)) for i, im in enumerate(ims)]; s.save(sys.argv[2])
