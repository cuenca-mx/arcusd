from .enums.optype import OperationType
from .enums.opstatus import OperationStatus


class OpInfo:
    def __init__(self,
                 tran_type: OperationType,
                 status: OperationStatus = OperationStatus.NONE,
                 operation=None,
                 error_message=None):
        self.type = tran_type
        self.status = status
        self.operation = operation,
        self.error_message = error_message
