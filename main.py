import time
import threading
from bot_manager import BotManager
from logger import setup_logging, log_bot_usage, log_completion
from config import TOTAL_BOTS, ACTIVE_BOTS, TOTAL_REQUESTS, REQUEST_DELAY

# Global variables
total_requests = 0
request_id_counter = 0
counter_lock = threading.Lock()
stop_flag = threading.Event()
request_semaphore = threading.Semaphore(TOTAL_REQUESTS)

def main():
    # Set up logging
    setup_logging()
    
    # Initialize bot manager
    bot_manager = BotManager(TOTAL_BOTS, ACTIVE_BOTS)
    
    # Calculate time
    start_time = time.time()
    
    # Create and start worker threads
    threads = []
    for _ in range(ACTIVE_BOTS):
        thread = threading.Thread(
            target=worker,
            args=(bot_manager, stop_flag, increment_counter)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Monitor total requests and set stop flag when limit reached
    while total_requests < TOTAL_REQUESTS:
        time.sleep(0.00001)
    
    stop_flag.set()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Log final statistics
    log_bot_usage(bot_manager.get_bot_usage_stats())
    log_completion(total_requests, execution_time)

def increment_counter():
    """Thread-safe counter increment"""
    global request_id_counter
    with counter_lock:
        request_id_counter += 1
        return request_id_counter

def worker(bot_manager: BotManager, stop_flag: threading.Event, get_request_id):
    """Worker function that processes requests using bots"""
    global total_requests
    
    while not stop_flag.is_set():
        # Try to acquire a request slot
        if not request_semaphore.acquire(blocking=False):
            break  
            
        
        bot_id = bot_manager.get_random_active_bot()
        if bot_id is None:
            request_semaphore.release()  
            time.sleep(0.001)
            continue
        
        # Get next request ID
        request_id = get_request_id()
        
        # Check if we've reached the limit before making the request
        with counter_lock:
            if total_requests >= TOTAL_REQUESTS:
                request_semaphore.release()
                break
        
        # Perform request
        bot_manager.perform_request(bot_id, request_id)
        
        
        with counter_lock:
            if total_requests < TOTAL_REQUESTS:
                total_requests += 1
                if total_requests >= TOTAL_REQUESTS:
                    stop_flag.set()
            else:
                request_semaphore.release()
                break
        
        request_semaphore.release()

if __name__ == "__main__":
    main() 