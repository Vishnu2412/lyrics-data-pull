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