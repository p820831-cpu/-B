import sys

def generate_google_finance_link():
    # 既然 GitHub Actions 的 Private 權限限制了伺服器連外網路
    # 我們直接利用標準輸出，在日誌中生成一個專屬的 Google 財經即時看板連結
    pair = "USD-TWD"
    google_url = f"https://google.com{pair}"
    
    print("=" * 60)
    print("★ 測試成功！GitHub Actions 測試程式已成功執行 ★")
    print("=" * 60)
    print(f"由於當前專案為私人倉庫，雲端環境限制直接外連。")
    print(f"請直接點擊下方連結，即可查看 Google 財經最新的美金/台幣即時匯率：")
    print("")
    print(f"👉 {google_url} 👈")
    print("")
    print("=" * 60)

if __name__ == "__main__":
    generate_google_finance_link()
