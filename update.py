import json
from datetime import datetime

productos = [
    {
        "nombre": "Prueba automática " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "imagen": "https://sharetribe.imgix.net/6644cdce-c443-44fc-a95e-d3abbca7a3b9/68f23a86-a2b8-41da-883d-5c0d47271c3a?auto=format&fit=clip&h=750&w=750&s=f9d52c3fd455c1871c79dd1f38892043"
    }
]

with open("productos-populares.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, ensure_ascii=False, indent=2)

print("productos-populares.json actualizado correctamente")
