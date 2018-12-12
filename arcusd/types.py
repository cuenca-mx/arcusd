from enum import Enum


class OperationStatus(str, Enum):
    none = 'none'
    success = 'success'
    failed = 'failed'


class OperationType(str, Enum):
    query = 'query'
    payment = 'payment'
    topup = 'topup'
