# Bot Configuration
TOTAL_BOTS = 1000  # Total number of bots to manage
ACTIVE_BOTS = 200  # Number of bots that can be active at once

# Rate limits for each account type
ACCOUNT_TYPES = {
    'A': {'max_requests': 50, 'time_window': 15 * 60},    # 50 requests per 15 minutes
    'B': {'max_requests': 200, 'time_window': 15 * 60},   # 200 requests per 15 minutes
    'C': {'max_requests': 500, 'time_window': 15 * 60}    # 500 requests per 15 minutes
}

# Request Configuration
TOTAL_REQUESTS = 10000  # Total number of requests to make
REQUEST_DELAY = 0.1     # Delay between requests in seconds

# Logging Configuration
LOG_FILE = "logs/bot_requests.log"  # Path to the log file
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # Log message format

