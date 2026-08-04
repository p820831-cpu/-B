import os
import urllib.request
import urllib.parse
import yfinance as yf

def send_line_notify(message, token):
    # LINE Notify 官方發送接口
    url = "https://line.me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # 封裝訊息內容
    data = urllib.parse.urlencode({"message": message}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("🔔 LINE 通知發送成功！")
    except Exception as e:
        print(f"❌ LINE 通知發送失敗: {e}")

def check_usd_rate():
    print("=" * 60)
    print("★ 自動匯率檢查程式啟動 ★")
    print("=" * 60)
    
    # 從 GitHub 保險箱中讀取 LINE 密鑰
    line_token = os.environ.get("LINE_NOTIFY_TOKEN")
    
    try:
        # 抓取美金對台幣匯率
        usd_twd = yf.Ticker("TWD=X")
        todays_data = usd_twd.history(period='1d')
        
        if not todays_data.empty:
            rate = todays_data['Close'].iloc[-1]
            print(f"💵 當前美金對台幣匯率: {rate:.4f}")
            
            # 設定你的觸發門檻：低於 30 元
            target_price = 30.0
            
            if rate < target_price:
                msg = f"\n🚨 匯率警報！\n目前美金匯率已跌破 {target_price} 元！\n當前最新匯率為: {rate:.4f}"
                if line_token:
                    send_line_notify(msg, line_token)
                else:
                    print("⚠️ 找不到 LINE_NOTIFY_TOKEN，請至 GitHub Settings 設定。")
            else:
                print(f"📊 目前匯率 ({rate:.4f}) 高於 {target_price} 元，不觸發 LINE 通知。")
                
                # 【測試功能】如果你現在想在 LINE 收到一次成功的通知，可以把下面兩行的井字號 # 刪除
                # test_msg = f"\n測試成功！目前美金匯率為: {rate:.4f}（未低於30元，這僅是測試）"
                # send_line_notify(test_msg, line_token)
                
        else:
            print("⚠️ 暫無匯率數據。")
            
    except Exception as e:
        print(f"❌ 讀取匯率或發送時發生錯誤: {e}")
    print("=" * 60)

if __name__ == "__main__":
    check_usd_rate()
