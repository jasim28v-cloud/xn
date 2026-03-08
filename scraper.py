import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_aura_ultra_prime():
    # مصادر الأخبار (يمكنك تغيير الرابط لأي قسم إخباري آخر)
    rss_url = "https://arabic.rt.com/rss/news/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # رابطك الإعلاني الذهبي
    my_ad_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
    
    try:
        # جلب البيانات من المصدر الإخباري
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400/111/ffd700?text=AURA+NEWS"
            
            # بناء شبكة الأخبار
            news_html += f'''
            <div class="news-card animate-on-scroll">
                <a href="{my_ad_link}" target="_blank">
                    <div class="image-wrapper">
                        <img src="{img}" alt="news">
                        <div class="category-tag">عاجل</div>
                    </div>
                    <div class="content-area">
                        <h3>{title}</h3>
                        <div class="card-footer">
                            <span>🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="read-more">التفاصيل الكاملة ←</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # الواجهة الكاملة Ultra Prime
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA NEWS | أورا نيوز الألترا</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --gold: #d4af37; 
            --gold-light: #f9e29c;
            --bg: #050505;
            --glass: rgba(255, 255, 255, 0.03);
            --border: rgba(212, 175, 55, 0.2);
        }}
        
        body {{ 
            background: var(--bg); color: #e0e0e0; font-family: 'Cairo', sans-serif; margin: 0; 
            background-image: radial-gradient(circle at top right, #1a1a1a, #050505);
            overflow-x: hidden;
        }}

        /* Header Prime */
        header {{ 
            background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(25px); 
            padding: 15px 5%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900; color: #fff; text-decoration: none; letter-spacing: 2px; }}
        .logo span {{ color: var(--gold); text-shadow: 0 0 10px var(--gold); }}

        .main-container {{ max-width: 1200px; margin: 40px auto; padding: 0 20px; }}

        /* Popup Styling */
        .overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9);
            display: flex; justify-content: center; align-items: center; z-index: 9999; visibility: hidden; opacity: 0; transition: 0.5s;
        }}
        .overlay.active {{ visibility: visible; opacity: 1; }}
        .popup {{
            background: #111; border: 2px solid var(--gold); padding: 40px; border-radius: 30px;
            text-align: center; max-width: 400px; transform: scale(0.7); transition: 0.5s;
        }}
        .overlay.active .popup {{ transform: scale(1); }}
        .popup h2 {{ font-family: 'Orbitron'; color: var(--gold); margin-bottom: 10px; }}
        .btn-gold {{ 
            display: inline-block; background: var(--gold); color: #000; padding: 12px 30px; 
            border-radius: 50px; text-decoration: none; font-weight: 900; margin-top: 20px;
        }}

        /* News Grid */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; }}
        .news-card {{ 
            background: var(--glass); border-radius: 25px; border: 1px solid var(--border);
            overflow: hidden; transition: 0.4s; backdrop-filter: blur(10px);
        }}
        .news-card:hover {{ transform: translateY(-10px); border-color: var(--gold); box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1); }}
        .news-card a {{ text-decoration: none; color: inherit; }}

        .image-wrapper {{ position: relative; height: 200px; overflow: hidden; }}
        .image-wrapper img {{ width: 100%; height: 100%; object-fit: cover; transition: 1s; }}
        .news-card:hover .image-wrapper img {{ transform: scale(1.1); }}
        .category-tag {{ 
            position: absolute; top: 15px; left: 15px; background: var(--gold); color: #000;
            padding: 4px 12px; border-radius: 8px; font-size: 10px; font-weight: 900;
        }}

        .content-area {{ padding: 20px; }}
        .content-area h3 {{ font-size: 17px; line-height: 1.6; margin: 0 0 15px; color: #fff; height: 55px; overflow: hidden; }}
        .card-footer {{ display: flex; justify-content: space-between; font-size: 12px; color: #888; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px; }}
        .read-more {{ color: var(--gold); font-weight: bold; }}

        /* Animations */
        .animate-on-scroll {{ opacity: 0; transform: translateY(20px); transition: 0.6s ease-out; }}
        .animate-on-scroll.visible {{ opacity: 1; transform: translateY(0); }}

        footer {{ text-align: center; padding: 60px; border-top: 1px solid var(--border); margin-top: 50px; background: #000; }}
        
        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>

    <div class="overlay" id="welcomePopup">
        <div class="popup">
            <h2>AURA PRIME</h2>
            <p>أهلاً بك في الجيل الجديد من التغطية الإخبارية الذكية.</p>
            <a href="{my_ad_link}" class="btn-gold" target="_blank" onclick="closePopup()">دخول المنصة</a>
            <p style="font-size: 10px; color: #555; margin-top: 15px; cursor: pointer;" onclick="closePopup()">تخطي الآن</p>
        </div>
    </div>

    <header>
        <a href="{my_ad_link}" class="logo">AURA<span>NEWS</span></a>
        <div style="font-family: 'Orbitron'; font-size: 11px; color: var(--gold);">ULTRA PREMIER</div>
    </header>

    <div class="main-container">
        <h2 style="font-size: 24px; font-weight: 900; margin-bottom: 35px; color: #fff;">أبرز العناوين اليوم <span style="color: var(--gold);">.</span></h2>
        
        <div class="news-grid">
            {news_html}
        </div>
    </div>

    <footer>
        <div class="logo">AURA<span>2026</span></div>
        <p style="font-size: 13px; opacity: 0.5;">جميع الحقوق محفوظة - نظام أورا نيوز ألترا</p>
    </footer>

    <script>
        // إظهار Popup بعد قليل
        window.addEventListener('load', () => {{
            setTimeout(() => {{ document.getElementById('welcomePopup').classList.add('active'); }}, 1500);
        }});

        function closePopup() {{ document.getElementById('welcomePopup').classList.remove('active'); }}

        // حركة التمرير
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) entry.target.classList.add('visible');
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
    </script>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("Success: Aura News Ultra Prime created!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_aura_ultra_prime()
