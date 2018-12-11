import os

from arcus.client import Client
from arcus.resources import Bill, Topup, Transaction

ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


use_arcus_sandbox = os.environ.get('ARCUS_USE_SANDBOX') == 'true'


client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY,
                sandbox=use_arcus_sandbox)


def cents_to_unit(cents: int)-> float:
    return cents/100


def query_bill(biller_id: int, account_number: str) -> Bill:
    return client.bills.create(biller_id, account_number)


def pay_bill_id(bill_id: int) -> Transaction:
    bill = client.bills.get(bill_id)
    return bill.pay()


def pay_bill(biller_id: int, account_number: str) -> Transaction:
    bill = client.bills.create(biller_id, account_number)
    return bill.pay()


def cancel_transaction(transaction_id: int) -> Transaction:
    cancelation = client.transactions.cancel(transaction_id)
    return client.transactions.get(transaction_id)


def topup(biller_id: int, phone_number: str, amount: int,
          currency='MXN') -> Topup:
    unit = cents_to_unit(amount)
    return client.topups.create(biller_id, phone_number, unit, currency)
