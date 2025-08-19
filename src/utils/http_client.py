import requests
import time

class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def get(self, url, delay=0):
        for attempt in range(3):  # MAX_RETRIES = 3
            try:
                if delay > 0:
                    time.sleep(delay)
                return self.session.get(url, timeout=30)  # REQUEST_TIMEOUT = 30
            except Exception as e:
                if attempt == 2:  # MAX_RETRIES - 1
                    raise e
        return None