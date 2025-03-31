# Multithreaded Bot Management System

A Python-based system for managing concurrent requests using a pool of bots with rate limiting, cooldown mechanisms, and detailed usage statistics.

## Features

- **Multithreaded Architecture**: Concurrent request processing using Python's `threading`
- **Bot Type System**: 3 bot types with different capabilities:
  - **Type A**: 50 requests per 15 minutes
  - **Type B**: 200 requests per 15 minutes
  - **Type C**: 500 requests per 15 minutes
- **Dynamic Bot Management**:
  - Automatic cooldown when limits reached
  - Smart bot selection algorithm
  - Bot type distribution configuration
- **Monitoring & Logging**:
  - Real-time request tracking
  - Bot usage statistics
  - Performance metrics
- **Thread Safety**:
  - Semaphores for concurrency control
  - Locks for shared resource protection

## Requirements

- Python 3.7+
- Standard Libraries:
  - `threading`
  - `time`
  - `random`
  - `collections`

## Installation

- Clone repository:

  ```
  git clone https://github.com/yourusername/bot-system.git
  cd bot-system
  ```

- Set up configuration

  ```
  cp config.example.py config.py
  ```

- Running the program

## Working of Bot Selection Algorithm

### Bot Management & Selection Process

The algorithm use queue architecture to manage bot availability states:

- Active Bots: Currently processing requests

- Available Bots: Ready for task assignment

- Cooldown Queue: Bots that reached request limits

### For efficient bot selection:

- Sampling: A maximum of 10 bots are randomly sampled from the available pool, reducing computational overhead while selecting bot.

#### Scoring Mechanism:

- Usage Ratio (70% Weight): (1 - (completed_requests/max_capacity))
  Prioritizes underutilized bots.
  Here max_capacity depends on type of bots

- Recency Factor (30% Weight): (time_since_last_use/reference_window) ensures bot with longer ideal timer are selected

The bot with the highest score is automatically assigned to new tasks
