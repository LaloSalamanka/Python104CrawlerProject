# 從opendata或網路爬蟲擷取資料,並將資料存入資料庫
# 從資料庫讀取資料並進行資料分析與視覺化
#  以簡報方式報告您的專題
    #  選取動機
    #  圖表說明
    #  遇到的問題與解決方式
#  繳交資料:
    #  PPT簡報
    #  來源資料(CSV、JSON、XML皆可)
    #  Python程式碼

# 104職缺分析
    # 爬取所有軟體工程師的職缺
    # 全台灣地區軟體工程師職缺分布
    # 所有java的職缺
    # 所有python的職缺
    # java跟python在資訊軟體系統類佔了多少比例
    # 哪個地區最多職缺
    # 哪個地區最少職缺
    # 最後選出適合去哪邊工作之類的
# 第一步: 先把資料爬出來
# 第二步: 看怎麼存到資料庫裡面
# 第三步: 再從資料庫讀取資料進行分析與資料視覺化
# 第四步: 邊做報告邊用
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time



def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

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
            print("N/A")

        # 發布日期
        company_release_date = block_left.find("h2", class_="b-tit")
        company_release_date = company_release_date.find("span", class_="b-tit__date")
        if company_release_date:
            company_release_date = company_release_date.text.strip()
        else:
            print("N/A")

        # 應徵人數
        company_applicants = a.find("div", class_="b-block__right b-pos-relative")
        if company_applicants:
            company_applicants = company_applicants.a.text
        else:
            print("N/A")

        print(f"""
        {company_release_date} {company_applicants}
        職缺名稱: {job_title}
        公司名稱: {company_name}
        公司產業: {company_industry}
        公司區域: {company_district}
        要求學經歷: {company_required_education}, {company_required_experience}""")
url = 'https://www.104.com.tw/jobs/search/?cat=2007000000&jobsource=2018indexpoc&ro=0'
# fetch_data(url)
# 下一頁的邏輯

# 創建一個 WebDriver
driver = webdriver.Chrome()

# 打開網頁
driver.get("https://www.104.com.tw/jobs/search/?cat=2007000000&jobsource=2018indexpoc&ro=0")

# 使用 Selenium 定位並操作下拉式選單
dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         '#main-content .b-float-right label.b-select select.page-select.js-paging-select.gtm-paging-top'))
)
select = Select(dropdown)

# 選擇特定頁數（這裡是第 page 頁）
select.select_by_value("3")

# 等待頁面跳轉完畢
time.sleep(1)  # 這裡可以調整等待的時間

current_url = driver.current_url

fetch_data(current_url)

    # 準備第二步 怎麼存到資料庫
# for a in articles:
#     title = a.find("h2", class_="b_tit")
#     for b in title:
#         title2 = b.find("a", class_="js-job-link")
#         print(title2.b.text)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     title = soup.title.text
#     print('寫入成功')
#     with open('output.html', 'w', encoding='utf-8') as f:
#         f.write(response.text)
# else:
#     print(f'Error: {response.status_code}')


