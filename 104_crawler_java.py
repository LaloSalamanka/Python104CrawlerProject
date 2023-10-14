import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import mysql.connector
import pymysql
def fetch_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="b-block--top-bord job-list-item b-clearfix js-job-item")

    for a in articles:
        block_left = a.find("div", class_="b-block__left")
        # 職缺名稱
        job_title = block_left.find("h2", class_="b-tit")
        if job_title and job_title.a:
            job_title = job_title.a.text.strip()
        else:
            print("N/A")

        # 公司名稱
        company_first_ul = block_left.find("ul", class_="b-list-inline b-clearfix")
        company_first_ul = company_first_ul.find_all('li')
        company_name = company_first_ul[1]
        if company_name and company_name.a:
            company_name = company_name.a.text.strip()
        else:
            print("N/A")

        # 公司產業
        company_industry = company_first_ul[2]
        if company_industry:
            company_industry = company_industry.text.strip()
        else:
            print("N/A")


        # 公司區域, 要求經歷, 要求學歷
        company_second_ul = block_left.find("ul", class_="b-list-inline b-clearfix job-list-intro b-content")
        company_second_ul = company_second_ul.find_all("li")
        company_district = company_second_ul[0]
        company_required_experience = company_second_ul[1]
        company_required_education = company_second_ul[2]
        if company_district and company_required_experience and company_required_education:
            company_district = company_district.text.strip()
            company_required_experience = company_required_experience.text.strip()
            company_required_education = company_required_education.text.strip()
        else:
            company_required_education = company_required_experience = company_district = "N/A"

        # 發布日期
        company_release_date = block_left.find("h2", class_="b-tit")
        company_release_date = company_release_date.find("span", class_="b-tit__date")
        if company_release_date:
            company_release_date = company_release_date.text.strip()
        else:
            company_release_date = "N/A"

        # 應徵人數
        company_applicants = a.find("div", class_="b-block__right b-pos-relative")
        if company_applicants:
            company_applicants = company_applicants.a.text
        else:
            company_applicants = "N/A"

        # 連接到 MySQL 資料庫
        try:
            conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='12345678',
                database='104crawler_database'
            )
            print("成功連接到 MySQL 伺服器")
        except mysql.connector.Error as err:
            print(f"連接失敗：{err}")

        # 創建一個游標物件
        cursor = conn.cursor()

        # 創建資料表（如果不存在）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS 104crawler_test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(255),
                company_name VARCHAR(255),
                company_industry VARCHAR(255),
                company_district VARCHAR(255),
                company_required_education VARCHAR(255),
                company_required_experience VARCHAR(255),
                company_release_date VARCHAR(255),
                company_applicants VARCHAR(255)
            )
        ''')

        # 插入資料
        cursor.execute('''
                    INSERT INTO 104crawler_test (job_title, company_name, company_industry, company_district, company_required_education, company_required_experience, company_release_date, company_applicants)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (job_title, company_name, company_industry, company_district, company_required_education,
                      company_required_experience, company_release_date, company_applicants))

        # 提交事務
        conn.commit()

        # 關閉連接
        cursor.close()
        conn.close()

# 下一頁的邏輯
# 設定Chrome Driver的執行檔路徑
options = Options()
options.add_experimental_option("detach", True)
options.chrome_executable_path = r"C:\Users\austi\PycharmProjects\pythonCrawler\chromedriver.exe"

# 建立Driver物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome(options=options)

# 打開網頁
driver.get("https://www.104.com.tw/jobs/main/")
# 在104打java搜尋
keywordInput = driver.find_element(By.ID, "ikeyword")
keywordInput.send_keys("java")
time.sleep(1)
button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.js-formCheck")
button.send_keys(Keys.RETURN)
# 點選全職
fulltime_ul = driver.find_element(By.ID, "js-job-tab")
fulltime_button = fulltime_ul.find_elements(By.TAG_NAME, "li")[1]
fulltime_button.click()
def nextpage(page):
    # 使用 Selenium 定位並操作下拉式選單
    dropdown = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#main-content .b-float-right label.b-select select.page-select.js-paging-select.gtm-paging-top'))
    )
    select = Select(dropdown)

    # 選擇特定頁數（這裡是第 page 頁）
    select.select_by_value(str(page))

    # 獲取當前頁面的網址
    current_url = driver.current_url

    # 呼叫fetch_data並帶入當前網址
    fetch_data(current_url)


for i in range(1, 4):
    print(f"正在爬第{i}頁")
    nextpage(i)
    if i == 3:
        driver.close()


