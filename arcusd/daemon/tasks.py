from .celery_app import app
from .utils import execute_op
from ..types import OperationType
import arcusd.arcusactions


@app.task
def topup(biller_id: int, phone_number: str,
          amount: int, currency: str = 'MXN'):
    execute_op(OperationType.topup, arcusd.arcusactions.topup,
               biller_id, phone_number, amount, currency)


@app.task
def query_bill(biller_id: int, account_number: str):
    execute_op(OperationType.query, arcusd.arcusactions.query_bill, biller_id,
               account_number)


@app.task
def pay_bill_id(bill_id: int):
    execute_op(OperationType.payment, arcusd.arcusactions.pay_bill_id, bill_id)


@app.task
def pay_bill(biller_id: int, account_number: str):
    execute_op(OperationType.payment, arcusd.arcusactions.pay_bill, biller_id,
               account_number)


@app.task
def cancel_transaction(transaction_id: int):
    execute_op(OperationType.payment, arcusd.arcusactions.cancel_transaction,
               transaction_id)
