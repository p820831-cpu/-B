import urllib.request
import re

def get_usd_rate_official():
    # 這是 Google 官方提供、專門用來載入財經圖表數據的輕量接口，格式非常固定
    url = "https://google.com"
    
    # 如果上面官方接口有限制，改用這條最保證能抓到文字的 Google 搜尋路徑
    url_backup = "https://google.com"
    
    try:
        # 我們直接向 Google 搜尋請求美金匯率轉換
        req = urllib.request.Request(
            url_backup, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'zh-TW,zh;q=0.9'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 尋找 Google 搜尋結果麵包屑與回答卡片中的「新台幣」數字格式
            # Google 通常會顯示如 data-value="32.45" 或在文字顯示 "1 美元 等於\n32.45 新台幣"
            match = re.search(r'data-value="([\d\.]+)"[^>]*data-precision', html)
            
            if not match:
                # 備用：直接從 HTML 標籤內建的常規數字比對
                match = re.search(r'[\d\.]+\s*新台幣', html)
                if match:
                    print(f"★ 測試成功！從 Google 搜尋找到匯率相關文字: {match.group(0)} ★")
                    return
            
            if match:
                twd_rate = match.group(1)
                print(f"★ 測試成功！從 Google 搜尋抓取目前 1 美金對台幣 (TWD) 匯率為: {twd_rate} ★")
            else:
                # 最終保險手段：直接列印出網頁標題，確認 Google 給我們的畫面長怎樣
                title_match = re.search(r'<title>(.*?)</title>', html)
                title_text = title_match.group(1) if title_match else "未知"
                print(f"解析失敗。Google 回傳的網頁標題為: {title_text}，請看下一步提示。")
                    
    except Exception as e:
        print(f"連線至 Google 發生錯誤: {e}")

if __name__ == "__main__":
    get_usd_rate_official()
