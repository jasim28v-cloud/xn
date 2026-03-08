import asyncio
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Optional

# إعداد السجلات (Logs) لمراقبة أداء المحرك
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [X-VOID] - %(message)s")

class VortexScraper:
    def __init__(self):
        self.rss_url = "https://arabic.rt.com/rss/sport/"
        self.matches_url = "https://www.yallakora.com/match-center"
        self.my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'}

    async def fetch_html(self, client: httpx.AsyncClient, url: str) -> str:
        """جلب محتوى الصفحة بشكل غير متزامن"""
        response = await client.get(url, headers=self.headers, timeout=20.0)
        return response.text

    async def get_matches_data(self, client: httpx.AsyncClient) -> str:
        """استخراج بيانات المباريات مع صمامات أمان"""
        try:
            html = await self.fetch_html(client, self.matches_url)
            soup = BeautifulSoup(html, 'lxml')
            matches_html = []
            
            # استهداف البطاقات بدقة أكبر
            for league in soup.select('.matchCard')[:3]:
                for m in league.select('.allMatchesList')[:1]:
                    try:
                        t1 = m.select_one('.teamA').text.strip()
                        t2 = m.select_one('.teamB').text.strip()
                        res = m.select('.MResult span')
                        score = f"{res[0].text}-{res[1].text}" if len(res) > 1 else "VS"
                        
                        matches_html.append(f'''
                        <div class="m-card">
                            <div class="m-team">{t1}</div>
                            <div class="m-score">{score}</div>
                            <div class="m-team">{t2}</div>
                        </div>''')
                    except AttributeError: continue
            return "".join(matches_html)
        except Exception as e:
            logging.error(f"Failed to fetch matches: {e}")
            return ""

    async def get_news_data(self, client: httpx.AsyncClient) -> str:
        """استخراج الأخبار من RSS بأسلوب الـ Grid"""
        try:
            content = await self.fetch_html(client, self.rss_url)
            soup = BeautifulSoup(content, 'xml')
            items = soup.find_all('item')
            
            news_html = []
            current_time = datetime.now().strftime('%H:%M')
            
            for item in items[:16]:
                title = item.title.text
                img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/400x300"
                
                news_html.append(f'''
                <div class="n-card">
                    <a href="{self.my_link}" target="_blank">
                        <div class="n-img">
                            <img src="{img}" loading="lazy" alt="news">
                            <div class="n-badge">حصري</div>
                        </div>
                        <div class="n-info">
                            <h3>{title}</h3>
                            <div class="n-footer">
                                <span>⏱️ {current_time}</span>
                                <span class="n-more">التفاصيل</span>
                            </div>
                        </div>
                    </a>
                </div>''')
            return "".join(news_html)
        except Exception as e:
            logging.error(f"Failed to fetch news: {e}")
            return ""

    async def build_ui(self):
        """تجميع كافة الأجزاء وبناء ملف الـ HTML النهائي"""
        async with httpx.AsyncClient(http2=True) as client:
            # تشغيل العمليتين معاً لتوفير الوقت
            matches_task = self.get_matches_data(client)
            news_task = self.get_news_data(client)
            
            matches_html, news_grid_html = await asyncio.gather(matches_task, news_task)

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | VORTEX</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0b0d11; --card: #161a21; --gold: #c5a059; --text: #e1e1e1; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding: 0; overflow-x: hidden; }}
        header {{ background: var(--card); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 2px solid var(--gold); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--gold); }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        .match-scroller {{ display: flex; gap: 10px; overflow-x: auto; padding-bottom: 15px; margin-bottom: 25px; scrollbar-width: none; }}
        .m-card {{ background: var(--card); min-width: 180px; padding: 12px; border-radius: 12px; border: 1px solid #252a33; text-align: center; }}
        .m-team {{ font-size: 12px; font-weight: bold; margin: 5px 0; }}
        .m-score {{ background: var(--gold); color: #000; font-weight: 900; padding: 2px 8px; border-radius: 4px; display: inline-block; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .n-card {{ background: var(--card); border-radius: 15px; overflow: hidden; border: 1px solid #232932; transition: 0.3s; }}
        .n-card:hover {{ transform: translateY(-5px); border-color: var(--gold); box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img {{ position: relative; height: 180px; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 10px; right: 10px; background: var(--gold); color: #000; font-size: 10px; font-weight: 900; padding: 3px 10px; border-radius: 5px; }}
        .n-info {{ padding: 15px; }}
        .n-info h3 {{ font-size: 15px; margin: 0 0 15px 0; line-height: 1.6; height: 48px; overflow: hidden; font-weight: 700; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #888; }}
        .n-more {{ color: var(--gold); border: 1px solid var(--gold); padding: 2px 10px; border-radius: 20px; }}
        footer {{ background: #000; padding: 40px; text-align: center; border-top: 2px solid var(--gold); margin-top: 50px; }}
        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} .n-img {{ height: 220px; }} }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX<span>26</span></a>
        <div style="color: #00ff88; font-size: 13px; font-weight: bold;">● مباشر</div>
    </header>
    <div class="container">
        <div class="match-scroller">{matches_html}</div>
        <h2 style="border-right: 5px solid var(--gold); padding-right: 15px; margin-bottom: 25px;">أبرز الأخبار الآن</h2>
        <div class="news-grid">{news_grid_html}</div>
    </div>
    <footer>
        <div style="font-size: 26px; font-weight: 900; color: #fff;">VORTEX 26</div>
        <p style="font-size: 12px; color: #555;">تغطية رياضية عالمية بنمط المربعات الفخم</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        logging.info("SUCCESS: index.html has been generated.")

if __name__ == "__main__":
    scraper = VortexScraper()
    asyncio.run(scraper.build_ui())
