import time
from src import (
    init_browser, process_multiple_pages, save_data,
    init_db, load_seen_ids, load_config, get_logger
)

logger = get_logger("main")

def main():
    logger.info("=== STARTING SCRAPER SYSTEM ===")
    init_db()
    # mongo = MongoDBClient()
    cfg = load_config()
    sc_cfg = cfg.get('scraper', {})
    targets = cfg.get('targets', [])

    if not targets:
        logger.error("No targets found in config.yaml")
        return

    driver = init_browser(headless=sc_cfg.get('headless', False))
    seen_ids = load_seen_ids()
    logger.info(f"Loaded {len(seen_ids)} previously successful IDs")

    start_time = time.time()
    total_new_records = 0
    total_skipped = 0
    pages_processed = 0

    try:
        for target in targets:
            if not target.get('enabled', True):
                logger.info(f"Skipping disabled target: {target.get('name')}")
                continue

            new_record, skipped_record, page_process = process_multiple_pages(
                driver=driver,
                target=target,
                save_data_fn=save_data
            )

            total_new_records += new_record
            total_skipped += skipped_record
            pages_processed += page_process

    except Exception as e:
        logger.critical(f"SYSTEM CRASH: {e}", exc_info=True)

    finally:
        try:
            driver.quit()
        except Exception as e:
            logger.debug(f"Error close connection: {e}")

        duration = int(time.time() - start_time)
        minutes, seconds = divmod(duration, 60)

        logger.info(" === SUMMARY ===")
        logger.info(f" Total pages processed: {pages_processed}")
        logger.info(f" Total new records added: {total_new_records}")
        logger.info(f" Total items duplicated: {total_skipped}")
        logger.info(f" Total Duration: {minutes}m {seconds}s")
        logger.info("=== PROCESS FINISHED ===")


if __name__ == "__main__":
    main()