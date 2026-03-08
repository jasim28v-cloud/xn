import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vista_prime_aljazeera_fixed():
    # رابط الجزيرة الذي تفضله
    rss_url = "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a23964341ee0/48d6e144-2f3c-4d2b-ad42-261647306947"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الإعلاني الخاص بك من المعلومات المحفوظة
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(rss_url, headers=headers, timeout=25)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = None
            
            # محاولة جلب الصورة بأكثر من طريقة لضمان الظهور في GitHub Actions
            media_content = item.find('media:content')
            enclosure = item.find('enclosure')
            
            if media_content and media_content.get('url'):
                img = media_content.get('url')
            elif enclosure and enclosure.get('url'):
                img = enclosure.get('url')
            
            # إذا لم يجد صورة، نضع رابطاً بديلاً لكي لا يظهر المربع فارغاً
            if not img:
                img = "https://www.aljazeera.net/wp-content/uploads/2023/10/Placeholder-Image.jpg"
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy" onerror="this.src='https://via.placeholder.com/600x400/030508/ffcf4b?text=VISTA+NEWS'">
                        <div class="n-badge">ULTRA</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">إقرأ الآن</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # واجهة VISTA PRIME
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISTA PRIME | الجزيرة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --gold: #ffcf4b; --glass: rgba(255, 255, 255, 0.05); --bg: #030508; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; min-height: 100vh; }}
        header {{ background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(20px); padding: 20px 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--gold); }}
        .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        .n-card {{ background: var(--glass); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); transition: 0.4s ease; backdrop-filter: blur(10px); }}
        .n-card:hover {{ transform: translateY(-8px); border-color: var(--gold); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img {{ position: relative; height: 200px; overflow: hidden; background: #111; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 15px; left: 15px; background: var(--gold); color: #000; font-size: 9px; font-weight: 900; padding: 4px 12px; border-radius: 50px; }}
        .n-info {{ padding: 20px; }}
        .n-info h3 {{ font-size: 17px; margin: 0 0 15px 0; line-height: 1.6; font-weight: 700; height: 55px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.5); border-top: 1px solid var(--glass); padding-top: 15px; }}
        .n-more {{ color: var(--gold); font-weight: 900; }}
        footer {{ padding: 60px 20px; text-align: center; border-top: 1px solid var(--glass); margin-top: 80px; }}
        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <a href="{my_link}" class="logo">VISTA<span>PRIME</span></a>
        <div style="color: var(--gold); font-size: 11px;">● LIVE FEED</div>
    </header>
    <div class="container">
        <div class="news-grid">{news_grid_html}</div>
    </div>
    <footer>
        <div class="logo">VISTA <span>PRIME</span></div>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Vista Prime News created!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vista_prime_aljazeera_fixed()
