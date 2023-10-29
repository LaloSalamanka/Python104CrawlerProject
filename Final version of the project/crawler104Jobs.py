import pymysql
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fetch_data_workpage import Fetch_data_workpage
from fetch_data_companypage import Fetch_data_companypage
from selenium.webdriver.support.ui import Select
class Crawler104Jobs:
    # -----主頁面邏輯-----
    def __init__(self, keyword, table, browser):
        self.keyword = keyword
        self.table = table
        self.browser = browser
        options = Options()
        options.add_experimental_option("detach", True)
        # 創建對應瀏覽器的 WebDriver
        if browser == "Chrome":
            driver = webdriver.Chrome(options=options)
        elif browser == "Edge":
            driver = webdriver.Edge(options=options)

        driver.maximize_window()
        driver.implicitly_wait(5)
        # 打開網頁
        driver.get("https://www.104.com.tw/jobs/main/")
        # 在104打java搜尋
        keywordInput = driver.find_element(By.ID, "ikeyword")
        keywordInput.send_keys(self.keyword)
        time.sleep(1)
        button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.js-formCheck")
        button.send_keys(Keys.RETURN)
        # 點選全職
        fulltime_ul = driver.find_element(By.ID, "js-job-tab")
        fulltime_button = fulltime_ul.find_elements(By.TAG_NAME, "li")[1]
        fulltime_button.click()
    #   -----------------------------------------------
        time.sleep(1)

        # 爬取資料
        for x in range(2, 151): # 翻頁
            jobs = WebDriverWait(driver, 20).until( #工作頁面, 找每個工作連結位置
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article.b-block--top-bord.job-list-item.b-clearfix.js-job-item a.js-job-link"))
            )

            for i in range(0, len(jobs)): # 從這邊進入每個工作頁面
                jobs[i].click() # 開啟工作頁面
                # 切換到工作頁面視窗
                new_window_handle = driver.window_handles[-1]
                driver.switch_to.window(new_window_handle)

                # 爬蟲取得內容
                workpage = Fetch_data_workpage(driver.current_url)

                # 從這邊進入公司頁面
                companies = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/div/a[1]"))
                )
                companies.click()
                time.sleep(1)

                windows = driver.window_handles # 取得所有頁面

                driver.switch_to.window(windows[2])
                companypage = Fetch_data_companypage(driver.current_url)
                driver.close() # 關閉公司頁面

                driver.switch_to.window(windows[1])
                driver.close() # 關閉工作頁面

                # 寫進資料庫
                try:
                    conn = pymysql.connect(
                        host='127.0.0.1',
                        user='root',
                        password='12345678',
                        database='104crawler_database',
                        charset='utf8mb4'
                    )

                    # 創建一個游標物件
                    cursor = conn.cursor()

                    # 創建資料表（如果不存在）
                    cursor.execute(f'''
                               CREATE TABLE IF NOT EXISTS {self.table}(
                                   id INT AUTO_INCREMENT PRIMARY KEY,
                                   職缺更新時間 VARCHAR(255),
                                   職缺名稱 VARCHAR(255),
                                   工作待遇 VARCHAR(255),
                                   公司名稱 VARCHAR(255),
                                   員工人數 VARCHAR(255),
                                   工作經歷 VARCHAR(255),
                                   擅長工具 VARCHAR(255),                          
                                   產業類別 VARCHAR(255),
                                   上班地點 VARCHAR(255)
                               )
                           ''')

                    # 插入資料
                    cursor.execute(f'''
                       INSERT INTO {self.table} (`職缺更新時間`, `職缺名稱`, `工作待遇`, `公司名稱`, `員工人數`, `工作經歷`, `擅長工具`, `產業類別`, `上班地點`)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       ''', (workpage.release_time, workpage.job_title, workpage.salary, companypage.company_name,
                             companypage.number_of_employees, workpage.work_experience, workpage.tool,
                             companypage.industry, workpage.location))

                    # 提交事務
                    conn.commit()

                    # 關閉連接
                    cursor.close()
                    conn.close()

                except pymysql.err.Error as err:
                    print(f"連接失敗：{err}")

                driver.switch_to.window(windows[0]) # 回到主頁面

            # 使用 Selenium 定位並操作下拉式選單
            dropdown = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     '#main-content .b-float-right label.b-select select.page-select.js-paging-select.gtm-paging-top'))
            )
            select = Select(dropdown)

            # 選擇特定頁數（這裡是第 page 頁）
            select.select_by_value(str(x))
            time.sleep(2)

        driver.quit() # 關閉瀏覽器
