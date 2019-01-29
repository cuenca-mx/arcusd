from .contract import Contract


class Topup(Contract):

    def __init__(self,
                 id: int,
                 service_provider_code: int,
                 account_number: str,
                 amount: int,
                 currency: str,
                 payment_transaction_fee: int,
                 payment_total: int,
                 chain_earned: int,
                 chain_paid: int,
                 starting_balance: int,
                 ending_balance: int,
                 hours_to_fulfill: int,
                 ticket_text: str):
        self.id = id
        self.service_provider_code = service_provider_code
        self.account_number = account_number
        self.amount = amount
        self.currency = currency
        self.payment_transaction_fee = payment_transaction_fee
        self.payment_total = payment_total
        self.chain_earned = chain_earned
        self.chain_paid = chain_paid
        self.starting_balance = starting_balance
        self.ending_balance = ending_balance
        self.hours_to_fulfill = hours_to_fulfill
        self.ticket_text = ticket_text
