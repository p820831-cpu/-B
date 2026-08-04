import urllib.request
import re

def get_tsmc_price():
    # 抓取台股即時公開股市網頁
    url = "https://tw.stock.yahoo.com/quote/2330.TW"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 搜尋 Yahoo 股市網頁結構中的股價文字 (通常會顯示在特定 Fz(32px) 的價格區塊)
            # 這是一段簡單的正規表達式，抓取網頁中顯示的台積電價格
            match = re.search(r'"price":"([\d\.]+)"', html)
            
            if match:
                price = match.group(1)
                print(f"★ 測試成功！★")
                print(f"從 Yahoo 股市抓取目前台積電 (2330) 股價為: {price} 元")
            else:
                # 備用尋找方案
                match_backup = re.search(r'Fz\(32px\)[^>]*>([\d\.]+)<', html)
                if match_backup:
                    print(f"★ 測試成功！目前台積電 (2330) 股價為: {match_backup.group(1)} 元")
                else:
                    print("已成功連網，但無法從網頁結構中解析出股價數字。")
                    
    except Exception as e:
        print(f"連網抓取股價時發生錯誤: {e}")

if __name__ == "__main__":
    get_tsmc_price()
