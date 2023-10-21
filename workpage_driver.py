import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Workpage_driver:
    def __init__(self, url):
        optionss = Options()
        optionss.add_experimental_option("detach", True)
        optionss.chrome_executable_path = r"C:\Users\austi\PycharmProjects\pythonCrawler\chromedriver.exe"
        Workpage_Driver = webdriver.Chrome(options=optionss)
        Workpage_Driver.maximize_window()
        Workpage_Driver.get(url)

        for i in range(2, 22):  # 開啟一個頁面中的20個工作頁面

            job_link = WebDriverWait(Workpage_Driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-job-link"))
            )
            job_link[i].click()
            time.sleep(1)
            # 切換到新的窗口
            new_window_handle = Workpage_Driver.window_handles[-1]
            Workpage_Driver.switch_to.window(new_window_handle)

            Workpage_Driver.implicitly_wait(10)  # 等待 JavaScript 加載完成

            # 在新窗口上進行操作，例如爬取資料
            html = Workpage_Driver.page_source  # 因為是動態生成的元素, 所以要用這方法等js加載完成才能取得元素
            soup = BeautifulSoup(html, "html.parser")

            label_t3mb0 = soup.find_all("div", class_="list-row row mb-2")
            requirements = soup.find("div", class_="job-requirement-table row")
            requirements = requirements.find_all("div", class_="list-row row mb-2")

            # 工作待遇
            salary = soup.find("p", class_="t3 mb-0 mr-2 text-primary font-weight-bold align-top d-inline-block")
            if salary:
                salary = salary.text.strip()
            else:
                print("N/A")
            # 管理責任
            management = label_t3mb0[4]
            management = management.find("div", class_="col p-0 list-row__data")
            if management:
                management = management.text.strip()
            else:
                print("N/A")
            # 出差外派
            overseas_assignment = label_t3mb0[5]
            overseas_assignment = overseas_assignment.find("div", class_="t3 mb-0")
            if overseas_assignment:
                overseas_assignment = overseas_assignment.text.strip()
            else:
                print("N/A")
            # 上班時段
            working_hours = label_t3mb0[6]
            working_hours = working_hours.find("div", class_="t3 mb-0")
            if working_hours:
                working_hours = working_hours.text.strip()
            else:
                print("N/A")
            # 需求人數
            vacancies = label_t3mb0[9]
            vacancies = vacancies.find("div", class_="t3 mb-0")
            if vacancies:
                vacancies = vacancies.text.strip()
            else:
                print("N/A")

            # 條件要求:
            # 科系要求 -> 經歷學歷要求
            major = requirements[2]
            major = major.find("div", class_="t3 mb-0")
            if major:
                major = major.text.strip()
            else:
                print("N/A")
            # 語文條件
            language = requirements[3]
            language = language.find("div", class_="t3 mb-0")
            if language:
                language = language.text.strip()
            else:
                print("N/A")
            # 擅長工具 -> 技能需求
            tools = requirements[4]
            tools = tools.find("div", class_="t3 mb-0")
            if tools:
                tools = tools.text.strip()
            else:
                print("N/A")
            # 工作技能 -> 技能需求
            skills = requirements[5]
            skills = skills.find("div", class_="t3 mb-0")
            if skills:
                skills = skills.text.strip()
            else:
                print("N/A")

            # 資料庫用update的方法寫資料進去吧
            try:
                conn = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    password='12345678',
                    database='test'
                )
                print("成功連接到 MySQL 伺服器!!!!!!")
            except pymysql.Error as err:
                print(f"連接失敗：{err}")

            # 創建一個游標物件
            with conn.cursor() as cursor:
                # 創建資料表（如果不存在）
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS 104crawler_test_workplace (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        salary VARCHAR(255), 
                        management VARCHAR(255), 
                        overseas_assignment VARCHAR(255), 
                        working_hours VARCHAR(255), 
                        vacancies VARCHAR(255), 
                        major VARCHAR(255), 
                        language VARCHAR(255), 
                        tools VARCHAR(255), 
                        skills VARCHAR(255)
                    ) AUTO_INCREMENT = 1;
                ''')

                cursor.execute('''
                    INSERT INTO 104crawler_test_workplace (
                        salary, management, overseas_assignment, working_hours, vacancies, major, language, tools, skills)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (salary, management, overseas_assignment, working_hours, vacancies, major, language, tools, skills))
                # 提交事務
                conn.commit()
            # 連接會在退出 with 區塊時自動關閉

            Workpage_Driver.close()
            Workpage_Driver.switch_to.window(Workpage_Driver.window_handles[0])

        Workpage_Driver.quit()
