from services.lyrics_service import LyricsService

def main():
    service = LyricsService()
    
    # Scrape specific websites
    service.scrape_website('lyricsmint', max_songs=100, max_pages=5)
    
    service.save_data('lyrics_data.json')
    print(f"Total songs collected: {len(service.all_songs)}")

if __name__ == "__main__":
    main()