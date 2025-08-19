import json
from utils.http_client import HttpClient
from services.website_adapters.lyricsmint_adapter import LyricsMintAdapter

class LyricsService:
    def __init__(self):
        self.http_client = HttpClient()
        self.adapters = {
            'lyricsmint': LyricsMintAdapter(self.http_client)
        }
        self.all_songs = []
    
    def scrape_website(self, website_name, max_songs=1000, max_pages=10):
        if website_name not in self.adapters:
            raise ValueError(f"Adapter for {website_name} not found")
        
        adapter = self.adapters[website_name]
        songs = adapter.scrape(max_songs, max_pages)
        self.all_songs.extend(songs)
        return songs
    
    def scrape_website_batch(self, website_name, start_page, end_page):
        if website_name not in self.adapters:
            raise ValueError(f"Adapter for {website_name} not found")
        
        adapter = self.adapters[website_name]
        songs = adapter.scrape_batch(start_page, end_page)
        return songs
    
    def save_data(self, filename='lyrics_data.json'):
        # Ensure output goes to output folder
        if not filename.startswith('../output/'):
            filename = f'../output/{filename}'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_songs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.all_songs)} songs to {filename}")