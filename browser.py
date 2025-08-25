import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_cookies(driver, path="cookie.json"):
    full_path = os.path.join(os.getcwd(), path)
    if not os.path.exists(full_path):
        print(f"🍪 Cookie dosyası bulunamadı: {full_path}")
        return
    with open(full_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    for cookie in cookies:
        cookie.pop("sameSite", None)  # Selenium bazı versiyonlarda bunu kabul etmiyor
        driver.add_cookie(cookie)
    print("✅ Cookie'ler yüklendi.")

def save_cookies(driver, path="cookie.json"):
    full_path = os.path.join(os.getcwd(), path)
    cookies = driver.get_cookies()
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f)
    print("💾 Cookie'ler kaydedildi.")

def get_html_from_brave(
    url="https://www.amazon.com.tr/deals?ref_=nav_cs_gb",
    cookie_path="cookie.json",
    dump_path="amazon_brave_dump.html"
):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com.tr")
    time.sleep(2)

    load_cookies(driver, path=cookie_path)
    driver.refresh()
    time.sleep(2)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        ).click()
    except:
        print("ℹ️ Çerez onay butonu görünmedi veya tıklanamadı.")

    driver.execute_script("window.scrollTo(0, 300);")
    driver.execute_script("document.body.dispatchEvent(new Event('mousemove'));")
    time.sleep(1)

    driver.get(url)
    time.sleep(10)

    for i in range(0, 5000, 500):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
        )
    except:
        print("⚠️ Fiyat alanı DOM'da bulunamadı.")

    html = driver.page_source
    with open(dump_path, "w", encoding="utf-8") as f:
        f.write(html)

    save_cookies(driver, path=cookie_path)
    driver.quit()
    return html
