from bs4 import BeautifulSoup
import re
import unidecode
from urllib.parse import urlparse
from datetime import datetime

def extract_from_js_config(html_content):
    """
    Uses flexible Regex to extract key numerical values coordinates
    from a hidden JavaScript configuration block in the static HTML
    """
    js_data = {}

    # extract a specific field
    def search_key(key, content):
        # Pattern: ["']?key["']?: value
        pattern = rf'["\']?{re.escape(key)}["\']?\s*:\s*([\d\.]+)'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return None

    # 1. Latitude
    lat_str = search_key('latitude', html_content)
    if lat_str:
        try:
            js_data['latitude'] = float(lat_str)
        except ValueError:
            pass

    # 2. Longitude
    lon_str = search_key('longitude', html_content)
    if lon_str:
        try:
            js_data['longitude'] = float(lon_str)
        except ValueError:
            pass

    return js_data

def classify_property(url):
    """ Classify the property type based on the URL path segment """
    mapping = {
        "ban-can-ho-chung-cu": "Apartment",
        "ban-can-ho-chung-cu-mini": "Apartment",
        "ban-nha-rieng": "House",
        "ban-nha-biet-thu-lien-ke": "House",
        "ban-nha-mat-pho": "House",
        "ban-shophouse-nha-pho-thuong-mai": "House",
        "ban-dat-nen-du-an": "Land",
        "ban-dat": "Land",
        "ban-trang-trai-khu-nghi-duong": "Resort/Investment",
        "ban-condotel": "Resort/Investment",
        "ban-kho-nha-xuong": "Warehouse/Factory"
    }

    path = urlparse(url).path
    path = path.strip('/').lower()
    for detailed_type, main_group in mapping.items():
        if path.startswith(detailed_type):
            if len(path) == len(detailed_type) or path[len(detailed_type)] == '-':
                return main_group
    return "Unknown"

def normalize_key(key):
    """ Lowercase, remove accents, replace spaces with underscores """
    key = unidecode.unidecode(key)
    key = key.lower().replace(" ", "_")
    return key

def extract_post_id(url):
    """ Extract the numerical post ID from the URL (pr____) """
    match = re.search(r"pr(\d+)$", url)
    return match.group(1) if match else None

def parse_detail_page(html_content, url):
    """ Extract all structured and unstructured data  from the detailed listing HTML."""
    soup = BeautifulSoup(html_content, "lxml")

    # Extract text or attribute value using a CSS selector
    def get_info(selector, attr=None, default=None):
        tag = soup.select_one(selector)
        if tag:
            return tag.get(attr, default) if attr else tag.get_text(strip=True)
        return default

    # COORDINATE
    latitude = None
    longitude = None
    js_config_data = extract_from_js_config(html_content)

    latitude = js_config_data.get('latitude')
    longitude = js_config_data.get('longitude')

    # HTML PARSING
    type_property = classify_property(url)
    post_id = extract_post_id(url)
    title = get_info("h1")
    address = get_info("span.re__pr-short-description")
    price_per_spm = get_info("span.ext")

    # PROPERTY CHARACTERISTICS
    specs = {}
    for item in soup.select(".re__pr-specs-content-item"):
        label_tag = item.select_one(".re__pr-specs-content-item-title")
        value_tag = item.select_one(".re__pr-specs-content-item-value")
        if label_tag and value_tag:
            key = normalize_key(label_tag.get_text(strip=True))
            value = value_tag.get_text(strip=True)
            specs[key] = value

    # SUB-INFO
    sub_info = {}
    for item in soup.select("div.re__pr-short-info-item"):
        title_tag = item.select_one("span.title")
        value_tag = item.select_one("span.value")
        if title_tag and value_tag:
            key = normalize_key(title_tag.get_text(strip=True))
            value = value_tag.get_text(strip=True)
            sub_info[key] = value

    # DESCRIPTION
    description_tag = soup.select_one(".re__pr-description")
    description = None
    if description_tag:
        description = description_tag.get_text(strip=True)
        if description.startswith("Thông tin mô tả"):
            description = description.replace("Thông tin mô tả", "", 1).strip()

    # IMAGES
    images = [
        (item.find("img").get("data-src") or item.find("img").get("src"))
        for item in soup.select("div.re__media-thumb-item.js__media-thumbs-item")
        if item.find("img")  # Ensure img tag exists
    ]

    # DATA STRUCTURE
    data = {
        "post_id": post_id,
        "property_url": url,
        "type_property": type_property,
        "title": title,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "price": specs.get("khoang_gia"),
        "price_per_spm": price_per_spm,
        "spec": {
            "area": specs.get("dien_tich"),
            "bedroom": specs.get("so_phong_ngu"),
            "bathroom": specs.get("so_phong_tam,_ve_sinh"),
            "num_floor": specs.get("so_tang"),
            "orientation": specs.get("huong_nha"),
            "balcony_direction": specs.get("huong_ban_cong"),
            "front_width": specs.get("mat_tien"),
            "road_width": specs.get("duong_vao"),
            "legal": specs.get("phap_ly"),
            "furniture": specs.get("noi_that")
        },
        "description": description,
        "images": images if images else None,
        "date_posted": sub_info.get("ngay_dang"),
        "expire_posted": sub_info.get("ngay_het_han"),
        "type_news": sub_info.get("loai_tin"),
        "scraped_at": datetime.now().isoformat()
    }

    # Remove keys with None values
    data = {k: v for k, v in data.items() if v is not None}
    if 'spec' in data:
        data['spec'] = {k: v for k, v in data['spec'].items() if v is not None}
        if not data['spec']: del data['spec']

    return data

if __name__ == "__main__":
    post_id = extract_post_id("https://batdongsan.com.vn/ban-dat-duong-vo-van-thu-xa-hung-long-5/sieu-vip-binh-chanh-2-5tr-m2-pr44810318")
    print(post_id)
