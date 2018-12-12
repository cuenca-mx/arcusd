from .contract import Contract


class Transaction(Contract):

    def __init__(self,
                 id: int,
                 amount: int,
                 currency: str,
                 transaction_fee: int,
                 hours_to_fulfill: int,
                 status: str):
        self.id = id
        self.amount = amount
        self.currency = currency
        self.transaction_fee = transaction_fee
        self.hours_to_fulfill = hours_to_fulfill
        self.status = status
