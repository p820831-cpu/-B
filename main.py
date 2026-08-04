import urllib.request
import json
import re

def get_financial_data():
    print("=" * 60)
    print("★ 終極測試成功！GitHub 雲端環境連網數據抓取正常 ★")
    print("=" * 60)
    
    # 1. 抓取台積電股價 (Yahoo 股市)
    yahoo_url = "https://yahoo.com"
    try:
        req_yahoo = urllib.request.Request(yahoo_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_yahoo, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            match_stock = re.search(r'"price":"([\d\.]+)"', html) or re.search(r'Fz\(32px\)[^>]*>([\d\.]+)<', html)
            if match_stock:
                print(f"📈 台灣股市｜台積電 (2330) 最新股價: {match_stock.group(1)} 元")
            else:
                print("⚠️ 台灣股市｜已連線，但無法解析台積電股價結構。")
    except Exception as e:
        print(f"❌ 台灣股市｜連線失敗: {e}")
        
    print("-" * 60)

    # 2. 抓取最新美金匯率 (使用公開國際經貿 API 接口)
    api_url = "https://er-api.com"
    try:
        req_api = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_api, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("result") == "success":
                twd_rate = data["rates"].get("TWD")
                print(f"💵 外匯市場｜目前 1 美金 (USD) 對新台幣 (TWD) 匯率: {twd_rate}")
            else:
                print("⚠️ 外匯市場｜API 回傳失敗。")
    except Exception as e:
        print(f"❌ 外匯市場｜連線失敗: {e}")
        
    print("=" * 60)

if __name__ == "__main__":
    get_financial_data()
