from arcusd.callbacks import CallbackHelper
from arcusd.contracts import Bill, OpInfo, Transaction
from arcusd import OperationStatus, OperationType


def test_callbackhelper_send_message():
    op_info = OpInfo(OperationType.topup, OperationStatus.success)
    op_info.operation = Transaction(
        id=1010101,
        amount=550000,
        currency='MXN',
        transaction_fee=500,
        hours_to_fulfill=10,
        status='fulfilled'
    )
    CallbackHelper.send_op_result(op_info)
