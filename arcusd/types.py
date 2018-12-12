from enum import Enum


class OperationStatus(int, Enum):
    none = 0
    success = 1
    failed = 2


class OperationType(int, Enum):
    query = 1
    payment = 2
    topup = 3
