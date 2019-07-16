import pytest

from click.testing import CliRunner
from unittest.mock import patch

from arcusd.commands.arcusd_command import change_status
from arcusd.daemon.tasks import pay_bill
from arcusd.data_access.tasks import get_task_info, save_task_info
from arcusd.types import ServiceProvider


SEND_OP_RESULT = 'arcusd.callbacks.CallbackHelper.send_op_result'


def test_transaction_id_does_not_exist():
    request_id = 'request-id'
    task_info = dict(
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    result = runner.invoke(change_status, ['other-id', 'success'])
    assert result.output == 'transaction id other-id does not exists\n'


def test_command_donnot_change_status_when_already_refunded():
    request_id = 'testingId'
    task_info = dict(
        request_id=request_id,
        op_info=dict(status='failed')
    )
    save_task_info(task_info)
    runner = CliRunner()
    result = runner.invoke(change_status, [request_id, 'failed'])
    assert result.output == 'transaction was already refunded\n'


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
def test_success_and_create_op_info(mock_pay_bill, mock_send_op_result):
    request_id = 'idtest'
    task_info = dict(
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    with pytest.raises(Exception):
        pay_bill(request_id, ServiceProvider.internet_telmex.name,
                 '24242ServiceProvider.satellite_tv_sky.value')
    result = runner.invoke(
        change_status,
        [request_id, 'success'],
        input='arcus-id\n100')
    assert result.exit_code == 0
    transaction = get_task_info(dict(request_id=request_id))
    assert transaction['op_info']['operation']['amount'] == 100
    assert transaction['op_info']['operation']['id'] == 'arcus-id'


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
@pytest.mark.vcr(cassette_library_dir='tests/cassettes/test_commands')
def test_set_status_failed_creates_op_info(mock_pay_bill,
                                           mock_send_op_result):
    request_id = 'request-id2'
    task_info = dict(
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
    assert transaction['op_info'] is not None
    assert transaction['op_info']['status'] == 'failed'
    assert mock_send_op_result.called


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT, side_effect=ConnectionError())
def test_refund_payment_handles_error(mock_pay_bill, mock_send_op_result):
    request_id = 'testid'
    task_info = dict(
        request_id=request_id,
    )
    save_task_info(task_info)
    runner = CliRunner()
    with pytest.raises(Exception):
        pay_bill(request_id, ServiceProvider.internet_telmex.name,
                 '24242ServiceProvider.satellite_tv_sky.value')
    result = runner.invoke(change_status, [request_id, 'failed'])
    get_task_info(dict(request_id=request_id))
    assert result.output == 'connection error try again\n'


@patch('arcusd.arcusactions.pay_bill', side_effect=Exception('unexpected!'))
@patch(SEND_OP_RESULT, return_value=dict(status='ok'))
def test_command_change_status_already_exists(mock_pay_bill,
                                              mock_send_op_result):
    request_id = 'testingId2'
    task_info = dict(
        request_id=request_id,
        op_info=dict(status='success')
    )
    save_task_info(task_info)
    runner = CliRunner()
    result = runner.invoke(change_status, [request_id, 'failed'])
    assert result.exit_code == 0
    transaction = get_task_info(dict(request_id=request_id))
    assert transaction['op_info']['status'] == 'failed'
