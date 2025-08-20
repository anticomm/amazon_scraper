import requests

def format_product_message(product):
    title = product.get("title", "🛍️ Ürün adı bulunamadı")
    price = product.get("price", "Fiyat alınamadı")
    link = product.get("link", "#")
    discount = product.get("discount", "")
    rating = product.get("rating", "")
    colors = product.get("colors", [])
    specs = product.get("specs", [])

    # Fiyat biçimlendirme
    if "TL" not in price:
        price = f"{price} TL"

    # İndirim ve puan
    indirimbilgi = f"%{discount}" if discount and discount.isdigit() else ""
    stars = f"⭐ {rating}" if rating else ""

    # Renkler
    renkler = ", ".join([c["color"] for c in colors]) if colors else None

    # Teknik özellikler
    teknik = "\n".join([f"▫️ {spec}" for spec in specs]) if specs else ""

    return (
        f"*{title}*\n"
        f"{indirimbilgi}  {stars}\n"
        f"{teknik}\n"
        f"{f'🎨 Renkler: {renkler}' if renkler else ''}\n"
        f"💰 *{price}*\n"
        f"🔗 [🔥🔥 FIRSATA GİT 🔥🔥]({link})"
    )




def send_to_telegram(products):
    token = ""  # ← Buraya kendi bot token'ını yaz
    chat_id = ""  # ← Buraya kendi chat ID'ni yaz
    base_url = f"https://api.telegram.org/bot{token}"

    for product in products:
        message = format_product_message(product)
        image_url = product.get("image")

        if image_url and image_url.startswith("http"):
            # Görselli gönderim
            payload = {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"{base_url}/sendPhoto", data=payload)
        else:
            # Görsel yoksa metin gönderimi
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"{base_url}/sendMessage", data=payload)

        if response.status_code == 200:
            print(f"✅ Gönderildi: {product.get('title', 'Ürün')}")
        else:
            print(f"❌ Gönderim hatası: {product.get('title', 'Ürün')} → {response.text}")
