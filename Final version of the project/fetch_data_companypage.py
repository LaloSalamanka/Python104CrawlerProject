import requests
from bs4 import BeautifulSoup
import time

class Fetch_data_companypage:
    company_name = None
    number_of_employees = None
    industry = None
    def __init__(self, url):
        # time.sleep(1)
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text, "lxml")

            # 公司名稱
            try:
                company_name = soup.find("h1", class_="h1 d-inline")
                self.company_name = company_name.text.strip()
            except Exception as e:
                print(f"Error in company_name: {e}")
            # 公司規模
            try:
                number_of_employees = soup.find_all("div", class_="row mb-2")
                number_of_employees = number_of_employees[3].find("div", class_="col pl-1 p-0 intro-table__data")
                number_of_employees = number_of_employees.find("p", class_="t3 mb-0")
                self.number_of_employees = number_of_employees.text.strip()
            except Exception as e:
                print(f"Error in number_of_employees: {e}")
            # 產業類別
            try:
                industry = soup.find("div", class_="intro-table row")
                industry = industry.find("div", class_="col pl-1 p-0 intro-table__data")
                industry = industry.find("p", class_="t3 mb-0")
                self.industry = industry.text.strip()
            except Exception as e:
                print(f"Error in industry: {e}")

        else:
            print("取得網頁內容失敗")