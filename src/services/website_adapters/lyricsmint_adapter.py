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
            video_url = self._extract_video_url(soup)
            
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
                    'video_url': video_url,
                    'lyrics': full_lyrics.strip(),
                    'url': url,
                    'source': 'LyricsMint'
                }
            return None
        except Exception as e:
            print(f"Error extracting {url}: {e}")
            return None
    
    def _extract_from_h3_structure(self, soup):
        """Extract structured data from h3 Song Info sections"""
        data = {}
        h3_elements = soup.find_all('h3')
        
        for h3 in h3_elements:
            text = h3.get_text().strip()
            if 'Song Info' in text:
                next_elem = h3.find_next_sibling()
                if next_elem:
                    content = next_elem.get_text()
                    for line in content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip().lower()
                            value = value.strip()
                            if key == 'singer': data['artist'] = value
                            elif key == 'lyricist': data['lyricist'] = value
                            elif key == 'music': data['music'] = value
                            elif key == 'director': data['director'] = value
                            elif key == 'language': data['language'] = value
                            elif key == 'choreography': data['choreography'] = value
                            elif key == 'music label': data['music_label'] = value
        return data
    
    def _extract_from_h3_questions(self, soup):
        """Extract writer and cast from h3 question sections"""
        data = {}
        h3_elements = soup.find_all('h3')
        
        for h3 in h3_elements:
            text = h3.get_text().strip()
            if 'written' in text.lower():
                match = re.search(r'written.*?by\s+([A-Za-z\s,&]+)', text, re.IGNORECASE)
                if match: data['writer'] = match.group(1).strip()
            elif 'features' in text.lower() or 'cast' in text.lower():
                match = re.search(r'features\s+([A-Za-z\s,&]+)', text, re.IGNORECASE)
                if match: data['cast'] = match.group(1).strip()
        return data
    
    def _extract_artist(self, soup, title):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('artist'): return h3_data['artist']
        
        # Fallback to title parsing
        if 'Lyrics' in title:
            parts = title.replace('Lyrics', '').strip().split()
            if len(parts) > 1: return ' '.join(parts[1:]).strip()
        return None
    
    def _extract_writer(self, soup):
        # Try h3 questions first
        h3_data = self._extract_from_h3_questions(soup)
        if h3_data.get('writer'): return h3_data['writer']
        
        # Fallback to regex
        text = soup.get_text()
        match = re.search(r'Written by:\s*([A-Za-z\s,&]+)', text)
        return match.group(1).strip() if match else None
    
    def _extract_director(self, soup):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('director'): return h3_data['director']
        
        # Fallback to regex
        text = soup.get_text()
        match = re.search(r'([A-Za-z\s]+) has directed the music video', text)
        return match.group(1).strip() if match else None
    
    def _extract_cast(self, soup):
        # Try h3 questions first
        h3_data = self._extract_from_h3_questions(soup)
        if h3_data.get('cast'): return h3_data['cast']
        
        # Fallback to regex
        text = soup.get_text()
        match = re.search(r'music video.*?features ([A-Za-z\s,&]+)', text)
        return match.group(1).strip() if match else None
    
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
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('lyricist'): return h3_data['lyricist']
        
        # Fallback to regex patterns
        text = soup.get_text()
        patterns = [r'lyrics by[\s:]+([A-Za-z\s,&]+)', r'lyricist[\s:]+([A-Za-z\s,&]+)']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match: return match.group(1).strip()
        return self._extract_writer(soup)
    
    def _extract_music(self, soup):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('music'): return h3_data['music']
        
        # Fallback to regex patterns
        text = soup.get_text()
        patterns = [r'music by[\s:]+([A-Za-z\s,&]+)', r'composed by[\s:]+([A-Za-z\s,&]+)']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match: return match.group(1).strip()
        return None
    
    def _extract_language(self, soup, lyrics):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('language'): return h3_data['language']
        
        # Fallback to script detection
        if re.search(r'[ਅ-ੌ]', lyrics): return 'Punjabi (Gurmukhi)'
        elif re.search(r'[अ-ौ]', lyrics): return 'Hindi/Punjabi (Devanagari)'
        else: return 'Punjabi (Roman)'
    
    def _extract_choreography(self, soup):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('choreography'): return h3_data['choreography']
        
        # Fallback to regex
        text = soup.get_text()
        match = re.search(r'choreograph[a-z]*[\s:]+([A-Za-z\s,&]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_music_label(self, soup):
        # Try h3 structure first
        h3_data = self._extract_from_h3_structure(soup)
        if h3_data.get('music_label'): return h3_data['music_label']
        
        # Fallback to regex
        text = soup.get_text()
        patterns = [r'label[\s:]+([A-Za-z\s0-9&]+)', r'presented by[\s:]+([A-Za-z\s0-9&]+)']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match: return match.group(1).strip()
        return None
    
    def _extract_video_url(self, soup):
        """Extract video URL from embedded players"""
        # YouTube iframe
        youtube_iframe = soup.find('iframe', src=re.compile(r'youtube\.com|youtu\.be'))
        if youtube_iframe:
            return youtube_iframe['src']
        
        # Video tags
        video_tag = soup.find('video')
        if video_tag and video_tag.get('src'):
            return video_tag['src']
        
        # Source tags within video
        if video_tag:
            source = video_tag.find('source')
            if source and source.get('src'):
                return source['src']
        
        return None