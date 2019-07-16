from enum import Enum


class OperationStatus(Enum):
    none = 'none'
    success = 'success'
    failed = 'failed'


class OperationType(Enum):
    query = 'query'
    payment = 'payment'
    topup = 'topup'
