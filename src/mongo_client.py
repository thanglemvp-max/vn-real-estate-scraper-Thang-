from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["property"]
collection = db["posts"]

def save_to_mongo(data: dict):
    if not data:
        return

    post_id = data.get("post_id")
    if post_id and collection.find_one({"post_id": post_id}):
        print("Duplicate post_id:", post_id)
        return

    collection.insert_one(data)
    print("Saved post_id:", post_id)

if __name__ == "__main__":
    save_to_mongo({
        "post_id": "38619623",
        "property_url": "https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-phung-hung-1-phuong-phuc-la-prj-khu-do-thi-moi-xa-la/em-ha-mua-ban-nhieu-tai-kdt-ha-dong-ha-noi-tline-pr38619623",
        "type_property": "Apartment",
        "title": "EM HÀ PHƯƠNG BÁN HÀNG TRĂM CĂN HỘ CHUNG CƯ XA LA HÀ ĐÔNG. LH0986 186 ***",
        "address": {
            "province": "Hà Nội",
            "district": "Hà Đông",
            "ward": "Phường Phúc La",
            "street": "Phố Phùng Hưng"
        },
        "latitude": 20.962404629474776,
        "longitude": 105.79233933526207,
        "price": 4160000000,
        "price_per_spm": 65.0,
        "area": 64,
        "spec": {
            "bedroom": 2,
            "bathroom": 2,
            "orientation": "Tây - Bắc",
            "balcony_direction": "Đông - Nam",
            "legal": "Sổ đỏ/ Sổ hồng",
            "furniture": "Đầy đủ"
        },
        "description": "Em Hà Phương xin giới thiệu tới anh chị quỹ căn chung cư Xa La đang mở bán.+ Căn 1PN 1WC tầng trung tòa TTTM Đức Thành, 56m², nội thất cơ bản, SĐCC. Giá 3.6 tỷ.+ Căn 2PN 2WC tầng trung tòa CT5, 75m², nội thất cơ bản, SĐCC. Giá 4.3x tỷ.+ Căn 2PN 2WC tầng trung tòa CT5, 73m², nội thất cơ bản, SĐCC. Giá 4.5x tỷ.+ Căn 2PN 2WC tầng trung tòa BMM, 75m², nội thất cơ bản, SĐCC. Giá 4.5x tỷ.+ Căn 3PN 2WC tầng trung tòa CT4, 63m², full nội thất mới tinh, SĐCC. Giá 4.6x tỷ.+ Căn 2PN 2WC tầng cao tòa CT5, 77m², full nội thất, SĐCC. Giá 4.5x tỷ.+ Căn 3PN 2WC tầng trung tòa CT1, 100m², nội thất cơ bản, SĐCC. Giá 6,xxx tỷ.+ Căn 2PN 2WC tầng trung tòa CT2, 64m², nội thất cơ bản, SĐCC. Giá 4.8x tỷ.+ Căn 2PN 2WC tầng trung tòa CT4, 70m², full nội thất mới tinh, SĐCC. Giá 4.6x tỷ.+ Căn góc 2PN 2WC tầng trung tòa CT4, 70m², nội thất cơ bản, SĐCC, ban công Đông Nam. Giá 4.5x tỷ+ Căn 3PN 2WC tầng trung tòa CT3, 104m², nội thất cơ bản, SĐCC. Giá 6,xxx tỷ+ Căn 2PN 2WC tầng trung tòa CT5, 72m², full nội thất mới tinh, SĐCC. Giá 4.4x tỷ.+ Căn góc 2PN 2WC, tầng trung tòa CT4, 70m², SĐCC. Giá 4.7x tỷ.+ Căn góc 2PN 2WC, tầng cao tòa CT5, 81.3m², SĐCC. Giá 4.9x tỷ.+ Căn 2PN 2WC, tầng trung tòa CT2 Nam Xa La, 90m², SĐCC. Giá 6.1x tỷ.+ Căn 2PN 2WC tầng trung tòa Newhouse Xa La, 60m², SĐCC. Giá 4.8x tỷ.+ Căn 2PN 2WC tầng trung tòa CT5, 77m², SĐCC. Giá 4.6x tỷ.+ Căn 2PN 2WC tầng trung tòa CT1 Nam Xa La, 84m², HĐMB. Giá 4.0x tỷ.+ Căn 2PN 2WC, tầng trung tòa CT2 Nam Xa La, 90m², SĐCC. Giá 6.1x tỷ.+ Căn 2PN 2WC, tầng trung tòa Newhouse Xa La, 70m², SĐCC. Giá 5.7x tỷ.+ Căn góc 2PN 2WC, tầng trung tòa CT4C Xa La, 70m², SĐCC, ban công Đông Nam. Giá 4.5x tỷ+ Căn 2PN 2WC, tầng 2x tòa CT1 Nam Xa La, 84m², SĐCC. Giá 4.9x tỷ.+ Căn 3PN 2WC, tầng trung tòa CT1 Xa La, 100m², SĐCC. Giá 5.8x tỷ.+ Căn 2PN 1WC, tầng trung tòa BMM, 63m², SĐCC. Giá 4.3x tỷ.+ Căn góc 2PN 2WC, tầng trung tòa CT4, 70m², SĐCC. Giá 4.6x tỷ.+ Căn 2PN 1WC, tầng trung tòa CT1, 84m², SĐCC. Giá 4.6x tỷ.+ Căn 3PN 2WC, tầng trung tòa Hemisco, 90m², SĐCC. Giá 6.1x tỷ.+ Căn 2PN 1WC, tầng trung tòa CT1B2, 75m², HĐMB. Giá 4.0x tỷ.+ Căn 2PN 2WC, tầng trung tòa Hemisco, 86m². SĐCC. Giá 5.4x tỷ.+ Căn 2PN 1WC, tầng trung tòa CT4C, 54m², SĐCC. Giá 3.7x tỷ.+ Căn 4PN 2WC, tầng Pen tòa CT1B1, 217m². SĐ vi bằng. Giá 6.7x tỷ.+ Căn 1PN 1WC, tầng thấp tòa CT1 Nam Xa La, 42m², HĐMB. Giá 2.3x tỷ.+ Căn 1PN 1WC, tầng cao tòa CT4B, 54m², SĐCC. Giá 3.4x tỷ.+ Căn 2PN 2WC, tầng trung tòa CT4A, 70m², SĐCC. Giá 4.6x tỷ.+ Căn 2PN 2WC, tầng trung tòa CT2A, 63m², SĐCC. Giá 4.1x tỷVà còn gần trăm căn hộ chủ nhà gửi bán tại tất cả các tòa trong KĐT Xa La, Hà Đông.Quý khách hàng có nhu cầu tìm mua căn hộ vui lòng liên hệ Hotline Hà Phương0986 186 ***.",
        "images": [
            "https://i1.ytimg.com/vi/6ASKbHsKoC0/default.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-12d7_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-8231_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-e419_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-396b_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-b76b_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-9472_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-5050_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/18/20251218172944-ca41_wm.jpg"
        ],
        "date_posted": "2025-12-04",
        "date_expired": "2025-12-19",
        "news_type": "Tin thường",
        "contact_info": {
            "name": "Hoàng Thị Thu Phương",
            "profile_url": "https://guru.batdongsan.com.vn/pa/hoangthithuphuong.0784?productType=38&cateId=324&projectId=53&cityCode=HN&districtId=15",
            "avatar_url": "https://file4.batdongsan.com.vn/resize/255x180/2025/04/16/20250416152018-f85e.jpg",
            "phone_visible": "0986 186 *** · Hiện số",
            "zalo_url": "https://zalo.me/XKoBOE125WPTh7mzednzkXgBFZqRiYcpn9JBixNpecZsv08rQmQ"
        },
        "scraped_at": "2025-12-19 02:04:05"
    })

    # post = collection.find_one({"post_id": "38619623"})
    # print(post)