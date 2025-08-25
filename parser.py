from bs4 import BeautifulSoup

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for card in soup.select('div[data-asin][data-deal-id]'):
        asin = card['data-asin']

        # Başlık
        title_tag = card.select_one('.a-truncate-full')
        title = title_tag.text.strip() if title_tag else None

        # Fiyat
        price = extract_price(card)

        # Rozet
        badge_tag = card.select_one('div[data-component="dui-badge"] .a-size-mini')
        badge = badge_tag.text.strip() if badge_tag else None

        # Link
        link = extract_product_link(card)

        # Görsel
        image_tag = card.select_one('img')
        image = image_tag['src'] if image_tag else None

        # Renkler
        colors = []
        for swatch in card.select('li a[aria-label]'):
            colors.append({
                'color': swatch['aria-label'],
                'href': swatch['href']
            })

        # Ürün geçerli mi?
        if title and price and link:
            products.append({
                "asin": asin,
                "title": title,
                "price": price,
                "badge": badge,
                "link": link,
                "image": image,
                "colors": colors
            })

    return products

def extract_price(card):
    try:
        # En güvenilir kaynak: .a-offscreen
        offscreen = card.select_one(".a-offscreen")
        if offscreen:
            text = offscreen.text.strip()
            if any(c.isdigit() for c in text) and ("TL" in text or "₺" in text):
                return text.replace(",", ".").replace("TL", "₺").strip()

        # Alternatif: .a-price-whole + .a-price-fraction
        price_whole = card.select_one(".a-price-whole")
        price_fraction = card.select_one(".a-price-fraction")
        if price_whole:
            return f"{price_whole.text.strip()},{price_fraction.text.strip() if price_fraction else '00'} ₺"

    except Exception as e:
        print("Fiyat parse hatası:", e)

    return "Fiyat bulunamadı"

def extract_product_link(card):
    link_tag = card.select_one("a[href]")
    if link_tag:
        href = link_tag['href']
        return href if href.startswith("http") else "https://www.amazon.com.tr" + href
    return None

def batch_price_fetch(products):
    for product in products:
        price = product.get("price", "")
        if not price or "bulunamadı" in price.lower() or "güncellenemedi" in price.lower():
            product["price"] = "Fiyat güncellenemedi"
    return products
