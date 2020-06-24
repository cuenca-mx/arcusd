from .contract import Contract


class Bill(Contract):
    def __init__(
        self,
        id: int,
        service_provider_code: int,
        account_number: str,
        balance: int,
        currency: str,
    ):
        self.id = id
        self.service_provider_code = service_provider_code
        self.account_number = account_number
        self.balance = balance
        self.currency = currency
