import urllib.request
import json

def get_usd_rate():
    # 更換為另一個免費且對 GitHub Actions 較友善的 API 來源
    url = "https://er-api.com"
    
    # 備用 API 網址（如果上面那個也失敗，可以試試這行：https://er-api.com ）
    
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8')
            
            # 檢查是否為空內容
            if not html_content.strip():
                print("錯誤：API 回傳了空內容")
                return
                
            data = json.loads(html_content)
            
            # 根據新 API 的格式解析資料
            if data.get("success") == True or "quotes" in data:
                twd_rate = data.get("quotes", {}).get("USDTWD")
                print(f"★ 測試成功！目前 1 美金對台幣 (TWD) 匯率為: {twd_rate} ★")
            elif "rates" in data:
                twd_rate = data["rates"].get("TWD")
                print(f"★ 測試成功！目前 1 美金對台幣 (TWD) 匯率為: {twd_rate} ★")
            else:
                print(f"API 回傳資料格式不符。收到的內容為: {html_content[:100]}")
                
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    get_usd_rate()
