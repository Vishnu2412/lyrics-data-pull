# Lyrics Data Framework

Framework for scraping Hindi/Punjabi song lyrics from multiple websites.

## Usage

```bash
cd src
python main.py
```

## Adding New Websites

1. Create new adapter in `services/website_adapters/`
2. Inherit from `BaseAdapter`
3. Implement `get_song_urls()` and `extract_song_data()`
4. Register in `LyricsService`

## Example New Adapter

```python
class NewSiteAdapter(BaseAdapter):
    def get_song_urls(self, max_pages=10):
        # Return list of song URLs
        pass
    
    def extract_song_data(self, url):
        # Return song dict with title, artist, lyrics
        pass
```