import os
import urllib.request
import json
import yfinance as yf

def send_line_bot_message(message, channel_token, user_id):
    # LINE Messaging API 官方發送推播訊息接口
    url = "https://line.me"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_token}"
    }
    
    # 封裝符合 LINE 官方格式的 JSON 內容
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("🔔 LINE Bot 通知發送成功！")
    except Exception as e:
        print(f"❌ LINE Bot 通知發送失敗: {e}")

def check_usd_rate():
    print("=" * 60)
    print("★ 自動匯率檢查程式啟動 (LINE Bot 版) ★")
    print("=" * 60)
    
    # 從 GitHub 保險箱讀取 LINE 機器人設定
    channel_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    
    try:
        usd_twd = yf.Ticker("TWD=X")
        todays_data = usd_twd.history(period='1d')
        
        if not todays_data.empty:
            rate = todays_data['Close'].iloc[-1]
            print(f"💵 當前美金對台幣匯率: {rate:.4f}")
            
            target_price = 30.0
            
            if rate < target_price:
                msg = f"🚨 匯率警報！\n目前美金匯率已跌破 {target_price} 元！\n當前最新匯率為: {rate:.4f}"
                if channel_token and user_id:
                    send_line_bot_message(msg, channel_token, user_id)
            else:
                print(f"📊 目前匯率 ({rate:.4f}) 高於 {target_price} 元，不觸發通知。")
                
                # 【測試開關】直接解開，讓你執行時能立刻在 LINE 收到最新匯率
                test_msg = f"✅ 測試成功！GitHub 目前美金匯率為: {rate:.4f}（未低於30元，這僅是測試）"
                send_line_bot_message(test_msg, channel_token, user_id)
                
        else:
            print("⚠️ 暫無匯率數據。")
            
    except Exception as e:
        print(f"❌ 讀取匯率或發送時發生錯誤: {e}")
    print("=" * 60)

if __name__ == "__main__":
    check_usd_rate()
