from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def crawl_data(url_real_estate):
    gecko_path = "geckodriver.exe"
    
    # Cấu hình Firefox
    options = webdriver.firefox.options.Options()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    options.headless = False

    driver = webdriver.Firefox(
        service=Service(gecko_path),
        options=chrome_options
    )
    url = url_real_estate
    driver.get(url)

    # Đợi JS render xong
    time.sleep(5)

    # Lấy HTML sau khi JS load
    html = driver.page_source

    # Parse bằng BeautifulSoup
    soup = BeautifulSoup(html, "lxml")

    # Trích xuất thông tin

    # post_id

    # Tiêu đề
    title = soup.find("h1")
    print("Tiêu đề:", title.get_text(strip=True) if title else "N/A")

    # Địa chỉ
    address = soup.select_one("span.re__pr-short-description")
    print("Địa chỉ:", address.get_text(strip=True) if address else "N/A")

    # Giá
    price = soup.select_one(".re__pr-specs-content-item-value")
    print("Giá:", price.get_text(strip=True) if price else "N/A")

    # Diện tích
    specs = soup.select(".re__pr-specs-content-item-value")
    area = specs[1].get_text(strip=True) if len(specs) > 1 else "N/A"
    print("Diện tích:", area)

    # Phòng ngủ
    specs = soup.select(".re__pr-specs-content-item-value")
    bedroom = specs[2].get_text(strip=True) if len(specs) > 1 else "N/A"
    print("Phòng ngủ:", bedroom)

    # Mô tả
    description = soup.select_one(".re__pr-description")
    print("Mô tả:", description.get_text(strip=True) if description else "N/A")

    driver.quit()

if __name__ == '__main__':
    crawl_data('https://batdongsan.com.vn/ban-can-ho-chung-cu-xa-long-hung-prj-vinhomes-ocean-park-2/dau-tu-tai-vin-2-gia-tu-59tr-m2-full-vat-pr44804495')