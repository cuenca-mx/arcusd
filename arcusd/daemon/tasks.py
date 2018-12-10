import os

from .celery_app import app
from ..models.operationinfo import OpInfo
from ..models.enums.optype import OperationType
from ..models.enums.opstatus import OperationStatus
from arcus.client import Client
from arcus.resources import Transaction


ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


use_arcus_sandbox = os.environ.get('ARCUS_USE_SANDBOX') == 'true'


client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY,
                sandbox=use_arcus_sandbox)


@app.task
def topup(biller_id: int, phone_number: str,
          amount: float, currency: str = 'MXN') -> OpInfo:
    return execute_op(OperationType.TOPUP, client.topups.create, biller_id,
                      phone_number, amount, currency)


@app.task
def query_bill(biller_id: int, account_number: str) -> OpInfo:
    return execute_op(OperationType.QUERY, client.bills.create, biller_id,
                      account_number)


@app.task
def pay_bill(bill_id: int) -> OpInfo:
    def pay(bill_id: int) -> Transaction:
        bill = client.bills.get(bill_id)
        return bill.pay()

    return execute_op(OperationType.PAYMENT, pay, bill_id)


@app.task
def pay_bill(biller_id: int, account_number: str) -> OpInfo:
    def pay(biller_id: int, account_number: str) -> Transaction:
        bill = client.bills.create(biller_id, account_number)
        return bill.pay()

    return execute_op(OperationType.PAYMENT, pay, biller_id, account_number)


@app.task
def cancell_transaction(transaction_id: int) -> OpInfo:
    def cancell(transaction_id: int) -> Transaction:
        cancellation = client.transactions.cancel(transaction_id)
        return client.transactions.get(transaction_id)

    return execute_op(OperationType.PAYMENT, cancell, transaction_id)


def execute_op(op_type: OperationType, funct, *args) -> OpInfo:
    op_info = OpInfo(op_type)
    try:
        transaction = funct(*args)
        op_info.operation = transaction
        op_info.status = OperationStatus.SUCCESS
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info
