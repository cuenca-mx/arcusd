from .contract import Contract


class Bill(Contract):

    def __init__(self,
                 id: int,
                 biller_id: int,
                 account_number: str,
                 balance: int,
                 currency: str):
        self.id = id
        self.biller_id = biller_id
        self.account_number = account_number
        self.balance = balance
        self.currency = currency
