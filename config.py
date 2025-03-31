TOTAL_BOTS = 1000
ACTIVE_BOTS = 1000  
TIME_WINDOW = 15 * 60

ACCOUNT_TYPES = {
    'A': {'max_requests': 50, 'time_window': 15 * 60},    # 50 requests per 15 minutes
    'B': {'max_requests': 200, 'time_window': 15 * 60},   # 200 requests per 15 minutes
    'C': {'max_requests': 500, 'time_window': 15 * 60}    # 500 requests per 15 minutes
}


REQUEST_DELAY = 0.1  
TOTAL_REQUESTS = 10000


LOG_FILE = "logs/bot_requests.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s" 