import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def get_usd_rate_google_csv():
    # 計算時間：因為匯率可能週末不開盤，我們直接抓取過去 3 天的資料確保一定有數據
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    
    # 將日期格式化為 Google 財經需要的字串格式 (例如: 2026-08-01)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # 這是 Google Finance 官方提供、專門下載金融與匯率歷史數據的純文字 CSV 接口
    url = f"https://google.com{start_str}&enddate={end_str}&output=csv"
    
    # 備用官方數據接口（如果上面被限制，直接向 Google 的財經核心組件庫讀取）
    url_backup = "https://google.com"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            csv_text = response.read().decode('utf-8')
            lines = csv_text.strip().split('\n')
            
            # 檢查 Google 回傳的 CSV 資料結構
            if len(lines) > 1:
                # 第一行通常是欄位標題 (Date,Open,High,Low,Close,Volume)
                # 第二行就是最新一天的收盤數據
                latest_data = lines[1].split(',')
                if len(latest_data) > 4:
                    # 通常第 4 個欄位（索引 4）是當天的收盤價 (Close)
                    rate = latest_data[4]
                    print(f"★ 測試成功！★")
                    print(f"從 Google 官方數據庫抓取目前 1 美金對台幣 (TWD) 匯率為: {rate}")
                    return
            
            # 如果 CSV 接口當前維護中，啟動下方的 Google 精準文字匹配保險機制
            req_backup = urllib.request.Request(url_backup, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_backup, timeout=15) as resp_backup:
                html = resp_backup.read().decode('utf-8')
                import re
                # 利用正則表達式尋找包含匯率的 JSON 數據區塊
                match = re.search(r'\["USD",\s*"TWD",\s*([\d\.]+)\]', html)
                if match:
                    print(f"★ 測試成功！★")
                    print(f"從 Google 網頁核心數據提取目前 1 美金對台幣 (TWD) 匯率為: {match.group(1)}")
                else:
                    print("無法解析數據。請查看 GitHub 黑色畫面的完整日誌。")
                    
    except Exception as e:
        print(f"Google 金融接口連線或解析發生錯誤: {e}")

if __name__ == "__main__":
    get_usd_rate_google_csv()
