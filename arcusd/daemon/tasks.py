import os

from .celery_app import app
from ..models.operationinfo import OpInfo
from ..models.enums.optype import OperationType
from ..models.enums.opstatus import OperationStatus
from arcus.client import Client


ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


use_arcus_sandbox = os.environ.get('ARCUS_USE_SANDBOX') == 'true'


client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY,
                sandbox=use_arcus_sandbox)


@app.task
def topup(biller_id: int, phone_number: str,
          amount: float, currency: str = 'MXN') -> OpInfo:
    op_info = OpInfo(OperationType.TOPUP)
    try:
        topup = client.topups.create(biller_id, phone_number, amount, currency)
        op_info.status = OperationStatus.SUCCESS
        op_info.transaction = topup
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info


@app.task
def query_bill(biller_id: int, account_number: str) -> OpInfo:
    op_info = OpInfo(OperationType.QUERY)
    try:
        bill = client.bills.create(biller_id, account_number)
        op_info.status = OperationStatus.SUCCESS
        op_info.operation = bill
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info


@app.task
def pay_bill(bill_id: int) -> OpInfo:
    op_info = OpInfo(OperationType.PAYMENT)
    try:
        bill = client.bills.get(bill_id)
        transaction = bill.pay()
        op_info.transaction = transaction
        op_info.status = OperationStatus.SUCCESS
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info


@app.task
def pay_bill(biller_id: int, account_number: str) -> OpInfo:
    op_info = OpInfo(OperationType.PAYMENT)
    try:
        bill = client.bills.create(biller_id, account_number)
        transaction = bill.pay()
        op_info.operation = transaction
        op_info.status = OperationStatus.SUCCESS
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info


@app.task
def cancell_transaction(transaction_id: int) -> OpInfo:
    op_info = OpInfo(OperationType.PAYMENT)
    try:
        cancellation = client.transactions.cancel(transaction_id)
        transaction = client.transactions.get(transaction_id)
        op_info.operation = transaction
        op_info.status = OperationStatus.SUCCESS
    except Exception as exc:
        op_info.status = OperationStatus.FAILED
        op_info.error_message = exc.message
    return op_info

