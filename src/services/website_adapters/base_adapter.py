from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    def __init__(self, http_client):
        self.http_client = http_client
        self.songs = []
    
    @abstractmethod
    def get_song_urls(self, max_pages=10):
        pass
    
    @abstractmethod
    def extract_song_data(self, url):
        pass
    
    def scrape(self, max_songs=1000, max_pages=10):
        urls = self.get_song_urls(max_pages)
        for url in urls[:max_songs]:
            song_data = self.extract_song_data(url)
            if song_data:
                self.songs.append(song_data)
                print(f"Scraped: {song_data['title']}")
        return self.songs
    
    def scrape_batch(self, start_page, end_page):
        batch_songs = []
        urls = self.get_song_urls_batch(start_page, end_page)
        
        for i, url in enumerate(urls, 1):
            try:
                song_data = self.extract_song_data(url)
                if song_data:
                    batch_songs.append(song_data)
                    print(f"  ✓ [{i}/{len(urls)}] {song_data['title'][:50]}...")
                else:
                    print(f"  ✗ [{i}/{len(urls)}] Failed to extract: {url}")
            except Exception as e:
                print(f"  ✗ [{i}/{len(urls)}] Error: {str(e)[:50]}...")
                continue
        
        return batch_songs