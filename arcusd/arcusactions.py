import os
import re
from typing import Optional

from arcus.client import Client
from arcus.client import Transaction as ArcusTransaction

from arcusd.contracts import Bill, Cancellation, Topup, Transaction
from arcusd.data_access.providers_mapping import get_service_provider_code

ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']

use_arcus_sandbox = os.environ.get('ARCUS_USE_SANDBOX') == 'true'

client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY,
                sandbox=use_arcus_sandbox)


def cents_to_unit(cents: int) -> float:
    return cents / 100


def unit_to_cents(unit: float) -> int:
    return int(unit * 100)


def clean(value: str) -> str:
    return re.sub(r'\D', '', value)


def query_bill(biller_id: int, account_number: str) -> Bill:
    bill = client.bills.create(biller_id, clean(account_number))
    bill_contract = Bill(
        id=bill.id,
        service_provider_code=get_service_provider_code(biller_id),
        account_number=bill.account_number,
        balance=unit_to_cents(bill.balance),
        currency=bill.balance_currency
    )
    return bill_contract


def pay_bill_id(bill_id: int) -> Transaction:
    bill = client.bills.get(bill_id)
    transaction = bill.pay()
    transaction_contract = Transaction(
        id=transaction.id,
        amount=unit_to_cents(transaction.amount),
        currency=transaction.amount_currency,
        transaction_fee=unit_to_cents(transaction.transaction_fee),
        hours_to_fulfill=transaction.hours_to_fulfill,
        status=transaction.status
    )
    return transaction_contract


def pay_bill(biller_id: int, account_number: str,
             amount: Optional[int] = None) -> Transaction:
    bill = client.bills.create(biller_id, clean(account_number))
    if amount is None:
        transaction = bill.pay()
    else:
        amount = cents_to_unit(amount)
        transaction = bill.pay(amount)
    transaction_contract = Transaction(
        id=transaction.id,
        amount=unit_to_cents(transaction.amount),
        currency=transaction.amount_currency,
        transaction_fee=unit_to_cents(transaction.transaction_fee),
        hours_to_fulfill=transaction.hours_to_fulfill,
        status=transaction.status
    )
    return transaction_contract


def cancel_transaction(transaction_id: int) -> Cancellation:
    transaction = ArcusTransaction(transaction_id, 0, '', 0, 0,
                                   '', '', '', 0, 0, 0)
    arcus_cancellation = transaction.cancel()
    cancellation = Cancellation(
        transaction_id=transaction_id,
        code=arcus_cancellation['code'],
        message=arcus_cancellation['message'],
    )
    return cancellation


def topup(biller_id: int, phone_number: str, amount: int,
          currency: str, name_on_account: str) -> Topup:
    unit = cents_to_unit(amount)
    topup = client.topups.create(biller_id,
                                 clean(phone_number),
                                 unit,
                                 currency,
                                 name_on_account)
    topup_contract = Topup(
        id=topup.id,
        service_provider_code=get_service_provider_code(biller_id),
        account_number=topup.account_number,
        amount=unit_to_cents(topup.bill_amount),
        currency=topup.bill_amount_currency,
        payment_transaction_fee=unit_to_cents(topup.payment_transaction_fee),
        payment_total=unit_to_cents(topup.payment_total_chain_currency),
        chain_earned=unit_to_cents(topup.chain_earned),
        chain_paid=unit_to_cents(topup.chain_paid),
        starting_balance=unit_to_cents(topup.starting_balance),
        ending_balance=unit_to_cents(topup.ending_balance),
        hours_to_fulfill=topup.hours_to_fulfill,
        ticket_text=topup.ticket_text
    )
    return topup_contract
