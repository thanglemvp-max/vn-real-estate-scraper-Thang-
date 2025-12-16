from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def parse_detail_page(html_content, url):
    ser = Service(executable_path="geckodriver.exe")

    # Firefox Configuration
    options = webdriver.firefox.options.Options()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    options.headless = False

    driver = webdriver.Firefox(
        service=ser,
        options=options
    )
    driver.get(url)

    # JS render
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    # Parse BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    # Extract information
    # POST ID
    post_id = re.search(r"pr\d+", url)
    post_id = post_id.group() if post_id else "NaN"

    # TITLE
    title = soup.find("h1")
    title = title.get_text(strip=True) if title else "NaN"

    # ADDRESS
    address = soup.select_one("span.re__pr-short-description")
    address = address.get_text(strip=True) if address else "NaN"

    # DESCRIPTION
    description = soup.select_one(".re__pr-description")
    description = description.get_text(strip=True) if description else "N/A"

    # OTHER FEATURES
    specs = {}
    for item in soup.select(".re__pr-specs-content-item"):
        label = item.select_one(".re__pr-specs-content-item-title")
        value = item.select_one(".re__pr-specs-content-item-value")
        if label and value:
            specs[label.get_text(strip=True)] = value.get_text(strip=True)

    price = specs.get("Mức giá", "NaN")
    area = specs.get("Diện tích", "NaN")
    bedroom = specs.get("Số phòng ngủ", "NaN")
    bathroom = specs.get("Số phòng tắm, vệ sinh", "NaN")
    num_floor = specs.get("Số tầng", "NaN")
    house_orientation = specs.get("Hướng nhà, vệ sinh", "NaN")
    balcony_direction = specs.get("Hướng ban công, vệ sinh", "NaN")
    front = specs.get("Mặt tiền, vệ sinh", "NaN")
    entrance = specs.get("Đường vào", "NaN")
    legal = specs.get("Pháp lý, vệ sinh", "NaN")
    furniture = specs.get("Nội thất", "NaN")

    driver.quit()
    data = {
        "post_id": post_id,
        "title": title,
        "address": address,
        "price": price,
        "area": area,
        "bedroom": bedroom,
        "bathroom": bathroom,
        "num_floor": num_floor,
        "house_orientation": house_orientation,
        "balcony_direction": balcony_direction,
        "front": front,
        "entrance": entrance,
        "legal": legal,
        "furniture": furniture,
        "description": description
    }

    return data

if __name__ == '__main__':
    bds = parse_detail_page(html_content="", url='https://batdongsan.com.vn/ban-can-ho-chung-cu-xa-long-hung-prj-vinhomes-ocean-park-2/dau-tu-tai-vin-2-gia-tu-59tr-m2-full-vat-pr44804495')
    print(bds)