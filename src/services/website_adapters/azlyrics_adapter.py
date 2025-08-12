from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base_adapter import BaseAdapter

class AZLyricsAdapter(BaseAdapter):
    def __init__(self, http_client):
        super().__init__(http_client)
        self.base_url = 'https://www.azlyrics.com'
    
    def get_song_urls(self, max_pages=10):
        urls = []
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{self.base_url}/browse/page/{page}"
                response = self.http_client.get(page_url, delay=1.0)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.select('a[href*="/lyrics/"]')
                for link in links:
                    urls.append(urljoin(self.base_url, link['href']))
            except:
                continue
        return urls
    
    def extract_song_data(self, url):
        try:
            response = self.http_client.get(url, delay=1.0)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('h1, .lyricsh')
            lyrics = soup.select_one('div[class=""]')  # AZLyrics specific
            artist = soup.select_one('.artist, h2')
            
            if not title or not lyrics:
                return None
                
            return {
                'title': title.get_text().strip(),
                'artist': artist.get_text().strip() if artist else '',
                'lyrics': lyrics.get_text().strip(),
                'url': url,
                'source': 'AZLyrics'
            }
        except:
            return None