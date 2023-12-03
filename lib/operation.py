from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

from lib.e2e_util import Util


class Operation:
    def __init__(self, driver):
        self.driver = driver


class Get(Operation):
    def __init__(self, driver, url):
        super().__init__(driver)
        self.url = url

    def exec(self):
        print("Executing Get: " + self.url)
        self.driver.get(self.url)


class Screenshot(Operation):
    def __init__(self, driver, title):
        super().__init__(driver)
        self.title = title

    def exec(self):
        print("Executing Screenshot: " + self.title)
        Util.take_screenshot(self.driver, self.title)


class Click(Operation):
    def __init__(self, driver, xpath):
        super().__init__(driver)
        self.xpath = xpath

    def exec(self):
        print("Executing Click: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, self.xpath)))
            element.click()
        except:
            # 画面をelementまでスクロールする
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", element)
            element.click()


class Submit(Operation):
    def __init__(self, driver, xpath):
        super().__init__(driver)
        self.xpath = xpath

    def exec(self):
        print("Executing Submit: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, self.xpath)))
        element.submit()


class Input(Operation):
    def __init__(self, driver, xpath, value):
        super().__init__(driver)
        self.xpath = xpath
        self.value = value

    def exec(self):
        print("Executing Input: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, self.xpath)))
        element.send_keys(self.value)


class SelectBox(Operation):
    def __init__(self, driver, xpath, value):
        super().__init__(driver)
        self.xpath = xpath
        self.value = value

    def exec(self):
        print("Executing SelectBox: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, self.xpath)))
        select = Select(element)
        select.select_by_visible_text(self.value)


class DownloadHTML(Operation):
    def __init__(self, driver, filename):
        super().__init__(driver)
        self.filename = filename

    def exec(self):
        print("Executing DownloadHTML: " + self.filename)
        html = self.driver.page_source
        os.makedirs('temp', exist_ok=True)  # ディレクトリが存在しない場合にディレクトリを作成
        with open(os.path.join('temp', self.filename), 'w', encoding='utf-8') as f:
            f.write(html)


class ExecuteJS(Operation):
    def __init__(self, driver, script):
        super().__init__(driver)
        self.script = script

    def exec(self):
        print("Executing JavaScript: " + self.script)
        self.driver.execute_script(self.script)
