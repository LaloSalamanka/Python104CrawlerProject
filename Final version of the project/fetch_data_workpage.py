import requests
from bs4 import BeautifulSoup
import time

class Fetch_data_workpage:
    release_time = None
    job_title = None
    salary = None
    work_experience = None
    tool = None
    location = None
    def __init__(self, url):
        # time.sleep(1)
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text, "lxml")
            # 職缺更新時間
            try:
                release_time = soup.find("span", class_="ml-3 t4 text-gray-darker")
                self.release_time = release_time.text.strip()
            except Exception as e:
                print(f"Error in release_time: {e}")
            # 職缺名稱
            try:
                job_title_div = soup.find_all("div", class_="text-truncate d-inline-block align-bottom")
                self.job_title = job_title_div[2].text.strip()
            except Exception as e:
                print(f"Error in job_title: {e}")
            # 工作待遇
            try:
                salary = soup.find("div", class_="list-row row mb-2 identity-type")
                salary = salary.find("p", class_="t3 mb-0 mr-2 text-primary font-weight-bold align-top d-inline-block")
                self.salary = salary.text.strip()
            except Exception as e:
                print(f"Error in salary: {e}")
            # 工作經歷
            try:
                work_experience = soup.find("div", class_="job-requirement-table row")
                work_experience = work_experience.find("div", class_="list-row row mb-2")
                work_experience = work_experience.find("div", class_="t3 mb-0")
                self.work_experience = work_experience.text.strip()
            except Exception as e:
                print(f"Error in work_experience: {e}")
            # 擅長工具
            try:
                tool = soup.find("div", class_="job-requirement-table row")
                tool = tool.find_all("div", class_="list-row row mb-2")
                tool = tool[4].find("div", class_="t3 mb-0")
                self.tool = tool.text.strip()
            except Exception as e:
                print(f"Error in tool: {e}")
            # 上班地點
            try:
                location = soup.find("div", class_="job-address")
                location = location.find("span")
                self.location = location.text.strip()
            except Exception as e:
                print(f"Error in location: {e}")
        else:
            print("取得網頁內容失敗")