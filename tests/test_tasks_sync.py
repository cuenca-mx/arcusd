from unittest.mock import patch
import pytest

from arcusd.daemon.tasks_sync import query_bill
from arcusd.types import OperationStatus, OperationType


@patch('arcusd.callbacks.CallbackHelper.send_op_result')
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks_sync')
def test_query_bill_sync(callback_helper):
    op_info = query_bill(40, '501000000007')
    assert op_info['status'] == OperationStatus.success.value
    assert op_info['tran_type'] == OperationType.query.value
    assert op_info['operation']['account_number'] == '501000000007'
    assert type(op_info['operation']['balance']) is int
    assert not callback_helper.called


@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_tasks_sync')
@pytest.mark.parametrize('biller_id,account_number,expected_message', [
    (40, '501000000004', 'Invalid Account Number'),
    (6900, '1111362009', 'Unexpected error'),
    (2901, '1111322016', 'Failed to make the consult, please try again later'),
    (1821,
     '1111992022', 'Biller maintenance in progress, please try again later')
])
@patch('arcusd.callbacks.CallbackHelper.send_op_result')
def test_query_bill_failed_sync(callback_helper, biller_id, account_number,
                                expected_message):
    op_info = query_bill(biller_id, account_number)
    assert op_info['tran_type'] == OperationType.query.value
    assert op_info['status'] == OperationStatus.failed.value
    assert (op_info['error_message'] == expected_message
            or op_info['error_message'].startswith(expected_message))
    assert not callback_helper.called
