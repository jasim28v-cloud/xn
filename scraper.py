import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vista_prime_scraper():
    # تم تغيير الرابط إلى الأخبار العامة لـ RT
    rss_url = "https://arabic.rt.com/rss/news/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # 1. جلب المباريات
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for league in match_soup.find_all('div', class_='matchCard')[:4]:
            for m in league.find_all('div', class_='allMatchesList')[:1]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text}-{res[1].text}" if len(res) > 1 else "LIVE"
                matches_html += f'''
                <div class="m-card">
                    <div class="m-team">{t1}</div>
                    <div class="m-score">{score}</div>
                    <div class="m-team">{t2}</div>
                </div>'''

        # 2. جلب الأخبار الإخبارية (RT Arabic)
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            if not img: continue 
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">ULTRA</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>{datetime.now().strftime('%d/%m - %H:%M')}</span>
                            <span class="n-more">إقرأ المزيد</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. واجهة VISTA PRIME الشفافة
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISTA PRIME | فيستا برايم</title>
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
            color: #fff; 
            font-family: 'Cairo', sans-serif; 
            margin: 0; 
            min-height: 100vh;
        }}

        header {{ 
            background: rgba(0, 0, 0, 0.4); 
            backdrop-filter: blur(20px); 
            padding: 20px 8%; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            border-bottom: 1px solid var(--glass); 
            position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-decoration: none; text-transform: uppercase; letter-spacing: 2px; }}
        .logo span {{ color: var(--gold); text-shadow: 0 0 15px var(--gold); }}

        .container {{ max-width: 1300px; margin: 30px auto; padding: 0 20px; }}

        .match-scroller {{ display: flex; gap: 20px; overflow-x: auto; padding-bottom: 25px; scrollbar-width: none; }}
        .m-card {{ 
            background: var(--glass); 
            min-width: 220px; 
            padding: 20px; 
            border-radius: 20px; 
            border: 1px solid rgba(255,255,255,0.1); 
            text-align: center; 
            backdrop-filter: blur(10px);
            transition: 0.5s ease;
        }}
        .m-card:hover {{ border-color: var(--accent); transform: translateY(-5px); background: rgba(0, 242, 255, 0.05); }}
        .m-team {{ font-size: 14px; font-weight: 700; margin: 10px 0; }}
        .m-score {{ color: var(--accent); font-family: 'Orbitron'; font-weight: 900; font-size: 18px; text-shadow: 0 0 10px rgba(0,242,255,0.5); }}

        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }}
        .n-card {{ 
            background: var(--glass); 
            border-radius: 24px; 
            overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.08); 
            transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(5px);
        }}
        .n-card:hover {{ transform: scale(1.02); border-color: var(--gold); box-shadow: 0 15px 45px rgba(0,0,0,0.6); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        
        .n-img {{ position: relative; height: 210px; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 1s; }}
        .n-badge {{ position: absolute; top: 15px; left: 15px; background: var(--gold); color: #000; font-size: 9px; font-weight: 900; padding: 5px 15px; border-radius: 50px; text-transform: uppercase; }}
        
        .n-info {{ padding: 25px; }}
        .n-info h3 {{ font-size: 18px; margin: 0 0 15px 0; line-height: 1.6; font-weight: 700; height: 58px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.5); border-top: 1px solid var(--glass); padding-top: 15px; }}
        .n-more {{ color: var(--gold); font-weight: 900; letter-spacing: 1px; }}

        .ad-slot {{ display: flex; justify-content: center; margin: 40px 0; }}

        footer {{ 
            padding: 80px 20px; text-align: center; border-top: 1px solid var(--glass); 
            background: linear-gradient(transparent, rgba(255, 207, 75, 0.05)); margin-top: 80px; 
        }}
        .f-logo {{ font-family: 'Orbitron'; font-size: 28px; font-weight: 900; margin-bottom: 20px; }}

        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
            header {{ padding: 15px 5%; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="{my_link}" class="logo">VISTA<span>PRIME</span></a>
        <div style="background: rgba(0, 242, 255, 0.1); color: var(--accent); padding: 5px 15px; border-radius: 50px; font-size: 11px; font-weight: bold; border: 1px solid var(--accent);">ULTRA NEWS</div>
    </header>

    <div class="container">
        <div class="match-scroller">
            {matches_html}
        </div>

        <div class="ad-slot">
            <ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>
        </div>

        <h2 style="font-size: 26px; font-weight: 900; margin: 40px 0 30px; border-right: 5px solid var(--gold); padding-right: 15px;">آخر التغطيات العالمية <span style="color:var(--gold)">.</span></h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-slot">
             <script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>
        </div>
    </div>

    <footer>
        <div class="f-logo">VISTA <span>PRIME</span></div>
        <p style="opacity: 0.6; font-size: 14px;">نظام رصد إخباري فائق الجودة - جميع الحقوق محفوظة 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Done: Vista Prime news interface created in index.html")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vista_prime_scraper()
