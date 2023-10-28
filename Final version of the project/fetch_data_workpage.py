import requests
from bs4 import BeautifulSoup
import mysql.connector
import pymysql
import time

class Fetch_data_workpage:
    def __init__(self, url):
        time.sleep(1)
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text, "lxml")
            # 職缺名稱
            try:
                job_title_div = soup.find_all("div", class_="text-truncate d-inline-block align-bottom")
                job_title = job_title_div[2].text.strip()
                print(job_title)

            except Exception as e:
                print(f"Error in job_title: {e}")

            try:
                conn = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    password='12345678',
                    database='test',
                    charset='utf8mb4'
                )

                # 創建一個游標物件
                cursor = conn.cursor()
                # 創建資料表（如果不存在）
                cursor.execute('''
                            CREATE TABLE IF NOT EXISTS test (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                職缺名稱 VARCHAR(255),
                                company_name VARCHAR(255)
                            )
                        ''')

                # 插入資料
                cursor.execute('''
                INSERT INTO test (職缺名稱)
                VALUES (%s)
                                ''', (job_title))

                # 提交事務
                conn.commit()

                # 關閉連接
                cursor.close()
                conn.close()

            except mysql.connector.Error as err:
                print(f"連接失敗：{err}")

        else:
            print("取得網頁內容失敗")




