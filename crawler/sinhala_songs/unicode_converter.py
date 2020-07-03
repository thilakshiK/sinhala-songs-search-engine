import json

with open('./bla.json') as fp:
    data = json.load(fp)

with open('./sinhala_lyrics_bla.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent =2)
