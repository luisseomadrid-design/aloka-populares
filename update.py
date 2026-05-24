# update.py (versión de prueba)
import json
import requests
from pathlib import Path

# ENDPOINT de prueba que vimos en el bundle: integración sharetribe
# NOTA: si tu marketplace expone /integration_api/listings/query úsalo aquí.
# Si tu backend usa otro prefijo, ajusta la URL.
INTEGRATION_URL = "https://flex-api.sharetribe.com/v1/listings/query"  # ejemplo genérico

# Parámetros que queremos (mismo criterio que vimos: ordenar por meta_lastMonthBookings)
params = {
    "perPage": 10,
    "sort": "meta_lastMonthBookings",
    "include": "images,author,author.profileImage",
    # campos de ejemplo; el SDK serializa algunos parámetros en objetos, aquí usamos strings simples
    "fields.listing": "title,publicData,price",
    "fields.image": "variants.landscape-crop,variants.square-small,variants.square-small2x",
    "limit.images": 1,
    "page": 1
}

headers = {
    "User-Agent": "Mozilla/5.0 (update-script)",
    "Accept": "application/json"
}

out_raw = Path("last-response-raw.json")
out_products = Path("productos-populares.json")

def main():
    try:
        print("Llamando a", INTEGRATION_URL)
        resp = requests.get(INTEGRATION_URL, params=params, headers=headers, timeout=30)
        print("Status:", resp.status_code)
        text = resp.text

        # Guardamos la respuesta cruda para inspección
        out_raw.write_text(text, encoding="utf-8")
        print(f"Respuesta cruda guardada en {out_raw}")

        # Intentamos parsear JSON y extraer campos si la respuesta es JSON
        try:
            data = resp.json()
        except Exception as e:
            print("No es JSON válido o la API devolvió HTML (posible endpoint incorrecto o bloqueo).")
            print("Error parse JSON:", e)
            return

        # Si llegamos aquí, data es un dict. Guardamos un extracto simplificado
        productos = []
        for item in data.get("data", []):
            attrs = item.get("attributes", {})
            title = attrs.get("title") or attrs.get("name") or "Sin nombre"
            # intentamos localizar la imagen por relaciones + included si existe
            imagen = ""
            relationships = item.get("relationships", {})
            images_rel = relationships.get("images", {}).get("data", [])
            included = data.get("included", [])
            image_map = {}
            for inc in included:
                if inc.get("type") == "image":
                    iid = inc.get("id")
                    attrs_inc = inc.get("attributes", {})
                    variants = attrs_inc.get("variants", {}) or {}
                    # Prioridad similar a lo que usamos antes
                    url = None
                    if "landscape-crop" in variants:
                        url = variants["landscape-crop"].get("url")
                    elif "square-small2x" in variants:
                        url = variants["square-small2x"].get("url")
                    elif "square-small" in variants:
                        url = variants["square-small"].get("url")
                    if iid and url:
                        image_map[iid] = url

            if images_rel:
                first_image_id = images_rel[0].get("id")
                imagen = image_map.get(first_image_id, "")

            productos.append({
                "nombre": title,
                "imagen": imagen or "https://placehold.co/600x400/png?text=Sin+imagen"
            })

        # Guardamos resultado simplificado (aunque puede estar vacío si la API no devolvió datos)
        out_products.write_text(json.dumps(productos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"productos-populares.json actualizado con {len(productos)} items")

    except Exception as e:
        print("Error general en el script:", e)

if __name__ == "__main__":
    main()
