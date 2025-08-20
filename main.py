import json
from browser import get_html_from_brave
from fetcher import batch_price_fetch

from parser import parse_products
from telegram import send_to_telegram

# Daha önce gönderilen ürünleri yükle
try:
    with open("sent_products.json", "r", encoding="utf-8") as f:
        sent_titles = json.load(f)
except FileNotFoundError:
    sent_titles = []

# HTML çekimi ve ürün parse
html = get_html_from_brave()
products = parse_products(html)
products = batch_price_fetch(products)

# Yeni ürünleri filtrele
new_products = [p for p in products if p["title"] not in sent_titles]

if new_products:
    send_to_telegram(new_products)
    print(f"📨 {len(new_products)} yeni ürün Telegram'a gönderildi.")

    # Gönderilenleri kaydet
    sent_titles.extend([p["title"] for p in new_products])
    with open("sent_products.json", "w", encoding="utf-8") as f:
        json.dump(sent_titles, f, ensure_ascii=False, indent=2)
else:
    print("🚫 Yeni ürün bulunamadı veya hepsi daha önce gönderilmiş.")
