from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
import base64

def load_cookies(driver):
    encoded = os.getenv("COOKIE_BASE64")
    if not encoded:
        print("🚫 COOKIE_BASE64 Secret bulunamadı.")
        return

    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        cookies = json.loads(decoded)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("✅ Cookie'ler Secret üzerinden yüklendi.")
    except Exception as e:
        print("⚠️ Cookie yükleme hatası:", e)

def get_html_from_brave():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://www.amazon.com.tr/deals?ref_=nav_cs_gb"

    print(f"🌐 Sayfa açılıyor: {url}")
    driver.get("https://www.amazon.com.tr")  # Cookie'yi önce ana domaine yükle
    time.sleep(2)

    load_cookies(driver)

    driver.get(url)
    try:
        # Çerez onay butonu varsa tıkla
        consent = driver.find_elements(By.ID, "sp-cc-accept")
        if consent:
            consent[0].click()
            print("✅ Çerez onayı verildi.")
        else:
            print("ℹ️ Çerez onay butonu görünmedi veya tıklanamadı.")
    except Exception as e:
        print("⚠️ Çerez onayı sırasında hata:", e)

    try:
        # Fiyat alanı DOM'a girene kadar bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price"))
        )
        print("✅ Fiyat alanı DOM'da bulundu.")
    except Exception:
        print("⚠️ Fiyat alanı DOM'da bulunamadı.")

    html = driver.page_source

    # Dump al
    with open("amazon_brave_dump.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("📄 Dump alındı: amazon_brave_dump.html")

    driver.quit()
    return html
