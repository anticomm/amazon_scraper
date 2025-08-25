import os
import requests
import re
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def escape_md(text):
    # MarkdownV2 için özel karakterleri kaçır
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + c if c in escape_chars else c for c in str(text)])

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
                "parse_mode": "MarkdownV2"
            }
            endpoint = f"{BASE_URL}/sendPhoto"
        else:
            # Görsel yoksa metin gönderimi
            payload = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "MarkdownV2"
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
    title = escape_md(product.get("title", "🛍️ Ürün adı bulunamadı"))

    raw_price = product.get("price", "Fiyat alınamadı")
    price = escape_md(raw_price)
    if "TL" not in raw_price and "₺" not in raw_price:
        price += "\\ TL"

    raw_link = product.get("link", "#")
    link_text = escape_md("🔥🔥 FIRSATA GİT 🔥🔥")
    # Link URL'si kaçırılmaz, sadece metin kısmı kaçırılır
    link_satiri = f"🔗 [{link_text}]({raw_link})" if raw_link.startswith("http") else "🔗 Link bulunamadı"

    discount = product.get("discount", "")
    rating = product.get("rating", "")
    colors = product.get("colors", [])
    specs = product.get("specs", [])

    indirimbilgi = f"%{escape_md(discount)}" if discount and discount.isdigit() else ""
    stars = f"⭐ {escape_md(rating)}" if rating else ""
    renkler = ", ".join([escape_md(c["color"]) for c in colors]) if colors else None
    teknik = "\n".join([f"▫️ {escape_md(spec)}" for spec in specs]) if specs else ""

    return (
        f"*{title}*\n"
        f"{indirimbilgi}  {stars}\n"
        f"{teknik}\n"
        f"{f'🎨 Renkler: {renkler}' if renkler else ''}\n"
        f"💰 *{price}*\n"
        f"{link_satiri}"
    )
