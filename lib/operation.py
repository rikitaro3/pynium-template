import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

from lib.e2e_util import Util


class Operation:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)


class Get(Operation):
    def __init__(self, driver, url):
        super().__init__(driver)
        self.url = url

    def exec(self):
        self.logger.debug("Executing Get: " + self.url)
        self.driver.get(self.url)


class Screenshot(Operation):
    def __init__(self, driver, title):
        super().__init__(driver)
        self.title = title

    def exec(self):
        self.logger.debug("Executing Screenshot: " + self.title)
        Util.take_screenshot(self.driver, self.title)


class Click(Operation):
    def __init__(self, driver, xpath):
        super().__init__(driver)
        self.xpath = xpath

    def exec(self):
        self.logger.debug("Executing Click: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
            element.click()
        except Exception as e:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", element
                )
                element.click()
            except Exception as e:
                self.logger.debug("elements not found")


class Submit(Operation):
    def __init__(self, driver, xpath):
        super().__init__(driver)
        self.xpath = xpath

    def exec(self):
        self.logger.debug("Executing Submit: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        element.submit()


class Input(Operation):
    def __init__(self, driver, xpath, value):
        super().__init__(driver)
        self.xpath = xpath
        self.value = value

    def exec(self):
        self.logger.debug("Executing Input: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, self.xpath)))
        element.send_keys(self.value)


class SelectBox(Operation):
    def __init__(self, driver, xpath, value):
        super().__init__(driver)
        self.xpath = xpath
        self.value = value

    def exec(self):
        self.logger.debug("Executing SelectBox: " + self.xpath)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        select = Select(element)
        select.select_by_visible_text(self.value)


class DownloadHTML(Operation):
    def __init__(self, driver, filename):
        super().__init__(driver)
        self.filename = filename

    def exec(self):
        self.logger.debug("Executing DownloadHTML: " + self.filename)
        html = self.driver.page_source
        os.makedirs(
            "temp", exist_ok=True
        )  # ディレクトリが存在しない場合にディレクトリを作成
        with open(os.path.join("temp", self.filename), "w", encoding="utf-8") as f:
            f.write(html)


class ExecuteJS(Operation):
    def __init__(self, driver, script):
        super().__init__(driver)
        self.script = script

    def exec(self):
        self.logger.debug("Executing JavaScript: " + self.script)
        self.driver.execute_script(self.script)


class ClickUntilNotFound(Click):
    def exec(self):
        self.logger.debug("Executing ClickUntilNotFound: " + self.xpath)
        wait = WebDriverWait(self.driver, 3)
        while True:
            try:
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.xpath))
                )
                element.click()
            except Exception as e:
                try:
                    # 要素が見つからない場合、スクロールしてから再度クリックを試みる
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", element
                    )
                    element.click()
                except Exception as e:
                    # スクロールしても要素が見つからない場合、ループを終了
                    self.logger.debug("No more elements found, stopping.")
                    break


class SwitchToFrame(Operation):
    def __init__(self, driver, reference_type, frame_reference=None):
        super().__init__(driver)
        self.frame_reference = frame_reference
        self.reference_type = reference_type

    def exec(self):
        time.sleep(1)  # FIXME: フレーム変更はwaitをいれると壊れる？
        self.logger.debug("Switching to frame: " + str(self.frame_reference))
        if self.reference_type == "index":
            if self.frame_reference is None:
                raise ValueError(
                    "frame_reference must be provided when reference_type is 'index'."
                )
            self.driver.switch_to.frame(int(self.frame_reference))
        elif self.reference_type == "parent":
            self.driver.switch_to.parent_frame()
        else:
            raise ValueError(
                "Invalid reference_type. It should be either 'index' or 'parent'."
            )
