from enum import Enum


class OperationStatus(str, Enum):
    none = 'NONE'
    success = 'SUCCESS'
    failed = 'FAILED'


class OperationType(str, Enum):
    query = 'QUERY'
    payment = 'PAYMENT'
    topup = 'TOPUP'
