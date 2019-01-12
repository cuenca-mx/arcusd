from datetime import datetime

from .contract import Contract


class Cancellation(Contract):

    def __init__(self, transaction_id: int, code: str, message: str):
        self.transaction_id = transaction_id
        self.code = code
        self.message = message
        self.date = datetime.utcnow()
