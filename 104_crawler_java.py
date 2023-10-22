import requests
from bs4 import BeautifulSoup
import mysql.connector
import pymysql
from nextpage import Nextpage
from workpage_crawler import Workpage_crawler
# 公司頁面:
# 完整地址 -> 公司分布圖(用地圖視覺化工具或地理資訊系統)
# 資本額 -> 公司規模分析
# 員工人數
def fetch_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="b-block--top-bord job-list-item b-clearfix js-job-item")

    for jobs in articles:  # 這邊是遍歷每一個工作
        block_left = jobs.find("div", class_="b-block__left")
        # 職缺名稱
        try:
            job_title = block_left.find("h2", class_="b-tit")
            job_title = job_title.a.text.strip()
        except Exception as e:
            print(f"Error in job_title: {e}")
            job_title = "N/A"

        # 公司名稱
        try:
            company_first_ul = block_left.find("ul", class_="b-list-inline b-clearfix")
            company_first_ul = company_first_ul.find_all('li')
            company_name = company_first_ul[1]
            company_name = company_name.a.text.strip()
        except Exception as e:
            print(f"Error in company_name: {e}")
            company_name = "N/A"

        # 公司產業
        try:
            company_industry = company_first_ul[2]
            company_industry = company_industry.text.strip()
        except Exception as e:
            print(f"Error in company_industry: {e}")
            company_industry = "N/A"

        # 公司區域, 要求經歷, 要求學歷
        try:
            company_second_ul = block_left.find("ul", class_="b-list-inline b-clearfix job-list-intro b-content")
            company_second_ul = company_second_ul.find_all("li")
            company_district = company_second_ul[0]
            company_required_experience = company_second_ul[1]
            company_required_education = company_second_ul[2]
            company_district = company_district.text.strip()
            company_required_experience = company_required_experience.text.strip()
            company_required_education = company_required_education.text.strip()
        except Exception as e:
            print(f"Error in company_district, experience, or education: {e}")
            company_required_education = company_required_experience = company_district = "N/A"

        # 發布日期
        try:
            company_release_date = block_left.find("h2", class_="b-tit")
            company_release_date = company_release_date.find("span", class_="b-tit__date")
            company_release_date = company_release_date.text.strip()
        except Exception as e:
            print(f"Error in company_release_date: {e}")
            company_release_date = "N/A"

        # 應徵人數
        try:
            company_applicants = jobs.find("div", class_="b-block__right b-pos-relative")
            company_applicants = company_applicants.a.text.strip()
        except Exception as e:
            print(f"Error in company_applicants: {e}")
            company_applicants = "N/A"

        # 薪水
        try:
            salary = jobs.find_all(class_="b-tag--default")
            salary = salary[0]
            salary = salary.text.strip()
        except Exception as e:
            print(f"Error in salary: {e}")
            salary = "N/A"

        # 員工人數

        # 連接到 MySQL 資料庫
        try:
            conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='12345678',
                database='104crawler_database_java'
            )
            print("成功連接到 MySQL 伺服器")
        except mysql.connector.Error as err:
            print(f"連接失敗：{err}")

        # 封面的東西爬完後, 呼叫開工作頁面的方法
        # 叫出後開始爬, 爬完關掉

        # 工作頁面爬完, 呼叫開公司頁面的方法
        # 叫出後開始爬, 爬完關掉

        # 最後跟封面的值一起寫進資料庫, 再開始爬下一頁

        # 創建一個游標物件
        cursor = conn.cursor()

        # 創建資料表（如果不存在）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS 104crawler_java (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(255),
                company_name VARCHAR(255),
                company_industry VARCHAR(255),
                salary VARCHAR(255),
                company_district VARCHAR(255),
                company_required_education VARCHAR(255),
                company_required_experience VARCHAR(255),
                company_release_date VARCHAR(255),
                company_applicants VARCHAR(255)
            ) AUTO_INCREMENT = 1;
        ''')

        # 插入資料
        cursor.execute('''
                    INSERT INTO 104crawler_java (job_title, company_name, company_industry, salary, company_district, company_required_education, company_required_experience, company_release_date, company_applicants)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (job_title, company_name, company_industry, salary, company_district, company_required_education,
                      company_required_experience, company_release_date, company_applicants))

        # 提交事務
        conn.commit()

        # 關閉連接
        cursor.close()
        conn.close()



for i in range(1, 151):
    NextPage = Nextpage(i)
    fetch_data(NextPage.current_url)
    # Workpage_crawler(NextPage.current_url)
    # Companypage_crawler(NextPage.current_url)
Nextpage.driver.close()
Nextpage.driver.quit()
