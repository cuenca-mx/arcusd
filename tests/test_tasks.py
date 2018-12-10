import pytest

from arcusd.models.enums.opstatus import OperationStatus
from arcusd.models.enums.optype import OperationType
from arcusd.daemon.tasks import (
    topup, query_bill, pay_bill, cancel_transaction)


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_query_bill():
    op_info = query_bill(40, '501000000007')
    assert op_info.status == OperationStatus.SUCCESS
    assert op_info.type == OperationType.QUERY
    assert op_info.operation.account_number == '501000000007'
    assert type(op_info.operation.balance) is float


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize('biller_id,account_number,expected_message', [
    (40, '501000000004', 'Invalid Account Number'),
    (6900, '1111362009', 'Unexpected error'),
    (2901, '1111322016', 'Failed to make the consult, please try again later'),
    (1821,
     '1111992022', 'Biller maintenance in progress, please try again later')
])
def test_query_bill_failed(biller_id, account_number, expected_message):
    op_info = query_bill(biller_id, account_number)
    assert op_info.type == OperationType.QUERY
    assert op_info.status == OperationStatus.FAILED
    assert (op_info.error_message == expected_message
            or op_info.error_message.startswith(expected_message))


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment():
    op_info = pay_bill(40, '501000000007')
    assert op_info.type == OperationType.PAYMENT
    assert op_info.status == OperationStatus.SUCCESS
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_failed_payment():
    op_info = pay_bill(37, '2424240024')
    assert op_info.type == OperationType.PAYMENT
    assert op_info.status == OperationStatus.FAILED


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_topup():
    op_info = topup(13599, '5599999999', 100.0, 'MXN')
    assert op_info.type == OperationType.TOPUP
    assert op_info.status == OperationStatus.SUCCESS


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize('phone_number,amount,expected_message', [
    ('559999', 100.0, 'Invalid Phone Number'),
    ('5599999999', 93.3, 'Invalid Payment Amount')
])
def test_failed_topup(phone_number, amount, expected_message):
    op_info = topup(13599, phone_number, amount, 'MXN')
    assert op_info.type == OperationType.TOPUP
    assert op_info.status == OperationStatus.FAILED
    assert op_info.error_message == expected_message


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_cancel_bill():
    pay_op_info = pay_bill(35, '123456851236')
    cancel_op_info = cancel_transaction(pay_op_info.operation.id)
    assert cancel_op_info.status == OperationStatus.SUCCESS
    assert cancel_op_info.operation.id == pay_op_info.operation.id
    assert cancel_op_info.operation.status == 'refunded'
