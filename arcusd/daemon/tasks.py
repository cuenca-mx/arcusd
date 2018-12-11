from .celery_app import app
from ..models.operationinfo import OpInfo
from ..types import OperationStatus, OperationType
import arcusd.arcusactions


@app.task
def topup(biller_id: int, phone_number: str,
          amount: int, currency: str = 'MXN') -> OpInfo:
    return execute_op(OperationType.topup, arcusd.arcusactions.topup,
                      biller_id, phone_number, amount, currency)


@app.task
def query_bill(biller_id: int, account_number: str) -> OpInfo:
    return execute_op(OperationType.query, arcusd.arcusactions.query_bill,
                      biller_id, account_number)


@app.task
def pay_bill(bill_id: int) -> OpInfo:
    return execute_op(
        OperationType.payment, arcusd.arcusactions.pay_bill_id, bill_id)


@app.task
def pay_bill(biller_id: int, account_number: str) -> OpInfo:
    return execute_op(OperationType.payment,
                      arcusd.arcusactions.pay_bill, biller_id, account_number)


@app.task
def cancel_transaction(transaction_id: int) -> OpInfo:
    return execute_op(OperationType.payment,
                      arcusd.arcusactions.cancel_transaction, transaction_id)


def execute_op(op_type: OperationType, funct, *args) -> OpInfo:
    op_info = OpInfo(op_type)
    try:
        transaction = funct(*args)
    except Exception as exc:
        op_info.status = OperationStatus.failed
        op_info.error_message = exc.message
    else:
        op_info.operation = transaction
        op_info.status = OperationStatus.success
    return op_info
