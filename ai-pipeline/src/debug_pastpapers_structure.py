import requests
from bs4 import BeautifulSoup
import json

def debug_pastpapers_structure():
    """
    Debug script to examine the actual HTML structure of pastpapers.co
    """
    url = "https://pastpapers.co/cie/?dir=A-Level/Physics-9702/2022-May-June"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print(f"Fetching: {url}")
        response = session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"\nPage title: {soup.title.string if soup.title else 'No title'}")
        
        # Find all links
        all_links = soup.find_all('a', href=True)
        pdf_links = []
        
        print(f"\nFound {len(all_links)} total links")
        
        for i, link in enumerate(all_links[:20]):  # Show first 20
            href = link.get('href')
            text = link.get_text(strip=True)
            print(f"{i+1:2d}. Text: '{text}' | Href: '{href}'")
            
            if 'pdf' in text.lower() or 'pdf' in href.lower():
                pdf_links.append({
                    "text": text,
                    "href": href,
                    "full_url": f"https://pastpapers.co{href}" if href.startswith('/') else href
                })
        
        print(f"\nFound {len(pdf_links)} PDF-related links:")
        for link in pdf_links:
            print(f"  - Text: '{link['text']}'")
            print(f"    Href: '{link['href']}'")
            print(f"    Full URL: '{link['full_url']}'")
            print()
        
        # Save the HTML for inspection
        with open("debug_pastpapers.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        print("HTML saved to debug_pastpapers.html")
        
        # Save PDF links to JSON
        with open("debug_pdf_links.json", "w") as f:
            json.dump(pdf_links, f, indent=2)
        print("PDF links saved to debug_pdf_links.json")
        
        return pdf_links
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    debug_pastpapers_structure()
