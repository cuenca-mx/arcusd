from unittest.mock import patch

import pytest

from arcusd.daemon.tasks_sync import query_bill
from arcusd.types import OperationStatus, OperationType

SEND_OP_RESULT = 'arcusd.callbacks.CallbackHelper.send_op_result'


@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks_sync')
def test_query_bill_sync(send_op_result):
    op_info = query_bill('satellite_tv_sky', '501000000007')
    assert op_info['status'] == OperationStatus.success.value
    assert op_info['tran_type'] == OperationType.query.value
    assert op_info['operation']['account_number'] == '501000000007'
    assert type(op_info['operation']['balance']) is int
    assert not send_op_result.called


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks_sync')
@pytest.mark.parametrize(
    'service_provider_code,account_number,expected_message',
    [
        (
            'satellite_tv_sky',
            '501000000004',
            '501000000004 is an invalid account_number',
        ),
        ('cable_izzi', '1111362009', 'Unexpected error'),
        (
            'invoice_att',
            '1111322016',
            'Failed to make the consult, please try again later',
        ),
        (
            'cable_megacable',
            '1111992022',
            'Biller maintenance in progress, please try again later',
        ),
    ],
)
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
def test_query_bill_failed_sync(
    send_op_result, service_provider_code, account_number, expected_message
):
    op_info = query_bill(service_provider_code, account_number)
    assert op_info['tran_type'] == OperationType.query.value
    assert op_info['status'] == OperationStatus.failed.value
    assert op_info['error_message'] == expected_message or op_info[
        'error_message'
    ].startswith(expected_message)
    assert not send_op_result.called
