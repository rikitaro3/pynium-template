from lib.case import Case
from lib.e2e_util import Util
from lib.operation import Click, Get, Screenshot, Submit, Input, SelectBox, Select

import my_const as const
from my_catalog import Catalog


def main():
    driver = Util.create_driver(True, False)
    login_case = Case(
        Get(driver, const.BASE_URL)
    )
    login_case.exec_operation()


main()
