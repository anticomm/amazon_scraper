import os
import requests
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_to_telegram(products):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram ayarları eksik, mesaj gönderilmeyecek.")
        return

    for product in products:
        message = format_product_message(product)
        image_url = product.get("image")

        if image_url and image_url.startswith("http"):
            # Görselli gönderim
            payload = {
                "chat_id": CHAT_ID,
                "photo": image_url,
                "caption": message,
                "parse_mode": "Markdown"
            }
            endpoint = f"{BASE_URL}/sendPhoto"
        else:
            # Görsel yoksa metin gönderimi
            payload = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            endpoint = f"{BASE_URL}/sendMessage"

        try:
            response = requests.post(endpoint, data=payload)
            if response.status_code == 200:
                print(f"✅ Gönderildi: {product.get('title', 'Ürün')}")
            else:
                print(f"❌ Gönderim hatası: {product.get('title', 'Ürün')} → {response.text}")
        except Exception as e:
            print(f"⚠️ İstek hatası: {e}")

def format_product_message(product):
    title = product.get("title", "🛍️ Ürün adı bulunamadı")
    price = product.get("price", "Fiyat alınamadı")
    link = product.get("link", "#")
    discount = product.get("discount", "")
    rating = product.get("rating", "")
    colors = product.get("colors", [])
    specs = product.get("specs", [])

    # Fiyat biçimlendirme
    if "TL" not in price and "₺" not in price:
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
