from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import json

def load_cookies(driver, path="cookie.json"):
    if not os.path.exists(path):
        print("🚫 Cookie dosyası bulunamadı.")
        return

    with open(path, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for cookie in cookies:
        driver.add_cookie(cookie)
    print("✅ Cookie'ler yüklendi.")

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
    time.sleep(5)

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

    html = driver.page_source

    # Dump al
    with open("amazon_brave_dump.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("📄 Dump alındı: amazon_brave_dump.html")

    driver.quit()
    return html
