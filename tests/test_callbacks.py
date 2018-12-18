import pytest
from requests.exceptions import ConnectionError
from arcusd.callbacks import CallbackHelper
from arcusd.contracts import OpInfo, Transaction
from arcusd import OperationStatus, OperationType


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_callbacks')
def test_callbackhelper_send_message_success():
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


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_callbacks')
def test_callbackhelper_send_message_connection_error():
    op_info = OpInfo(OperationType.topup, OperationStatus.success)
    op_info.operation = Transaction(
        id=1010101,
        amount=550000,
        currency='MXN',
        transaction_fee=500,
        hours_to_fulfill=10,
        status='fulfilled'
    )
    with pytest.raises(ConnectionError):
        CallbackHelper.send_op_result(op_info)
