import os
import requests
import yfinance as yf

def send_discord_message(message):
    # 從保險箱讀取 Discord 網址
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ 找不到 DISCORD_WEBHOOK_URL，請檢查 GitHub 保險箱設定。")
        return
        
    # Discord 規定的標準傳送內容格式 (json={"content": "你的文字"})
    payload = {"content": message}
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        # Discord 成功發送時會回傳 204 或 200 狀態碼
        if response.status_code in:
            print("🔔 Discord 通知發送成功！")
        else:
            print(f"❌ 發送失敗，錯誤代碼: {response.status_code}，回應: {response.text}")
    except Exception as e:
        print(f"❌ 連線至 Discord 發生異常: {e}")

def check_usd_rate():
    print("=" * 60)
    print("★ 自動匯率檢查程式啟動 (Discord 版) ★")
    print("=" * 60)
    
    try:
        # 抓取最新美金匯率
        usd_twd = yf.Ticker("TWD=X")
        todays_data = usd_twd.history(period='1d')
        
        if not todays_data.empty:
            rate = todays_data['Close'].iloc[-1]
            print(f"💵 當前美金對台幣匯率: {rate:.4f}")
            
            target_price = 30.0
            
            if rate < target_price:
                msg = f"🚨 **【美金匯率警報】**\n目前美金匯率已跌破 {target_price} 元！\n當前最新匯率為: **{rate:.4f}** 📈"
                send_discord_message(msg)
            else:
                print(f"📊 目前匯率 ({rate:.4f}) 高於 {target_price} 元，不觸發通知。")
                
                # 測試開關：直接測試發送，讓你執行時能立刻在 Discord 看到漂亮結果
                test_msg = f"✅ **【測試成功】** GitHub 自動測試程式執行正常！\n目前美金對台幣匯率為: **{rate:.4f}** （尚未低於 30 元）"
                send_discord_message(test_msg)
                
        else:
            print("⚠️ 暫無匯率數據。")
            
    except Exception as e:
        print(f"❌ 讀取匯率時發生錯誤: {e}")
    print("=" * 60)

if __name__ == "__main__":
    check_usd_rate()
