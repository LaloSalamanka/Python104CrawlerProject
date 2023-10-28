from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fetch_data_workpage import Fetch_data_workpage
class Mainpage_driver:
    # -----主頁面邏輯-----
    # 設定Chrome Driver的執行檔路徑
    options = Options()
    options.add_experimental_option("detach", True)

    # 建立Driver物件實體，用程式操作瀏覽器運作
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    # 打開網頁
    driver.get("https://www.104.com.tw/jobs/main/")
    # 在104打java搜尋
    keywordInput = driver.find_element(By.ID, "ikeyword")
    keywordInput.send_keys("python")
    time.sleep(1)
    button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.js-formCheck")
    button.send_keys(Keys.RETURN)
    # 點選全職
    fulltime_ul = driver.find_element(By.ID, "js-job-tab")
    fulltime_button = fulltime_ul.find_elements(By.TAG_NAME, "li")[1]
    fulltime_button.click()
#   -----------------------------------------------
    time.sleep(1)

    # 工作頁面
    jobs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "article.b-block--top-bord.job-list-item.b-clearfix.js-job-item a.js-job-link"))
    )
    # for i in range(0, len(job_link)): # 從這邊進入每個工作頁面
    for i in range(0, 5): # 這邊測試 只取五個工作

        jobs[i].click() # 開啟工作頁面
        # 切換到工作頁面視窗
        new_window_handle = driver.window_handles[-1]
        driver.switch_to.window(new_window_handle)

        # 爬蟲取得內容
        url = driver.current_url
        Fetch_data_workpage(url)

        # 從這邊進入公司頁面
        companies = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/div/a[1]"))
        )
        companies.click()
        time.sleep(1)

        windows = driver.window_handles # 取得所有頁面

        driver.switch_to.window(windows[2])
        driver.close() # 關閉公司頁面

        driver.switch_to.window(windows[1])
        driver.close() # 關閉工作頁面

        driver.switch_to.window(windows[0]) # 回到主頁面
    driver.quit() # 關閉瀏覽器




