import os
import re
from typing import Optional

from arcus.client import Client
from arcus.client import Transaction as ArcusTransaction
from arcus.exc import InvalidAmount

from arcusd.contracts import Bill, Cancellation, Payment, Transaction
from arcusd.data_access.providers_mapping import get_service_provider_code

ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']
TOPUP_BILLERS = [int(biller_id) for biller_id in
                 os.environ['TOPUP_BILLERS'].split(',')]

use_arcus_sandbox = os.environ.get('ARCUS_USE_SANDBOX') == 'true'

client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY,
                sandbox=use_arcus_sandbox)


def cents_to_unit(cents: int) -> float:
    return cents / 100


def unit_to_cents(unit: float) -> int:
    return int(unit * 100)


def clean(value: str) -> str:
    return re.sub(r'[\W_]+', '', value)


def amount_to_unit(cents: int) -> float:
    if cents <= 100:
        raise InvalidAmount(code='00', message='Min amount is 1 peso')
    return cents_to_unit(cents)


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
        amount = amount_to_unit(amount)
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
    transaction = ArcusTransaction(
        id=transaction_id, amount=0, amount_currency='',
        transaction_fee=0, hours_to_fulfill=0, created_at='',
        status='', type='', fx_rate=0, amount_usd=0, total_usd=0)
    arcus_cancellation = transaction.cancel()
    cancellation = Cancellation(
        transaction_id=transaction_id,
        code=arcus_cancellation['code'],
        message=arcus_cancellation['message'],
    )
    return cancellation


def bill_payments(biller_id: int, account_number: str, amount: int,
                  currency: str, name_on_account: str) -> Payment:
    unit = amount_to_unit(amount)
    use_topup_creds = biller_id in TOPUP_BILLERS
    payment = client.bill_payments.create(biller_id,
                                          clean(account_number),
                                          unit,
                                          currency,
                                          name_on_account,
                                          topup=use_topup_creds)
    payment_contract = Payment(
        id=payment.id,
        service_provider_code=get_service_provider_code(biller_id),
        account_number=payment.account_number,
        amount=unit_to_cents(payment.bill_amount),
        currency=payment.bill_amount_currency,
        payment_transaction_fee=unit_to_cents(payment.payment_transaction_fee),
        payment_total=unit_to_cents(payment.payment_total_chain_currency),
        chain_earned=unit_to_cents(payment.chain_earned),
        chain_paid=unit_to_cents(payment.chain_paid),
        starting_balance=unit_to_cents(payment.starting_balance),
        ending_balance=unit_to_cents(payment.ending_balance),
        hours_to_fulfill=payment.hours_to_fulfill,
        ticket_text=payment.ticket_text
    )
    return payment_contract
