import urllib.request
import re

def get_usd_rate_from_google():
    # 直接使用 Google 財經的美金對台幣網頁
    url = "https://www.google.com/finance/quote/USD-TWD"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 使用正則表達式，精準定位 Google 財經網頁中的匯率數字區塊
            # Google Finance 原始碼中通常含有 data-last-price="32.xxxx" 的屬性
            match = re.search(r'data-last-price="([\d\.]+)"', html)
            
            if match:
                twd_rate = match.group(1)
                print(f"★ 測試成功！從 Google 財經抓取目前 1 美金對台幣 (TWD) 匯率為: {twd_rate} ★")
            else:
                # 備用尋找方案：搜尋網頁中顯示的特定數據結構
                match_backup = re.search(r'data-exchange-rate="([\d\.]+)"', html)
                if match_backup:
                    print(f"★ 測試成功！目前 1 美金對台幣 (TWD) 匯率為: {match_backup.group(1)} ★")
                else:
                    print("無法從 Google 財經網頁解析出匯率數字。")
                    
    except Exception as e:
        print(f"連線至 Google 發生錯誤: {e}")

if __name__ == "__main__":
    get_usd_rate_from_google()
