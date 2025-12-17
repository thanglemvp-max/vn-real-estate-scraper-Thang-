from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from parser import parse_detail_page, extract_post_id
from data_cleaner import clean_property_data
from duplicate_filter import is_duplicate, mark_as_scraped

def setup_driver(
        geckodriver_path="geckodriver.exe",
        firefox_binary="C:/Program Files/Mozilla Firefox/firefox.exe",
        headless=False
):
    service = Service(executable_path=geckodriver_path)
    options = Options()
    options.binary_location = firefox_binary
    options.headless = headless
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_rendered_html(url, wait_tag="h1", timeout=15):
    driver = setup_driver()
    driver.get(url)

    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, wait_tag))
        )
        scroll_to_bottom(driver)
        time.sleep(2)  # đợi AJAX load xong
        html = driver.page_source
    finally:
        driver.quit()

    return html


if __name__ == "__main__":
    urls = [
        "https://batdongsan.com.vn/ban-nha-mat-pho-duong-tran-thanh-mai-phuong-tan-tao/ban-9-ty-204-m2-binh-hcm-pr44814688",
        "https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-xa-lo-ha-noi-phuong-thao-dien-prj-masteri-thao-dien/ban-2pn-thap-t5-du-an-tro-vay-80-lh-mr-ai-pr44175404",
        "https://batdongsan.com.vn/ban-dat-duong-vo-van-thu-xa-hung-long-5/sieu-vip-binh-chanh-2-5tr-m2-pr44810318"
    ]

    results = []

    for url in urls:
        # 1. Extract ID quickly from URL to check for duplicates first
        post_id = extract_post_id(url)

        if is_duplicate(post_id):
            print(f"Skipping: {post_id} already exists.")
            continue

        print(f"Processing: {post_id}...")

        # 2. Get HTML (Assuming your get_rendered_html is defined)
        html = get_rendered_html(url)

        # 3. Parse raw data
        raw_data = parse_detail_page(html, url)

        # 4. Clean data using our new cleaner
        # final_data = clean_property_data(raw_data)

        # 5. Add to session list and mark ID as scraped
        results.append(raw_data)
        mark_as_scraped(post_id)

    # 6. Save to JSON file
    if results:
        with open("batdongsan_detail.json", "a", encoding="utf-8") as f:
            for data in results:
                json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Successfully exported {len(results)} new records.")
