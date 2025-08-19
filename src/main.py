import json
import time
from services.lyrics_service import LyricsService

def main():
    service = LyricsService()
    output_file = 'punjabi_lyricsmint_complete_v2.json'
    
    print("🎵 Starting complete Punjabi songs extraction from LyricsMint...")
    print("📊 Processing pages 1-300 with enhanced song info")
    
    # Extract from page 1 to 300
    batch_size = 50
    start_page = 1
    total_pages = 300
    all_songs = []
    
    for batch_start in range(start_page, total_pages + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, total_pages)
        print(f"\n🔄 Processing batch: pages {batch_start}-{batch_end}")
        
        # Create new service instance for each batch
        batch_service = LyricsService()
        batch_songs = batch_service.scrape_website_batch('lyricsmint', batch_start, batch_end)
        
        if batch_songs:
            all_songs.extend(batch_songs)
            print(f"✅ Batch complete: {len(batch_songs)} songs extracted")
            print(f"📈 Total songs so far: {len(all_songs)}")
            
            # Save progress after each batch
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_songs, f, ensure_ascii=False, indent=2)
            print(f"💾 Progress saved to {output_file}")
        else:
            print("⚠️ No songs found in this batch")
        
        # Small delay between batches
        time.sleep(2)
    
    print(f"\n🎉 Extraction complete!")
    print(f"📊 Total Punjabi songs collected: {len(all_songs)}")
    
    # Show sample of extracted data
    if all_songs:
        print("\n📝 Sample song data:")
        sample = all_songs[0]
        print(f"Title: {sample.get('title', 'N/A')}")
        print(f"Artist: {sample.get('artist', 'N/A')}")
        print(f"Writer: {sample.get('writer', 'N/A')}")
        print(f"Director: {sample.get('director', 'N/A')}")
        print(f"Cast: {sample.get('cast', 'N/A')}")
        print(f"Album: {sample.get('album', 'N/A')}")
        print(f"Music: {sample.get('music', 'N/A')}")
        print(f"Language: {sample.get('language', 'N/A')}")
        print(f"URL: {sample.get('url', 'N/A')}")
        print(f"Lyrics preview: {sample.get('lyrics', '')[:150]}...")

if __name__ == "__main__":
    main()