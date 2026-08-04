import os
import requests
import yfinance as yf

def send_line_bot_message(message, channel_token, user_id):
    # LINE 官方推播接口
    url = "https://line.me"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_token}"
    }
    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    try:
        # 使用 requests.post 自動處理所有底層封裝，100% 確保為 POST 請求
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("🔔 LINE Bot 通知發送成功！")
        else:
            print(f"❌ LINE Bot 發送失敗，錯誤代碼: {response.status_code}")
            print(f"原始回傳內容: {response.text}")
            
    except Exception as e:
        print(f"❌ 連線 LINE 發生異常錯誤: {e}")

def check_usd_rate():
    print("=" * 60)
    print("★ 自動匯率檢查程式啟動 (LINE Bot requests版) ★")
    print("=" * 60)
    
    channel_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    
    try:
        usd_twd = yf.Ticker("TWD=X")
        todays_data = usd_twd.history(period='1d')
        
        if not todays_data.empty:
            rate = todays_data['Close'].iloc[-1]
            print(f"💵 當前美金對台幣匯率: {rate:.4f}")
            
            target_price = 35.0
            
            if rate < target_price:
                msg = f"🚨 匯率警報！\n目前美金匯率已跌破 {target_price} 元！\n當前最新匯率為: {rate:.4f}"
                if channel_token and user_id:
                    send_line_bot_message(msg, channel_token, user_id)
            else:
                print(f"📊 目前匯率 ({rate:.4f}) 高於 {target_price} 元，不觸發通知。")
                
                # 測試開關：直接測試發送
                test_msg = f"✅ 測試成功！GitHub 目前美金匯率為: {rate:.4f}（這僅是測試訊息）"
                if channel_token and user_id:
                    send_line_bot_message(test_msg, channel_token, user_id)
                
        else:
            print("⚠️ 暫無匯率數據。")
            
    except Exception as e:
        print(f"❌ 讀取匯率或發送時發生錯誤: {e}")
    print("=" * 60)

if __name__ == "__main__":
    check_usd_rate()
