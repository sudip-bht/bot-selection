import logging
import os
from config import LOG_FILE, LOG_FORMAT

def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=LOG_FORMAT
    )

def log_bot_usage(bot_usage: dict):

    logging.info("\n\n### Total Requests Made by Each Bot ###")
    table_header = f"{'Bot ID':<10} {'Requests Made':<15}"
    logging.info(table_header)
    logging.info("-" * len(table_header))  # Line separator
    for bot_id, requests in bot_usage.items():
        logging.info(f"{bot_id:<10} {requests:<15}")
    logging.info("\n")

def log_completion(total_requests: int, execution_time: float):
    """Log completion statistics"""
    logging.info(f"Completed processing {total_requests} requests")
    logging.info(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Completed processing {total_requests} requests")
    print(f"Total execution time: {execution_time:.2f} seconds") 