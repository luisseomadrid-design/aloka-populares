import json
import requests

API_URL = "https://www.aloka.app/api/listings/query"

params = {
    "perPage": 10,
    "sort": "meta_lastMonthBookings",
    "include": "author,author.profileImage,images",
    "fields.listing": "title,geolocation,price,publicData.locationContext,publicData.listingType,publicData.transactionProcessAlias,publicData.unitType",
    "fields.image": "variants.landscape-crop,variants.square-small,variants.square-small2x",
    "limit.images": 1
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

productos = []

try:
    r = requests.get(API_URL, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()

    included = data.get("included", [])
    image_map = {}

    for item in included:
        if item.get("type") == "image":
            image_id = item.get("id")
            attrs = item.get("attributes", {})
            variants = attrs.get("variants", {})

            image_url = None
            if "landscape-crop" in variants:
                image_url = variants["landscape-crop"]["url"]
            elif "square-small2x" in variants:
                image_url = variants["square-small2x"]["url"]
            elif "square-small" in variants:
                image_url = variants["square-small"]["url"]

            if image_id and image_url:
                image_map[image_id] = image_url

    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        relationships = item.get("relationships", {})
        images_rel = relationships.get("images", {}).get("data", [])

        imagen = ""
        if images_rel:
            first_image_id = images_rel[0].get("id")
            imagen = image_map.get(first_image_id, "")

        productos.append({
            "nombre": attrs.get("title", "Sin nombre"),
            "imagen": imagen or "https://placehold.co/600x400/png?text=Sin+imagen"
        })

    with open("productos-populares.json", "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)

    print("productos-populares.json actualizado correctamente")

except Exception as e:
    print("Error actualizando productos:", e)
