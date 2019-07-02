import pytest
from click import prompt
from click.testing import CliRunner
from arcusd.commands.arcusd_command import change_status
from arcusd.data_access.tasks import save_task_info, update_task_info, \
    get_task_info
from arcusd.types import ServiceProvider
from arcusd.daemon.tasks import pay_bill
from unittest.mock import patch

SEND_OP_RESULT = 'arcusd.callbacks.CallbackHelper.send_op_result'


def test_id_doesnt_exist():
    request_id = 'request-id'
    task_info = dict(
        task_id='abcdfg',
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    result = runner.invoke(change_status, ['other-id', 'success'])
    assert result.output == 'transaction id other-id does not exists\n'


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_commands')
def test_set_status_failed_and_create_op_info(mock_pay_bill,
                                              mock_send_op_result):
    request_id = 'request-id2'
    task_info = dict(
        task_id='abcdfg',
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    with pytest.raises(Exception):
        pay_bill(request_id, ServiceProvider.internet_telmex.name,
                 '24242ServiceProvider.satellite_tv_sky.value')
    result = runner.invoke(change_status, [request_id, 'failed'])
    assert result.exit_code == 0
    transaction = get_task_info(dict(request_id=request_id))

    assert 'op_info' in transaction
    assert transaction['op_info'] is not None
    assert transaction['op_info']['status'] == 'failed'
    assert mock_send_op_result.called


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT,  side_effect=ConnectionError())
def test_set_status_handles_error(mock_pay_bill,
                                   mock_send_op_result):
    request_id = 'testid'
    task_info = dict(
        task_id='abcdfg',
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    with pytest.raises(Exception):
        pay_bill(request_id, ServiceProvider.internet_telmex.name,
                 '24242ServiceProvider.satellite_tv_sky.value')
    result = runner.invoke(change_status, [request_id, 'failed'])

    get_task_info(dict(request_id=request_id))

    assert result.output == 'connection  error try again\n'

# def test_arcusd_handles_correct_when_property_exist():
#     request_id = 'test-id'
#     task_info = dict(
#         task_id='abcdfg',
#         task_sender='test',
#         request_id=request_id,
#         op_info=dict(abc='abc')
#     )
#     save_task_info(task_info)
#     runner = CliRunner()
#
#     result = runner.invoke(change_status, [request_id, 'success'])
#     task = get_task_info({'request_id': 'test-id'})
#     print(task)
#
#     assert task['op_info']['abc'] == 'abc'
#     assert result.output == 'tasks was successfully handled'

#
# @patch('arcusd.commands.arcusd_command.change_status',
#        side_effect=ConnectionError())
# def test_arcusd_handles_exception(mock_pay_bill):
#     request_id = 'request-id'
#     task_info = dict(
#         task_id='abcdfg',
#         request_id=request_id,
#     )
#     save_task_info(task_info)
#
#     runner = CliRunner()
#
#     result = runner.invoke(change_status, ['request-id', 'success'])
#
#     get_task_info({'request_id': 'request-id'})
#
#     assert result.output == 'connection error, try again'
