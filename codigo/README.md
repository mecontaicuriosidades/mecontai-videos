# Motor de vídeos Me ContAI

- `motor.py`: render (narração ElevenLabs com timestamps, boca da MAIA pelo volume, legendas palavra a palavra, trilha).
- `maia.py`: a apresentadora MAIA desenhada em código.
- `desenhos.py`: elementos reutilizáveis (sol, planetas, termômetro, contador...).
- `preview.py`: `python3 preview.py video_x folha.jpg` gera uma folha com 1 quadro por cena.
- `exemplos/`: vídeos já produzidos (copie um para a raiz e adapte).

A chave da ElevenLabs fica em `~/.secrets/elevenlabs` (nunca no repositório).
Os exemplos importam `video_polvo` (função `polvo`), por isso ele também está na raiz.

## Outros idiomas (desde 12/11/2026)
- `idioma.py`: configuração de cada idioma (voz, nome no selo, formato de números, fuso). Em português nada muda.
- `traducoes/<tema>.json`: tabela "texto em português" → tradução, por idioma.
- `traduzir.py`: `python3 traduzir.py video_venus es --listar` (o que falta traduzir), `--preview folha.jpg`, ou `out/venus_es.mp4` para renderizar.
