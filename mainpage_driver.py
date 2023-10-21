from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
class Mainpage_driver:
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

