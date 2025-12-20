from pymongo import MongoClient, errors
from utils.logger import get_logger

logger = get_logger("mongodb")


class MongoDBClient:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
            self.client.server_info()  # test connection

            self.db = self.client["real_estate"]
            self.col = self.db["posts"]
            self.col.create_index("post_id", unique=True)

            logger.info("MongoDB connected successfully.")

        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise


    def insert_post(self, data: dict) -> bool:
        try:
            self.col.insert_one(data)
            return True

        except errors.DuplicateKeyError:
            logger.warning(
                f"Duplicate post_id={data.get('post_id')}, skipped."
            )
            return False

        except Exception as e:
            logger.error(
                f"MongoDB insert error | post_id={data.get('post_id')} | {e}"
            )
            return False


    def insert_many_posts(self, data_list: list) -> int:
        """Chèn hàng loạt tin, trả về số lượng tin mới đã chèn thành công."""
        if not data_list:
            return 0

        try:
            # ordered=False: Nếu gặp tin trùng, nó bỏ qua và tiếp tục chèn các tin khác
            result = self.col.insert_many(data_list, ordered=False)
            return len(result.inserted_ids)

        except errors.BulkWriteError as bwe:
            # Lọc ra bao nhiêu tin mới thực sự được chèn thành công
            inserted_count = bwe.details.get('nInserted', 0)
            logger.warning(f"Bulk insert có trùng lặp. Đã chèn thành công {inserted_count} tin mới.")
            return inserted_count

        except Exception as e:
            logger.error(f"Lỗi insert_many: {e}")
            return 0

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("MongoDB connection closed.")
