from lib.case import Case
from lib.e2e_util import Util
from lib.spreadsheet_writer import SpreadsheetWriter
from lib.operation import Click, Get, Screenshot, Submit, Input, SelectBox, Select, DownloadHTML

import my_const as const
from my_catalog import Catalog


def main():
    driver = Util.create_driver(True, False)
    login_case = Case(
        Get(driver, const.BASE_URL),
        DownloadHTML(driver, "example.html")
    )
    login_case.exec_operation()
    
    writer = SpreadsheetWriter('client_secret.json', 'sample')
    # スプレッドシートにデータを出力
    writer.write([])


if __name__ == "__main__":
    main()
