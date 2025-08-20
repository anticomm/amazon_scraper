def get_html_from_brave():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com.tr/deals?ref_=nav_cs_gb")

    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        )
        cookie_button.click()
    except:
        pass

    time.sleep(3)

    for i in range(0, 5000, 500):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
        )
    except:
        print("Fiyat alanı DOM'da bulunamadı.")

    html = driver.page_source
    driver.quit()

    with open("amazon_brave_dump.html", "w", encoding="utf-8") as f:
        f.write(html)

    return html


def get_price_from_product_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 ...")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    try:
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#priceblock_dealprice, #priceblock_ourprice"))
        )
        result = price.text.strip()
    except:
        result = None

    driver.quit()
    return result
