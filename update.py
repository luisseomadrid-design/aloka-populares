import json
import random

with open("productos-base.json", "r", encoding="utf-8") as f:
    base = json.load(f)

cantidad = min(8, len(base))
seleccionados = random.sample(base, cantidad)

with open("productos-populares.json", "w", encoding="utf-8") as f:
    json.dump(seleccionados, f, ensure_ascii=False, indent=2)

print(f"productos-populares.json actualizado con {cantidad} productos")
