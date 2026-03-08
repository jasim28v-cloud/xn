import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vista_prime_news_only():
    # مصدر أخبار الجزيرة
    rss_url = "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a23964341ee0/48d6e144-2f3c-4d2b-ad42-261647306947"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الإعلاني الخاص بك
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # جلب أخبار الجزيرة
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]): # عرض 16 خبرًا لتغطية أوسع
            title = item.title.text
            img = None
            media_content = item.find('media:content')
            if media_content:
                img = media_content.get('url')
            elif item.find('enclosure'):
                img = item.find('enclosure').get('url')
            
            if not img:
                img = "https://via.placeholder.com/600x400/030508/ffcf4b?text=ALJAZEERA+PRIME"
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">ULTRA NEWS</div>
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

        # واجهة VISTA PRIME الشفافة (بدون يلا كورة)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISTA PRIME | فيستا برايم - الجزيرة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --gold: #ffcf4b; 
            --accent: #00f2ff;
            --glass: rgba(255, 255, 255, 0.05);
            --bg: #030508;
        }}
        
        body {{ 
            background: var(--bg); 
            background-image: radial-gradient(circle at 50% 50%, #0a111a 0%, #030508 100%);
            color: #fff; font-family: 'Cairo', sans-serif; margin: 0; min-height: 100vh;
        }}

        header {{ 
            background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(20px); 
            padding: 20px 8%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; text-transform: uppercase; letter-spacing: 2px; }}
        .logo span {{ color: var(--gold); text-shadow: 0 0 15px var(--gold); }}

        .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}

        /* شبكة الأخبار */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        .n-card {{ 
            background: var(--glass); border-radius: 20px; overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.08); transition: 0.4s ease;
            backdrop-filter: blur(10px);
        }}
        .n-card:hover {{ transform: translateY(-8px); border-color: var(--gold); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        
        .n-img {{ position: relative; height: 200px; overflow: hidden; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 1s; }}
        .n-card:hover .n-img img {{ transform: scale(1.1); }}
        .n-badge {{ position: absolute; top: 15px; left: 15px; background: var(--gold); color: #000; font-size: 9px; font-weight: 900; padding: 4px 12px; border-radius: 50px; }}
        
        .n-info {{ padding: 20px; }}
        .n-info h3 {{ font-size: 17px; margin: 0 0 15px 0; line-height: 1.6; font-weight: 700; height: 55px; overflow: hidden; color: #fff; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.5); border-top: 1px solid var(--glass); padding-top: 15px; }}
        .n-more {{ color: var(--gold); font-weight: 900; }}

        .ad-slot {{ display: flex; justify-content: center; margin: 40px 0; }}

        footer {{ 
            padding: 60px 20px; text-align: center; border-top: 1px solid var(--glass); 
            background: rgba(0,0,0,0.8); margin-top: 80px; 
        }}
        .f-logo {{ font-family: 'Orbitron'; font-size: 24px; font-weight: 900; color: #fff; }}

        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="{my_link}" class="logo">VISTA<span>PRIME</span></a>
        <div style="color: var(--gold); font-family: 'Orbitron'; font-size: 11px; letter-spacing: 1px;">● LIVE FEED</div>
    </header>

    <div class="container">
        <div class="ad-slot">
            <ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>
        </div>

        <h2 style="font-size: 24px; font-weight: 900; margin-bottom: 30px; border-right: 5px solid var(--gold); padding-right: 15px;">آخر أخبار الجزيرة</h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-slot">
             <script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>
        </div>
    </div>

    <footer>
        <div class="f-logo">VISTA <span>PRIME</span></div>
        <p style="opacity: 0.5; font-size: 12px; margin-top: 10px;">نشرة إخبارية متكاملة مدعومة بتقنيات الرصد الحديثة - 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Vista Prime News Edition is ready!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vista_prime_news_only()
