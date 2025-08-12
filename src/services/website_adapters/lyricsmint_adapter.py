import requests
from bs4 import BeautifulSoup
from .base_adapter import BaseAdapter

class LyricsMintAdapter(BaseAdapter):
    def __init__(self, http_client):
        super().__init__(http_client)
        self.BASE_URL = "https://www.lyricsmint.com"

    def get_song_urls(self, max_pages=10):
        urls = []
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{self.BASE_URL}/page/{page}"
                response = requests.get(page_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    if '/lyrics/' in link['href']:
                        urls.append(self.BASE_URL + link['href'])
            except:
                continue
        return urls
    
    def extract_song_data(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_elem = soup.find('h1') or soup.find('title')
            lyrics_elem = soup.find('div', class_='lyrics') or soup.find('div', {'id': 'lyrics'})
            
            if not title_elem or not lyrics_elem:
                return None
                
            return {
                'title': title_elem.get_text().strip(),
                'lyrics': lyrics_elem.get_text().strip(),
                'url': url,
                'source': 'LyricsMint'
            }
        except:
            return None