import requests
from bs4 import BeautifulSoup
import mysql.connector
import pymysql
from nextpage import Nextpage
from workpage_driver import Workpage_driver
# 工作頁面:
# 工作待遇 -> 薪資分析
# 管理責任
# 出差外派
# 上班時段
# 需求人數

# 條件要求:
# 科系要求 -> 經歷學歷要求
# 語文條件
# 擅長工具 -> 技能需求
# 工作技能 -> 技能需求
# 公司頁面:
# 完整地址 -> 公司分布圖(用地圖視覺化工具或地理資訊系統)
# 資本額 -> 公司規模分析
# 員工人數

# 先把資料都爬下來再合併
def fetch_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="b-block--top-bord job-list-item b-clearfix js-job-item")

    for jobs in articles:  # 這邊是遍歷每一個工作
        block_left = jobs.find("div", class_="b-block__left")
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
        company_applicants = jobs.find("div", class_="b-block__right b-pos-relative")
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
                database='test'
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
            ) AUTO_INCREMENT = 1;
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


# 這邊寫開工作頁面的方法, 包含爬蟲內容




# 這邊寫開公司頁面的方法, 包含爬蟲內容

# for i in range(1, 3):
#     print(f"正在爬第{i}頁")
#     nextpage(i)
#     if i == 2:
#         driver.close()

for i in range(1, 3):
    NextPage = Nextpage(i)
    fetch_data(NextPage.current_url)
    Workpage_driver(NextPage.current_url)

# driver.close()