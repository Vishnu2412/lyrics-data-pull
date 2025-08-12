import requests
from bs4 import BeautifulSoup
import json

def test_scrape():
    # Test with a simple lyrics site
    songs = []
    
    # Mock data for testing
    test_songs = [
        {
            'title': 'Tum Hi Ho',
            'artist': 'Arijit Singh',
            'lyrics': 'Hum tere bin ab reh nahi sakte\nTere bina kya wajood mera',
            'url': 'test_url_1',
            'source': 'Test'
        },
        {
            'title': 'Kal Ho Naa Ho',
            'artist': 'Sonu Nigam',
            'lyrics': 'Kal ho naa ho, kal ho naa ho\nPata nahin kya ho kal',
            'url': 'test_url_2', 
            'source': 'Test'
        }
    ]
    
    songs.extend(test_songs)
    
    with open('lyrics_data.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    
    print(f"Created test data with {len(songs)} songs")

if __name__ == "__main__":
    test_scrape()