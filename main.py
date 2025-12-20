import time
import random
from src.scraper import get_browser, fetch_list_links, parse
from src.storage import save_data
from src.utils.helper import load_seen_ids, load_config
from src.utils.logger import get_logger
# from src.mongo_client import MongoDBClient

logger = get_logger("main")

def run_scraper():
    """
    Main workflow with daily file persistence.
    """
    logger.info("=== STARTING SCRAPER SYSTEM ===")

    # Load config
    cfg = load_config()
    sc_cfg = cfg.get('scraper', {})
    targets = cfg.get('targets', [])

    if not targets:
        logger.error("No targets found in config.yaml")
        return

    # mongo = MongoDBClient()
    driver = get_browser(headless=sc_cfg.get('headless', False))

    # Preloading existing IDs
    seen_ids = load_seen_ids()
    logger.info(f"Loaded {len(seen_ids)} previously saved IDs.")

    start_time = time.time()
    total_new_records = 0
    total_skipped = 0
    pages_processed = 0

    try:
        for target in targets:
            if not target.get('enabled', True):
                logger.info(f"Skipping disabled target: {target.get('name')}")
                continue

            name = target.get('name')
            base_url = target.get('url')
            start_page = target.get('start_page', 1)
            end_page = target.get('end_page', 2)

            logger.info(f"=== PROCESSING TARGET: {name.upper()} ===")

            for p in range(start_page, end_page + 1):
                current_page_url = base_url if p == 1 else f"{base_url}/p{p}"
                logger.info(f"=== ACCESSING PAGE {p} ===")

                links, skipped_count = fetch_list_links(driver, current_page_url)
                total_skipped += skipped_count

                if not links:
                    logger.info(f"No new items on Page {p}. Moving to next...")
                    continue

                results = parse(driver, links)

                if results:
                    save_data(results)
                    # mongo.insert_many_posts(results)
                    total_new_records += len(results)

            pages_processed += 1
            time.sleep(random.uniform(3, 6))

    except Exception as e:
        logger.critical(f"SYSTEM CRASH: {e}", exc_info=True)
    finally:
        if 'driver' in locals() and driver:
            try:
                logger.info("Closing browser and database connection...")
                driver.quit()
                # mongo.close()
            except Exception as e:
                logger.debug(f"Error close connection: {e}")

        duration_seconds = time.time() - start_time
        minutes, seconds = divmod(int(duration_seconds), 60)

        logger.info(" === SUMMARY ===")
        logger.info(f" Total pages processed: {pages_processed}")
        logger.info(f" Total new records added: {total_new_records}")
        logger.info(f" Total items duplicated: {total_skipped}")
        logger.info(f" Total Duration: {minutes}m {seconds}s")
        logger.info("=== PROCESS FINISHED ===")


if __name__ == "__main__":
    run_scraper()