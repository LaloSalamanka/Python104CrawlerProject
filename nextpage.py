from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from mainpage_driver import Mainpage_driver


class Nextpage:
    current_url = None
    driver = None
    def __init__(self, page):
        self.page = page
        Nextpage.driver = Mainpage_driver().driver
        # 使用 Selenium 定位並操作下拉式選單
        dropdown = WebDriverWait(Nextpage.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#main-content .b-float-right label.b-select select.page-select.js-paging-select.gtm-paging-top'))
        )
        select = Select(dropdown)

        # 選擇特定頁數（這裡是第 page 頁）
        select.select_by_value(str(page))

        # 獲取當前頁面的網址
        Nextpage.current_url = Nextpage.driver.current_url
