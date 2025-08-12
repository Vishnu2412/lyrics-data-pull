import requests
import time
from config.settings import DEFAULT_HEADERS, REQUEST_TIMEOUT, MAX_RETRIES

class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
    
    def get(self, url, delay=0):
        for attempt in range(MAX_RETRIES):
            try:
                if delay > 0:
                    time.sleep(delay)
                return self.session.get(url, timeout=REQUEST_TIMEOUT)
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise e
        return None