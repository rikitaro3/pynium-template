import time
from lib.operation import Operation
from selenium.webdriver.remote.webdriver import WebDriver


class Case:

    def __init__(self, *args):
        self.operations = []
        for arg in args:
            if isinstance(arg, Case):
                self.operations.extend(arg.operations)
            elif isinstance(arg, Operation):
                self.operations.append(arg)
            else:
                raise ValueError("Invalid argument type")

    def exec_operation(self, driver: WebDriver = None) -> str:
        for operation in self.operations:
            time.sleep(1)  # FIXME: O_o
            operation.exec()

        time.sleep(2)  # FIXME: O_o
        if driver != None:
            return driver.page_source
