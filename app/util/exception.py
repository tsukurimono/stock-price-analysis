from typing import Any

# -----------------------------------------
# Base Exception for this application.
# -----------------------------------------
class BaseAppException(Exception):
    def __str__(self):
        return 'BaseAppException'

# -----------------------------------------
# Base Business Exception.
# -----------------------------------------
class BusinessAppException(BaseAppException):
    def __str__(self):
        return 'BusinessAppException'

class InvalidDataAppException(BusinessAppException):
    def __str__(self):
        return 'InvalidDataAppException'

class UniqViolationAppException(BusinessAppException):
    def __str__(self):
        return 'UniqViolationAppException'

class UnauthorizedAppException(BusinessAppException):
    def __str__(self):
        return 'UnauthorizedAppException'

class DataNotfoundAppException(BusinessAppException):
    def __str__(self):
        return 'DataNotfoundAppException'

# -----------------------------------------
# Fatal Exception such as. server or network problem.
# -----------------------------------------
class FatalAppException(BaseAppException):
    def __str__(self):
        return 'FatalAppException'

# -----------------------------------------
# Custom Business Exception.
# -----------------------------------------
class InconsistencyDataException(UniqViolationAppException):
    def __init__(self, present: Any, newer: Any):
        self.present = present
        self.newer   = newer

    def __str__(self):
        return 'InconsistencyDataException'
