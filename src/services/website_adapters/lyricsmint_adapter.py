import requests
from bs4 import BeautifulSoup
import re
from .base_adapter import BaseAdapter

class LyricsMintAdapter(BaseAdapter):
    def __init__(self, http_client):
        super().__init__(http_client)
        self.BASE_URL = "https://www.lyricsmint.com"

    def get_song_urls(self, max_pages=50):
        urls = []
        
        # Get Punjabi songs from multiple sections
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{self.BASE_URL}/punjabi/page/{page}"
                response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find article links that contain song URLs
                articles = soup.find_all('article') or soup.find_all('div', class_=re.compile('post|entry|item'))
                
                for article in articles:
                    links = article.find_all('a', href=True)
                    for link in links:
                        href = link['href']
                        if href.startswith('/'):
                            full_url = self.BASE_URL + href
                        elif href.startswith('http'):
                            full_url = href
                        else:
                            continue
                            
                        # Filter for song pages
                        if (self.BASE_URL in full_url and 
                            not any(skip in href.lower() for skip in ['page', 'category', 'tag', 'author', 'privacy', 'terms']) and
                            len(href.split('/')) >= 3):
                            if full_url not in urls:
                                urls.append(full_url)
                
                if len(urls) >= 1000:
                    break
                    
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
                
        return urls
    
    def get_song_urls_batch(self, start_page, end_page):
        urls = []
        
        for page in range(start_page, end_page + 1):
            try:
                page_url = f"{self.BASE_URL}/punjabi/page/{page}"
                response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find article links that contain song URLs
                articles = soup.find_all('article') or soup.find_all('div', class_=re.compile('post|entry|item'))
                
                for article in articles:
                    links = article.find_all('a', href=True)
                    for link in links:
                        href = link['href']
                        if href.startswith('/'):
                            full_url = self.BASE_URL + href
                        elif href.startswith('http'):
                            full_url = href
                        else:
                            continue
                            
                        # Filter for song pages
                        if (self.BASE_URL in full_url and 
                            not any(skip in href.lower() for skip in ['page', 'category', 'tag', 'author', 'privacy', 'terms']) and
                            len(href.split('/')) >= 3):
                            if full_url not in urls:
                                urls.append(full_url)
                                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
                
        return urls
    
    def extract_song_data(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            if not title_elem:
                return None
            title = title_elem.get_text().strip()
            
            # Extract lyrics from paragraphs
            lyrics_paragraphs = soup.find_all('p')
            full_lyrics = ""
            
            for p in lyrics_paragraphs:
                p_text = p.get_text().strip()
                if (len(p_text) > 20 and 
                    not any(skip in p_text.lower() for skip in ['subscribe', 'click', 'allow', 'home', 'contact', 'menu', 'search', 'copyright'])):
                    full_lyrics += p_text + "\n\n"
            
            # Extract additional song info
            artist = self._extract_artist(soup, title)
            writer = self._extract_writer(soup)
            director = self._extract_director(soup)
            cast = self._extract_cast(soup)
            album = self._extract_album(soup)
            lyricist = self._extract_lyricist(soup)
            music = self._extract_music(soup)
            language = self._extract_language(soup, full_lyrics)
            choreography = self._extract_choreography(soup)
            music_label = self._extract_music_label(soup)
            
            if len(full_lyrics.strip()) > 100:
                return {
                    'title': title,
                    'artist': artist,
                    'writer': writer,
                    'director': director,
                    'cast': cast,
                    'album': album,
                    'lyricist': lyricist,
                    'music': music,
                    'language': language,
                    'choreography': choreography,
                    'music_label': music_label,
                    'lyrics': full_lyrics.strip(),
                    'url': url,
                    'source': 'LyricsMint'
                }
            return None
        except Exception as e:
            print(f"Error extracting {url}: {e}")
            return None
    
    def _extract_artist(self, soup, title):
        # Try to extract artist from title or content
        if 'Lyrics' in title:
            parts = title.replace('Lyrics', '').strip().split()
            if len(parts) > 1:
                return ' '.join(parts[1:]).strip()
        
        # Look for artist info in text
        text = soup.get_text()
        artist_match = re.search(r'has sung the song ".*?".*?([A-Za-z\s]+) is known for singing', text)
        if artist_match:
            return artist_match.group(1).strip()
        return None
    
    def _extract_writer(self, soup):
        text = soup.get_text()
        writer_match = re.search(r'Written by:\s*([A-Za-z\s,&]+)', text)
        if writer_match:
            return writer_match.group(1).strip()
        return None
    
    def _extract_director(self, soup):
        text = soup.get_text()
        director_match = re.search(r'([A-Za-z\s]+) has directed the music video', text)
        if director_match:
            return director_match.group(1).strip()
        return None
    
    def _extract_cast(self, soup):
        text = soup.get_text()
        cast_match = re.search(r'music video.*?features ([A-Za-z\s,&]+)', text)
        if cast_match:
            return cast_match.group(1).strip()
        return None
    
    def _extract_album(self, soup):
        text = soup.get_text()
        # Look for album mentions
        album_patterns = [
            r'album[\s:]+([A-Za-z\s0-9]+)',
            r'from the album[\s:]+([A-Za-z\s0-9]+)',
            r'Album[\s:]+([A-Za-z\s0-9]+)'
        ]
        for pattern in album_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_lyricist(self, soup):
        text = soup.get_text()
        # Look for lyricist info (often same as writer but can be different)
        lyricist_patterns = [
            r'lyrics by[\s:]+([A-Za-z\s,&]+)',
            r'lyricist[\s:]+([A-Za-z\s,&]+)',
            r'Lyrics[\s:]+([A-Za-z\s,&]+)'
        ]
        for pattern in lyricist_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        # Fallback to writer if no specific lyricist found
        return self._extract_writer(soup)
    
    def _extract_music(self, soup):
        text = soup.get_text()
        # Look for music composer/director
        music_patterns = [
            r'music by[\s:]+([A-Za-z\s,&]+)',
            r'music director[\s:]+([A-Za-z\s,&]+)',
            r'composed by[\s:]+([A-Za-z\s,&]+)',
            r'Music[\s:]+([A-Za-z\s,&]+)'
        ]
        for pattern in music_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_language(self, soup, lyrics):
        # Detect language based on script and common words
        if any(char in lyrics for char in 'ਪੰਜਾਬੀ'):
            return 'Punjabi (Gurmukhi)'
        elif any(char in lyrics for char in 'हिंदी'):
            return 'Hindi/Punjabi (Devanagari)'
        elif re.search(r'[ਅ-ੌ]', lyrics):
            return 'Punjabi (Gurmukhi)'
        elif re.search(r'[अ-ौ]', lyrics):
            return 'Hindi/Punjabi (Devanagari)'
        else:
            return 'Punjabi (Roman)'
    
    def _extract_choreography(self, soup):
        text = soup.get_text()
        # Look for choreographer info
        choreo_patterns = [
            r'choreograph[a-z]*[\s:]+([A-Za-z\s,&]+)',
            r'dance director[\s:]+([A-Za-z\s,&]+)',
            r'Choreograph[a-z]*[\s:]+([A-Za-z\s,&]+)'
        ]
        for pattern in choreo_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_music_label(self, soup):
        text = soup.get_text()
        # Look for music label/production house
        label_patterns = [
            r'label[\s:]+([A-Za-z\s0-9&]+)',
            r'production[\s:]+([A-Za-z\s0-9&]+)',
            r'presented by[\s:]+([A-Za-z\s0-9&]+)',
            r'Label[\s:]+([A-Za-z\s0-9&]+)'
        ]
        for pattern in label_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None