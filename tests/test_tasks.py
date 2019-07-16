from unittest.mock import patch
import pytest

import arcusd.arcusactions
from arcusd.daemon.tasks import (cancel_transaction, pay_bill, pay_bill_id,
                                 query_bill, topup)
from arcusd.exc import UnknownServiceProvider
from arcusd.types import OperationStatus, OperationType

SEND_OP_RESULT = 'arcusd.callbacks.CallbackHelper.send_op_result'


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_query_bill(send_op_result):
    request_id = 'request-id'
    query_bill(request_id, 'satellite_tv_sky', '501000000007')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.status == OperationStatus.success
    assert op_info.tran_type == OperationType.query
    assert op_info.operation.account_number == '501000000007'
    assert type(op_info.operation.balance) is int


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize(
    'service_provider_code,account_number,expected_message', [
        ('satellite_tv_sky', '501000000004',
         '501000000004 is an invalid account_number'),
        ('cable_izzi', '1111362009', 'Unexpected error'),
        ('invoice_att', '1111322016',
         'Failed to make the consult, please try again later'),
        ('cable_megacable', '1111992022',
         'Biller maintenance in progress, please try again later')
    ])
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
def test_query_bill_failed(send_op_result,
                           service_provider_code,
                           account_number,
                           expected_message):
    request_id = 'request-id'
    query_bill(request_id, service_provider_code, account_number)
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.query
    assert op_info.status == OperationStatus.failed
    assert (op_info.error_message == expected_message
            or op_info.error_message.startswith(expected_message))


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment(send_op_result):
    request_id = 'request-id'
    pay_bill(request_id, 'satellite_tv_sky', '501000000007')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment_with_amount(send_op_result):
    request_id = 'request-id'
    pay_bill(request_id, 'satellite_tv_sky', '501000000007', 57000)
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_payment_bill_id(send_op_result):
    request_id = 'request-id'
    bill = arcusd.arcusactions.query_bill(40, '501000000007')
    pay_bill_id(request_id, bill.id)
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_failed_payment(send_op_result):
    request_id = 'request-id'
    pay_bill(request_id, 'internet_telmex', '2424240024')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.failed


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_failed_payment_exception_400(send_op_result):
    request_id = 'request-id'
    pay_bill(request_id, 'internet_telmex', '2424240024')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.failed


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_topup(send_op_result):
    request_id = 'request-id'
    topup(request_id, 'topup_att', '5599999999', 10000, 'MXN')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.success
    assert op_info.operation.amount == 10000
    assert op_info.operation.currency == 'MXN'
    assert (op_info.operation.starting_balance >
            op_info.operation.ending_balance)


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_topup(send_op_result):
    request_id = 'request-id'
    topup(request_id, 'topup_att', '5599999999', 10000, 'MXN')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.success
    assert op_info.operation.amount == 10000
    assert op_info.operation.currency == 'MXN'
    assert (op_info.operation.starting_balance >
            op_info.operation.ending_balance)


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_successful_invoice_with_name_on_account(send_op_result):
    request_id = 'request-id'
    topup(request_id, 'internet_axtel', '5599999999', 35000, 'MXN',
          'Billy R. Rosemond')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.success
    assert op_info.operation.amount == 35000
    assert op_info.operation.currency == 'MXN'
    assert (op_info.operation.starting_balance >
            op_info.operation.ending_balance)


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
@pytest.mark.parametrize('phone_number,amount,expected_message', [
    ('559999', 10000, 'Invalid Phone Number'),
    ('5599999999', 9330, 'Invalid Payment Amount')
])
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
def test_failed_topup(send_op_result, phone_number, amount, expected_message):
    request_id = 'request-id'
    topup(request_id, 'topup_att', phone_number, amount, 'MXN')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.topup
    assert op_info.status == OperationStatus.failed
    assert op_info.error_message == expected_message


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_cancel_bill(send_op_result):
    request_id = 'request-id'
    cfe_arcus_id = 35
    transaction = arcusd.arcusactions.pay_bill(cfe_arcus_id, '123456851236')
    cancel_transaction(request_id, transaction.id)
    assert send_op_result.called
    cancel_op_info = send_op_result.call_args[0][0]
    assert cancel_op_info.status == OperationStatus.success
    assert cancel_op_info.operation.transaction_id == transaction.id
    assert cancel_op_info.operation.code == 'R0'


def test_invalid_service_provider():
    with pytest.raises(UnknownServiceProvider) as exc:
        query_bill('abcdfeghijoklmn', 'fake-provider', '501000000007')
    assert exc.value.message == 'Unknown service provider: fake-provider'


@patch(SEND_OP_RESULT, side_effect=ConnectionError())
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks')
def test_send_operation_result_callback_failed_with_connection_error(
        send_op_result):
    request_id = 'request-id'
    pay_bill(request_id, 'satellite_tv_sky', '501000000007')
    assert send_op_result.called
    op_info = send_op_result.call_args[0][0]
    assert op_info.request_id == request_id
    assert op_info.tran_type == OperationType.payment
    assert op_info.status == OperationStatus.success
    assert type(op_info.operation.id) is int
    assert op_info.operation.status == 'fulfilled'
