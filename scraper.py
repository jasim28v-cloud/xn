import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vista_prime_ultra_ticker():
    # مصدر إخباري مباشر لضمان ظهور الصور بجودة عالية
    rss_url = "https://arabic.rt.com/rss/news/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الإعلاني الخاص بك
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # تجهيز نصوص شريط الأخبار العاجلة
        ticker_text = " • ".join([item.title.text for item in items[:10]])
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            
            if not img: continue # تخطي الأخبار التي لا تحتوي على صور لضمان جمال التصميم
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">LIVE</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">التفاصيل الكاملة</span>
                        </div>
                    </div>
                </a>
            </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISTA PRIME | التغطية الحية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --gold: #ffcf4b; --bg: #030508; --glass: rgba(255, 255, 255, 0.05); }}
        
        body {{ background: var(--bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; overflow-x: hidden; }}
        
        /* شريط الأخبار العاجلة */
        .ticker-wrap {{
            background: rgba(255, 207, 75, 0.1); border-bottom: 1px solid var(--gold);
            overflow: hidden; white-space: nowrap; padding: 10px 0; position: sticky; top: 70px; z-index: 999; backdrop-filter: blur(10px);
        }}
        .ticker {{ display: inline-block; animation: ticker 60s linear infinite; color: var(--gold); font-weight: bold; font-size: 14px; }}
        @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        header {{ 
            background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(20px); 
            padding: 15px 8%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        .n-card {{ background: var(--glass); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); transition: 0.4s; }}
        .n-card:hover {{ transform: translateY(-5px); border-color: var(--gold); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img {{ height: 200px; position: relative; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 10px; left: 10px; background: var(--gold); color: #000; padding: 3px 10px; border-radius: 5px; font-size: 10px; font-weight: 900; }}
        .n-info {{ padding: 20px; }}
        .n-info h3 {{ font-size: 16px; height: 50px; overflow: hidden; margin: 0 0 15px; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 12px; opacity: 0.6; border-top: 1px solid var(--glass); padding-top: 10px; }}

        footer {{ text-align: center; padding: 40px; border-top: 1px solid var(--glass); margin-top: 50px; }}
    </style>
</head>
<body>
    <header>
        <a href="{my_link}" class="logo">VISTA<span>PRIME</span></a>
        <div style="font-size: 10px; color: var(--gold); border: 1px solid var(--gold); padding: 2px 10px; border-radius: 4px;">SYSTEM LIVE</div>
    </header>

    <div class="ticker-wrap">
        <div class="ticker">خبر عاجل: {ticker_text}</div>
    </div>

    <div class="container">
        <div class="news-grid">{news_grid_html}</div>
    </div>

    <footer>
        <div class="logo">VISTA<span>2026</span></div>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Vista Prime with Ticker is ready!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vista_prime_ultra_ticker()
