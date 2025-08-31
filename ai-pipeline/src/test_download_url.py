import requests
from bs4 import BeautifulSoup

def test_download_urls():
    """
    Test the actual download URLs to see what's happening
    """
    base_url = "https://pastpapers.co"
    
    # Test URL format from the HTML
    test_url = f"{base_url}/view.php?id=cie/A-Level/Physics-9702/2022-May-June/9702_s22_qp_12.pdf"
    
    print(f"Testing URL: {test_url}")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        # First, let's see what the view.php page actually contains
        print("\n1. Testing view.php endpoint...")
        response = session.get(test_url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        
        if response.status_code == 200:
            # Check if it's a PDF or HTML
            if 'application/pdf' in response.headers.get('content-type', ''):
                print("✓ Direct PDF download!")
                print(f"Content length: {len(response.content)} bytes")
            else:
                print("HTML response received, parsing...")
                soup = BeautifulSoup(response.content, 'html.parser')
                print(f"Title: {soup.title.string if soup.title else 'No title'}")
                
                # Look for download links or redirects
                download_links = soup.find_all('a', href=True)
                print(f"Found {len(download_links)} links:")
                for i, link in enumerate(download_links[:10]):
                    href = link.get('href')
                    text = link.get_text(strip=True)
                    print(f"  {i+1}. {text} -> {href}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Let's also try to access the main page and see if there are different download mechanisms
    print("\n2. Checking main page for download mechanisms...")
    main_url = f"{base_url}/cie/?dir=A-Level/Physics-9702/2022-May-June"
    
    try:
        response = session.get(main_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for any JavaScript or forms that might handle downloads
            scripts = soup.find_all('script')
            forms = soup.find_all('form')
            
            print(f"Found {len(scripts)} scripts and {len(forms)} forms")
            
            # Look for any download buttons or special download links
            download_buttons = soup.find_all('a', class_='btn')
            print(f"Found {len(download_buttons)} button links:")
            for btn in download_buttons[:5]:
                href = btn.get('href', '')
                text = btn.get_text(strip=True)
                classes = ' '.join(btn.get('class', []))
                print(f"  - {text} ({classes}) -> {href}")
            
            # Look for any onclick handlers or data attributes
            onclick_elements = soup.find_all(attrs={'onclick': True})
            print(f"Found {len(onclick_elements)} elements with onclick handlers")
            
    except Exception as e:
        print(f"Error checking main page: {e}")

if __name__ == "__main__":
    test_download_urls()
