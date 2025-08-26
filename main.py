import json
from browser import get_html_from_brave
from parser import parse_products, batch_price_fetch
from telegram import send_to_telegram

def load_sent_titles(path="sent_products.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_sent_titles(titles, path="sent_products.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)

def main():
    print("🔄 Amazon sayfalarından HTML çekiliyor...")
    html_list = get_html_from_brave()  # Artık birden fazla sayfa dönebilir

    all_products = []
    for index, html in enumerate(html_list):
        print(f"🔍 [{index}] Sayfa parse ediliyor...")
        products = parse_products(html)
        all_products.extend(products)

    print("💰 Fiyatlar kontrol ediliyor...")
    all_products = batch_price_fetch(all_products)

    sent_titles = load_sent_titles()
    new_products = [p for p in all_products if p["title"] not in sent_titles]

    if new_products:
        send_to_telegram(new_products)
        print(f"📨 {len(new_products)} yeni ürün Telegram'a gönderildi.")
        sent_titles.extend([p["title"] for p in new_products])
        save_sent_titles(sent_titles)
    else:
        print("🚫 Yeni ürün bulunamadı veya hepsi daha önce gönderilmiş.")

if __name__ == "__main__":
    main()
