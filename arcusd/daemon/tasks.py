from typing import Optional

from .celery_app import app
from .utils import execute_op
from ..types import OperationType
import arcusd.arcusactions


@app.task
def topup(request_id: str, biller_id: int, phone_number: str,
          amount: int, currency: str = 'MXN',
          name_on_account: Optional[str] = None):
    execute_op(request_id, OperationType.topup, arcusd.arcusactions.topup,
               biller_id, phone_number, amount, currency, name_on_account)


@app.task
def query_bill(request_id: str, biller_id: int, account_number: str):
    execute_op(request_id, OperationType.query, arcusd.arcusactions.query_bill,
               biller_id, account_number)


@app.task
def pay_bill_id(request_id: str, bill_id: int):
    execute_op(request_id, OperationType.payment,
               arcusd.arcusactions.pay_bill_id, bill_id)


@app.task
def pay_bill(request_id: str, biller_id: int, account_number: str):
    execute_op(request_id, OperationType.payment, arcusd.arcusactions.pay_bill,
               biller_id, account_number)


@app.task
def cancel_transaction(request_id: str, transaction_id: int):
    execute_op(request_id, OperationType.payment,
               arcusd.arcusactions.cancel_transaction, transaction_id)
