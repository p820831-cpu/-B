import urllib.request
import json

def get_usd_rate():
    url = "https://er-api.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("result") == "success":
                twd_rate = data["rates"].get("TWD")
                print(f"★ 測試成功！目前 1 美金對台幣 (TWD) 匯率為: {twd_rate} ★")
            else:
                print("API 回傳失敗")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    get_usd_rate()
