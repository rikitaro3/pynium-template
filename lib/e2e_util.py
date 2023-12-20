from selenium import webdriver
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import os

# mobile device setting
# USE_MOBILE_DEVICE = "iPhone SE"
USE_MOBILE_DEVICE = "iPhone XR"

# output path
SCREENSHOT_DIR = "screenshot/"


class Util:

    @staticmethod
    def create_driver(is_chrome, is_headless=False):
        """_summary_

        Args:
            is_chrome (bool): trueならchrome, falseならfirefox
            is_headless (bool, optional): chromeのみheadlessを選択できる. Defaults to False.

        Returns:
            _type_: driver

        Sample:
            create_driver(True) # 通常のchrome driver
            create_driver(True,True) # headlessのchrome driver
            create_driver(False) # 通常のfirefox driver
            create_driver(False,True) # ※使わない。通常のfirefox driverを返却
        """

        if is_chrome:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

            # headlessオプション設定
            if is_headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')  # for docker
                chrome_options.add_argument(
                    '--disable-dev-shm-usage')  # for docker

            # ケース完了時にブラウザを閉じない
            chrome_options.add_experimental_option("detach", True)

            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
        else:
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--start-maximized")
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options
            )

        driver.implicitly_wait(10)
        return driver

    @staticmethod
    def create_driver_with_mobile():
        chrome_options = ChromeOptions()
        chrome_options.add_argument(USE_MOBILE_DEVICE)
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        driver.implicitly_wait(10)

        return driver

    @staticmethod
    def set_chrome_options_device(options, device_name):
        mobile_emulation = {'deviceName': device_name}
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        return options

    @staticmethod
    def take_screenshot(driver, file_name):
        file_path = SCREENSHOT_DIR + file_name
        screenshot = None
        if isinstance(driver, Chrome):
            screenshot = driver.get_screenshot_as_file(file_path + ".png")
        elif isinstance(driver, Firefox):
            screenshot = driver.get_full_page_screenshot_as_file(
                file_path + ".png")
        else:
            raise ValueError("Unsupported driver type")

    @staticmethod
    def convert_url(url, parameters):
        converted_url = url
        for parameter in parameters:
            converted_url = converted_url.replaceFirst('\\{.*?\\}', parameter)
        return converted_url

    @staticmethod
    def save_formatted_html(html, file_name):
        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(html, 'html.parser')

        # フォーマットされたHTMLを保存
        formatted_html = soup.prettify()

        # tempフォルダが存在しない場合は作成
        os.makedirs('temp', exist_ok=True)

        with open(os.path.join('temp', file_name), 'w', encoding='utf-8') as f:
            f.write(formatted_html)

    @staticmethod
    def validate_json_keyfile(json_keyfile_name):
        """_summary_
        googleのapiやcredentialのvalidateメソッド

        Args:
            json_keyfile_name (_type_): _description_
            
        Usage:
            from lib.e2e_util import Util

            # JSONキーファイル名を指定して関数を呼び出す
            Util.validate_json_keyfile('client_secret.json')
        
        """

        try:
            # スコープを設定
            scope = ['https://www.googleapis.com/auth/drive']

            # 認証情報を取得
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                json_keyfile_name, scope)

            # Google Driveサービスを作成
            drive_service = build('drive', 'v3', credentials=creds)

            # Google Driveのファイルリストを取得
            results = drive_service.files().list(pageSize=10).execute()
            items = results.get('files', [])

            print('Your client_secret.json is valid.')
            print('Files in your Google Drive:')
            for item in items:
                print(f'{item["name"]} ({item["id"]})')

        except Exception as e:
            print('Your client_secret.json is not valid.')
            print('Error:', e)
