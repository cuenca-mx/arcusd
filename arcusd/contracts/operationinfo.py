from .contract import Contract
from ..types import OperationStatus, OperationType


class OpInfo(Contract):

    def __init__(self,
                 tran_type: OperationType,
                 status: OperationStatus = OperationStatus.none,
                 operation=None,
                 error_message=None):
        self.tran_type = tran_type
        self.status = status
        self.operation = operation
        self.error_message = error_message
