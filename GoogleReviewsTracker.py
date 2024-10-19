import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 配置郵件
def send_email(subject, content, sender_email, receiver_email, password):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(content, "plain")
        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("📧 郵件發送成功！")
    except Exception as e:
        print(f"❌ 發送郵件時發生錯誤：{e}")

# 擷取評論
def fetch_reviews(target_url):
    try:
        print(f"🌐 正在連接到 {target_url}...")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(target_url)
        time.sleep(5)  # 等待頁面加載

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # 擷取評論區塊
        review_blocks = soup.find_all("div", class_="jftiEf")

        reviews = []
        for block in review_blocks:
            try:
                name = block.find("div", class_="d4r55 YJxk2d").get_text(strip=True)
                address = block.find("div", class_="RfnDt xJVozb").get_text(strip=True)
                time_posted = block.find("span", class_="rsqaWe").get_text(strip=True)

                review_info = f"商店名稱: {name}\n地址: {address}\n評論時間: {time_posted}"
                reviews.append(review_info)
            except Exception as e:
                print(f"❌ 解析單一評論時發生錯誤：{e}")

        return reviews

    except Exception as e:
        print(f"❌ 擷取評論時發生錯誤：{e}")
        return []

# 儲存和更新已寄送的評論
def update_sent_reviews(sent_reviews, new_reviews):
    sent_reviews.update(new_reviews)

def main(ids_with_names, sender_email, receiver_email, password, mode="track_new", interval=30, cycle_wait=300):
    sent_reviews = {id_: set() for id_ in ids_with_names}  # 每個 ID 的已寄送評論
    initial_run = True

    while True:
        try:
            for id_, name in ids_with_names.items():
                target_url = f"https://www.google.com/maps/contrib/{id_}/reviews"
                print(f"🔄 正在檢查 {name} 的評論...")

                current_reviews = fetch_reviews(target_url)

                if initial_run and mode == "sum_and_track":
                    if current_reviews:
                        combined_reviews = "\n\n".join(current_reviews)
                        send_email(f"{name} 的初次評論彙整", combined_reviews, sender_email, receiver_email, password)
                        update_sent_reviews(sent_reviews[id_], current_reviews)
                    continue  # 跳過此次循環

                new_reviews = [r for r in current_reviews if r not in sent_reviews[id_]]

                if new_reviews:
                    print(f"🆕 {name} 發現 {len(new_reviews)} 則新評論！")
                    combined_reviews = "\n\n".join(new_reviews)
                    send_email(f"{name} 的新 Google Maps 評論", combined_reviews, sender_email, receiver_email, password)
                    update_sent_reviews(sent_reviews[id_], new_reviews)
                else:
                    print(f"😴 {name} 沒有新評論")

                time.sleep(interval)  # 每個 ID 間隔一段時間

            initial_run = False  # 第一次檢查結束後標記為 False
            print(f"✅ 所有 ID 已檢查完畢，等待下一輪檢查...\n")
            time.sleep(cycle_wait)  # 每輪完成後等待

        except Exception as e:
            print(f"❌ 主程式發生錯誤：{e}")
            time.sleep(3600)  # 發生錯誤時等待 1 小時

if __name__ == "__main__":
    ids_with_names = {
        "GoogleID1": "名稱1",
        "GoogleID2": "名稱2"  #加逗號之後可以自己新增同時追蹤很多個 Google ID
    }

    # 在此設定郵件相關資訊
    sender_email = "發信者 Gmail 信箱"
    receiver_email = "接收報告的 Email 信箱"
    password = "發信者 Gmail 的應用程式密碼" 

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
