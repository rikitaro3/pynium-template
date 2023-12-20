from lib.case import Case
from lib.operation import Click, Get, Screenshot, Submit, Input, SelectBox, DownloadHTML, ExecuteJS, ClickUntilNotFound, SwitchToFrame

import my_const as const

class Catalog:

    @staticmethod
    def login_user(driver):
        case = Case(
            Input(driver, "//*[@name='login_id']", const.ID),
            Input(driver, "//*[@name='password']", const.PASSWORD),
            Submit(driver, "//form[@name='login_form']")
        )
        return case
