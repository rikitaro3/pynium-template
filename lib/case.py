import time
from lib.operation import Operation


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

    def exec_operation(self):
        for operation in self.operations:
            time.sleep(1)  # FIXME: O_o
            operation.exec()
