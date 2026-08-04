import yfinance as yf

def get_perfect_data():
    print("=" * 60)
    print("★ 國際金融庫套件連線測試 ★")
    print("=" * 60)
    
    try:
        # 1. 抓取美金對台幣匯率 (代號: TWD=X)
        usd_twd = yf.Ticker("TWD=X")
        # 取得最新一筆交易數據
        todays_data = usd_twd.history(period='1d')
        if not todays_data.empty:
            # Close 代表最新收盤/即時價
            rate = todays_data['Close'].iloc[-1]
            print(f"💵 國際匯市｜目前 1 美金對新台幣 (TWD) 匯率: {rate:.4f}")
        else:
            print("⚠️ 國際匯市｜目前非交易時段或暫無數據。")
            
    except Exception as e:
        print(f"❌ 國際匯市｜讀取失敗: {e}")
        
    print("-" * 60)
    
    try:
        # 2. 抓取台積電美股 ADR (代號: TSM)，在國際上抓台積電最穩定
        tsmc = yf.Ticker("TSM")
        tsmc_data = tsmc.history(period='1d')
        if not tsmc_data.empty:
            price = tsmc_data['Close'].iloc[-1]
            print(f"📈 國際股市｜台積電美股 ADR (TSM) 最新股價: {price:.2f} 美元")
        else:
            print("⚠️ 國際股市｜暫無台積電美股數據。")
            
    except Exception as e:
        print(f"❌ 國際股市｜讀取失敗: {e}")
        
    print("=" * 60)

if __name__ == "__main__":
    get_perfect_data()
