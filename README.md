# Real Estate Data Scraper
## Giới thiệu
Dự án được xây dựng nhằm thu thập và lưu trữ dữ liệu bất động sản từ website **batdongsanvn**.  
Dữ liệu sau khi thu thập được lưu trữ trong **MongoDB** để phục vụ cho việc phân tích dữ liệu.
---
## Nguồn dữ liệu
- Website: https://batdongsan.com.vn/
---

## Mô Tả Trường Dữ Liệu Đầu Ra

| Trường (Field) | Kiểu dữ liệu | Mô tả chi tiết                                                                          |
| :--- |:-------------|:----------------------------------------------------------------------------------------|
| `post_id` | `str`        | ID duy nhất của bài đăng lấy từ URL.                                                    |
| `property_url` | `str`        | Đường dẫn chi tiết đến bài đăng.                                                        |
| `transaction_type` | `str`        | Loại giao dịch: `sale` (bán) hoặc `rent` (cho thuê).                                    |
| `property_category` | `str`        | Loại hình BĐS: `Apartment`, `Private House`, `Land Plot`,...                            |
| `title` | `str`        | Tiêu đề chính của bài đăng.                                                             |
| `address` | `str`        | Địa chỉ đầy đủ của bất động sản.                                                        |
| `latitude` | `float`      | Tọa độ vĩ độ.                                                                           |
| `longitude` | `float`      | Tọa độ kinh độ.                                                                         |
| `price` | `str`        | Giá niêm yết (đơn vị: VND).                                                             |
| `price_per_spm` | `str`        | Đơn giá trên mỗi m² (đơn vị: VND).                                                      |
| `area` | `str`        | Diện tích bất động sản (đơn vị: m²").                                                   |
| `description` | `str`        | Nội dung văn bản mô tả chi tiết bất động sản.                                           |
| `images` | `list[str]`  | Danh sách các link ảnh của bài đăng.                                                    |
| `verified` | `str`        | Trạng thái tin chính chủ xác thực.                                                      |
| `date_posted` | `date`       | Ngày tin được đăng lên sàn.                                                             |
| `date_expired` | `date`       | Ngày tin hết hạn hiển thị.                                                              |
| `news_type` | `str`        | Phân cấp gói tin (Tin thường, Tin VIP...).                                              |
| `scraped_at` | `date`       | Thời điểm dữ liệu được thu thập <br/>(YYYY-MM-DDTHH:MM:SS).                             |
| `spec` | `object`     | Chứa các thông tin đặc diểm của bất dộng sản(bedroom, bathroom, orientation, legal...). |
| `project_info` | `object`     | Chứa thông tin dự án (name, investor, status, price, listing_count).                    |
| `contact_info` | `object`     | Chứa thông tin người đăng (name, phone_invisible, profile_url, avatar_url, listings).   |

---
## Project Structure
```text
vn-real-estate-scraper/
├── data/
├── notebooks/                  # EDA
│   └── processing.ipynb
├── src/
│   ├── scraper.py              # Selenium Webdriver
│   ├── parser.py               # Parse HTML
│   ├── cleaner.py              # Chuyển kiểu dữ liệu (Price, Area, Date)
│   ├── mongo_client.py         # Kết nối đến MongoDB
│   └── utils/
│       ├── logger.py           # Quản lý ghi Log
│       └── helper.py           # Đọc config
├── config.yaml                 # Cấu hình targets, headless driver
├── main.py                     # Script chạy chính
├── requirements.txt            # Danh sách thư viện Python cần thiết
└── .gitignore
```
---
## Dữ liệu đầu ra

```json
    {
        "post_id": "42518171",
        "property_url": "https://batdongsan.com.vn/ban-nha-biet-thu-lien-ke-duong-do-muoi-phuong-duong-quan-prj-hoang-huy-new-city/mot-can-duy-nhat-gia-goc-tu-chu-dau-tu-khong-chenh-pr42518171",
        "transaction_type": "sale",
        "property_category": "Villa/Townhouse",
        "title": "Quỹ căn Hoàng Huy New City giá gốc không chênh từ chủ đầu tư CRV",
        "address": "Dự án Hoàng Huy New City, Đường Đỗ Mười, Phường Dương Quan, Thủy Nguyên, Hải Phòng",
        "latitude": 20.87749671689332,
        "longitude": 106.68012628537717,
        "price": "5 tỷ",
        "area": "90 m2",
        "spec": {
            "bedroom": "4 phòng",
            "bathroom": "3 phòng",
            "num_floor": "5 tầng",
            "orientation": "Bắc",
            "balcony_direction": "Bắc",
            "front_width": "6.0 m",
            "road_width": "17.0 m",
            "legal": "Hợp đồng mua bán"
        },
        "description": "* Dự án Hoàng Huy New City giai đoạn 2 - nơi cuộc sống thăng hoa - quỹ độc quyền.Em Huy đang sở hữu quỹ căn không chênh từ chủ đầu tư siêu đẹp vị trí cực kỳ đắc địa và chuyển nhượng lại 1 số căn đẹp giá rẻ. Quý cô chú anh chị cần thêm thông tin có thể liên hệ ngay với em để lấy sản phẩm phù hợp ạ. LH:0866 666 ***.Website:Http://hoanghuynewcity-haiphong.com/* Hoàng Huy New City giai đoạn 2 - Sự kế thừa hoàn hảo của một khu đô thị đẳng cấp, nơi hội tụ đầy đủ tiện ích hiện đại và không gian sống xanh. Đây không chỉ là nơi an cư lý tưởng mà còn là điểm đến đầu tư sinh lời bền vững!* Điểm nổi bật của dự án.* Vị trí vàng - Tọa lạc tại trung tâm khu vực phát triển bậc nhất, kết nối thuận tiện với các trục đường chính, trung tâm thương mại, trường học và bệnh viện.* Tiện ích đẳng cấp - Hồ bơi vô cực, công viên cây xanh, phòng gym hiện đại, khu vui chơi trẻ em, khu BBQ và nhiều tiện ích khác đáp ứng mọi nhu cầu sống.* Thiết kế tinh tế - Căn hộ được thiết kế thông minh, tận dụng tối đa ánh sáng tự nhiên và không gian thoáng đãng, mang đến sự thoải mái tuyệt đối.* An ninh tuyệt đối - Hệ thống an ninh 24/7, camera giám sát, thẻ từ thông minh đảm bảo an toàn cho cư dân.* Không gian sống xanh.Hoàng Huy New City giai đoạn 2 được bao quanh bởi cây xanh và hồ nước, mang đến bầu không khí trong lành, giúp bạn tận hưởng cuộc sống bình yên giữa lòng đô thị.* Cơ hội đầu tư sinh lời.Với tiềm năng phát triển vượt bậc của khu vực, sở hữu căn hộ tại Hoàng Huy New City giai đoạn 2 chính là quyết định thông minh cho tương lai.* Ưu đãi đặc biệt: Ngoài áp dụng tất cả các chính sách và chiết khấu của CĐT dành cho khách hàng, em Huy còn có chiết khấu riêng CỰC KHỦNG, chiết khấu SUPER VIP cho các bác mà không đơn vị hay sale nào có* Liên hệ ngayHotline:0866 666 ***.Địa chỉ: Khu đô thị Hoàng Huy New City.* Hoàng Huy New City giai đoạn 2 - Nơi cuộc sống viên mãn bắt đầu!",
        "images": [
            "https://file4.batdongsan.com.vn/resize/200x200/2025/12/23/20251223191741-1bb4_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/11/04/20251104091911-aec6_wm.jpg",
            "https://file4.batdongsan.com.vn/resize/200x200/2025/11/04/20251104091911-7484_wm.jpg",
        ],
        "project_info": {
            "name": "Hoàng Huy New City",
            "status": "Đã bàn giao",
            "price": "18 - 30,53 triệu/m²",
            "investor": "Công ty CP Đầu tư Dịch vụ Tài chính Hoàng Huy",
            "image": "https://file4.batdongsan.com.vn/crop/320x320/2022/03/15/20220315082153-35b4.jpg",
            "project_url": "https://batdongsan.com.vn/du-an-khu-do-thi-moi-thuy-nguyen-hp/hoang-huy-new-city-pj5537",
            "listing_count": 55
        },
        "date_posted": "2025-12-25",
        "date_expired": "2026-01-07",
        "news_type": "Tin VIP Bạc",
        "contact_info": {
            "name": "Nguyễn Huy",
            "profile_url": "https://guru.batdongsan.com.vn/pa/nguyenhuy.761?productType=38&cateId=325&projectId=5537&cityCode=HP&districtId=42",
            "avatar_url": "https://file4.batdongsan.com.vn/resize/200x200/2024/08/22/20240822203528-2451.jpg",
            "phone_invisible": "0866 666 *** · Hiện số",
            "zalo_url": "https://zalo.me/-CbFIW6rzw0xS0KyDvacDkpDkMzmtdVZhBQl6m8GLMAajzaENa8",
            "join_duration": "6 năm",
            "listings": "17"
        },
        "verified": "verified",
        "scraped_at": "2025-12-24"
    }
```
