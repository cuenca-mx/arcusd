from enum import Enum


class OperationStatus(Enum):
    none = 0
    success = 1
    failed = 2


class OperationType(Enum):
    query = 1
    payment = 2
    topup = 3
