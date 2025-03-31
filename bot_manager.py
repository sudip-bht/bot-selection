import time
import random
import threading
from collections import deque, defaultdict
from config import (
     ACCOUNT_TYPES,
    REQUEST_DELAY, TOTAL_REQUESTS
)

class BotManager:
    def __init__(self, total_bots: int, active_bots: int):
        
        #  Maintaining a queue for keeping track of bots in different states
        self.all_bots = deque([f"bot_{i}" for i in range(1, total_bots + 1)])
        self.active_bots = set()  
        self.available_bots = deque(self.all_bots)  
        self.cooldown_bots = deque()  
        
        # Randomly assigning account types to bots
        self.account_types = {}
        for i, bot_id in enumerate(self.all_bots):
        
            self.account_types[bot_id] = ['A', 'B', 'C'][i % 3]
        
        # Keeping track of how many requests each bot has made
        self.bot_usage = defaultdict(int)
        self.cooldown_times = defaultdict(float)  
        self.last_selected_time = defaultdict(float)  
        
        # No of requests made so far
        self.total_requests = 0
        self.total_requests_lock = threading.Lock()
        
        #Threading primitives
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(active_bots)
        
        # Initially assign active bots
        with self.lock:
            for _ in range(min(active_bots, len(self.available_bots))):
                bot_id = self.available_bots.popleft()
                self.active_bots.add(bot_id)

    def perform_request(self, bot_id: str, request_id: int) -> None:
        
        with self.semaphore:
            with self.lock:
    
                with self.total_requests_lock:
                    if self.total_requests >= TOTAL_REQUESTS:
                        return
                
                self.bot_usage[bot_id] += 1
                account_type = self.account_types[bot_id]
                max_requests = ACCOUNT_TYPES[account_type]['max_requests']
                time_window = ACCOUNT_TYPES[account_type]['time_window']
                
                
                with self.total_requests_lock:
                    self.total_requests += 1
                
                log_message = f"✅ Request {request_id} sent by {bot_id} (Type: {account_type}, Total: {self.bot_usage[bot_id]}/{max_requests} requests, Global: {self.total_requests}/{TOTAL_REQUESTS})"
                

                if self.bot_usage[bot_id] >= max_requests:
                    if bot_id in self.active_bots:
                        self.active_bots.remove(bot_id)
                        self.cooldown_bots.append(bot_id)
                        self.cooldown_times[bot_id] = time.time()
                        log_message = f"🚨 {bot_id} (Type: {account_type}) reached limit. Cooling down for {time_window/60} minutes"
                      

            time.sleep(REQUEST_DELAY)

    def manage_cooldown(self) -> None:
        
        while True:
            with self.lock:
                current_time = time.time()
                
                for bot_id in list(self.cooldown_bots):
                    account_type = self.account_types[bot_id]
                    time_window = ACCOUNT_TYPES[account_type]['time_window']
                    if current_time - self.cooldown_times[bot_id] >= time_window:
                        self.cooldown_bots.remove(bot_id)
                        self.available_bots.append(bot_id)
                        del self.cooldown_times[bot_id]
                        log_message = f"✅ {bot_id} (Type: {account_type}) has cooled down and is ready to make requests again."
                        print(log_message)
            time.sleep(1)  # Check every second to avoid busy-waiting

    def select_bot(self) -> str:
        """Select a bot based on usage and last selection time."""
        if not self.active_bots:
            return None
            
        current_time = time.time()
        best_score = float('-inf')
        selected_bot = None
        
        active_bots_list = list(self.active_bots)
        
        
        sample_size = min(10, len(active_bots_list))
        sample_bots = random.sample(active_bots_list, sample_size)
        
        for bot_id in sample_bots:
            time_since_last = current_time - self.last_selected_time.get(bot_id, 0)
            account_type = self.account_types[bot_id]
            max_requests = ACCOUNT_TYPES[account_type]['max_requests']
            usage_ratio = self.bot_usage[bot_id] / max_requests
            
            
            score = (1 - usage_ratio) * 0.7 + (time_since_last / 10) * 0.3
            
            if score > best_score:
                best_score = score
                selected_bot = bot_id
        
      
        if selected_bot:
            self.last_selected_time[selected_bot] = current_time
            
        return selected_bot

    def get_random_active_bot(self) -> str:
        """Get a bot using the selection algorithm."""
        with self.lock:
            return self.select_bot()

    def get_bot_usage_stats(self) -> dict:
        """Get usage statistics for all bots."""
        return dict(self.bot_usage)