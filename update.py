import json

productos = [
    {
        "nombre": "DJI Ronin RS4 Pro",
        "imagen": "https://placehold.co/600x400/png?text=DJI+Ronin+RS4+Pro"
    },
    {
        "nombre": "Audio-Technica M40x",
        "imagen": "https://placehold.co/600x400/png?text=Audio-Technica+M40x"
    },
    {
        "nombre": "Tascam Portacapture X8",
        "imagen": "https://placehold.co/600x400/png?text=Tascam+Portacapture+X8"
    },
    {
        "nombre": "Kit 8x Helios Asteras",
        "imagen": "https://placehold.co/600x400/png?text=Kit+8x+Helios+Asteras"
    }
]

with open("productos-populares.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, ensure_ascii=False, indent=2)
