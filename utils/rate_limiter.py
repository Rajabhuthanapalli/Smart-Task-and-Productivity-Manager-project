import time

request_store = {}

RATE_LIMIT = 5        # max requests
TIME_WINDOW = 60      # seconds


def is_rate_limited(client_id: str):
    current_time = time.time()

    if client_id not in request_store:
        request_store[client_id] = []

    # remove expired requests
    request_store[client_id] = [
        t for t in request_store[client_id]
        if current_time - t < TIME_WINDOW
    ]

    if len(request_store[client_id]) >= RATE_LIMIT:
        return True

    request_store[client_id].append(current_time)
    return False
