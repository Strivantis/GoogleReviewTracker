# Google Reviews Tracker 🗺️  

## 📋 專案簡介
此專案設計用來自動追蹤並收集多個 **Google Maps ID** 的評論，並定期將新評論透過 **Email 通知**。適用於需要監控客戶回饋或 Google Maps 評論的商家、服務供應商或研究者。

---

## 📂 功能概覽  
- **多 ID 同時追蹤**：允許追蹤多個 Google Maps 使用者的評論。  
- **模式選擇**：  
  - **sum_and_track**：初次運行時彙整所有現有評論，並在未來追蹤新評論。  
  - **track_new**：只從程式開始運行後才追蹤並寄送新評論。  
- **郵件自動通知**：新評論發現時自動發送報告到指定 Email。  
- **靈活的檢查間隔**：可自訂每個 ID 的檢查間隔及每輪檢查間隔，避免過度頻繁請求。

---

## 📦 安裝與環境設置（以下為可運行之版本資訊）
1. **確認安裝 Python 3.11**：
   ```bash
   python --version
   ```
2. **安裝所需套件**：
   在終端機中執行：
   ```bash
   pip install selenium==4.25.0 beautifulsoup4==4.12.3 webdriver-manager==4.0.2
   ```

3. **設定 Gmail 應用程式密碼**：
   - 請至[Google 帳戶安全性設定](https://myaccount.google.com/security)開啟**兩步驟驗證**。
   - [建立應用程式密碼](https://myaccount.google.com/apppasswords)，並記錄該密碼。

---

## 🛠️ 使用方法
1. **編輯 `GoogleReviewTracker.py`**：
   在 `__main__` 區段中設定你的追蹤資訊：

   ```python
   ids_with_names = {
       "GoogleID1": "名稱1",
       "GoogleID2": "名稱2",
       # 可自行新增更多 ID
   }

   sender_email = "你的 Gmail"
   receiver_email = "接收通知的 Email"
   password = "你的 Gmail 應用程式密碼"

   # 呼叫 main，設定檢查間隔和每輪等待時間
    main(
        ids_with_names, 
        sender_email, 
        receiver_email, 
        password, 
        mode="sum_and_track", 
        # "sum_and_track" 直接先蒐集目標ID的最近評論並進行未來追蹤; 
        # "track_new" 不蒐集過去評論，從程式碼運行後才開始追蹤並回報
        interval=30,  # 每個 ID 間隔 30 秒
        cycle_wait=300  # 每輪完成後等待 300 秒，以防 Google 擋爬蟲
    )
   ```

2. **執行程式**：
   進入專案目錄並運行：
   ```bash
   python GoogleReviewTracker.py
   ```

---

## ⚙️ 參數說明
- **`mode`**：選擇運行模式，`"sum_and_track"` 或 `"track_new"`。
- **`interval`**：每個 ID 之間的檢查間隔（秒）。
- **`cycle_wait`**：所有 ID 檢查完後的等待時間（秒）。

---

## 📧 郵件通知範例
每當發現新評論時，會收到如下通知：

```
主旨: 名稱1 的新 Google Maps 評論

內容:
商店名稱: XXX
地址: 台北市中正區XX路XX號
評論時間: 2 天前

商店名稱: YYY
地址: 台北市信義區XX街XX號
評論時間: 3 小時前
```

---

## 🛑 錯誤處理
- **SMTP 錯誤**：請確認 Gmail 應用程式密碼正確，且發信郵件地址已開啟應用程式存取權限。
- **爬蟲被封鎖**：增加 `interval` 及 `cycle_wait` 時間，降低請求頻率。
- **無法擷取評論**：被追蹤者設定不公開、確認 Google Maps 頁面是否改版或 ID 是否正確。

