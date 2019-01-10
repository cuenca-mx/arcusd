from unittest.mock import patch
import pytest

import arcusd.arcusactions
from arcusd.daemon.tasks import (cancel_transaction, pay_bill, pay_bill_id,
                                 query_bill, topup)
from arcusd.types import OperationStatus, OperationType


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_query_bill(callback_helper):
    request_id = 'request-id'
    query_bill(request_id, 40, '501000000007')
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.status == OperationStatus.success
    assert op_info.tran_type == OperationType.query
    assert op_info.operation.account_number == '501000000007'
    assert type(op_info.operation.balance) is int


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize('biller_id,account_number,expected_message', [
    (40, '501000000004', '501000000004 is an invalid account_number'),
    (6900, '1111362009', 'Unexpected error'),
    (2901, '1111322016', 'Failed to make the consult, please try again later'),
    (1821,
     '1111992022', 'Biller maintenance in progress, please try again later')
])
@patch('arcusd.callbacks.CallbackHelper.send_op_result')
def test_query_bill_failed(callback_helper, biller_id, account_number,
                           expected_message):
    request_id = 'request-id'
    query_bill(request_id, biller_id, account_number)
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.query
    assert op_info.status == OperationStatus.failed
    assert (op_info.error_message == expected_message
            or op_info.error_message.startswith(expected_message))


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment(callback_helper):
    request_id = 'request-id'
    pay_bill(request_id, 40, '501000000007')
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment_bill_id(callback_helper):
    request_id = 'request-id'
    bill = arcusd.arcusactions.query_bill(40, '501000000007')
    pay_bill_id(request_id, bill.id)
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_failed_payment(callback_helper):
    request_id = 'request-id'
    pay_bill(request_id, 37, '2424240024')
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.failed


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_topup(callback_helper):
    request_id = 'request-id'
    topup(request_id, 13599, '5599999999', 10000, 'MXN')
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.success
    assert op_info.operation.amount == 10000
    assert op_info.operation.currency == 'MXN'
    assert (op_info.operation.starting_balance >
            op_info.operation.ending_balance)


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize('phone_number,amount,expected_message', [
    ('559999', 10000, 'Invalid Phone Number'),
    ('5599999999', 9330, 'Invalid Payment Amount')
])
@patch('arcusd.callbacks.CallbackHelper.send_op_result')
def test_failed_topup(callback_helper, phone_number, amount, expected_message):
    request_id = 'request-id'
    topup(request_id, 13599, phone_number, amount, 'MXN')
    assert callback_helper.called
    op_info = callback_helper.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.failed
    assert op_info.error_message == expected_message


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_cancel_bill(callback_helper):
    request_id = 'request-id'
    transaction = arcusd.arcusactions.pay_bill(35, '123456851236')
    cancel_transaction(request_id, transaction.id)
    assert callback_helper.called
    cancel_op_info = callback_helper.call_args[0][0]
    assert cancel_op_info.status == OperationStatus.success
    assert cancel_op_info.operation.transaction_id == transaction.id
    assert cancel_op_info.operation.code == 'R0'
