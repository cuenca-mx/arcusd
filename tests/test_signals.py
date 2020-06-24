from unittest.mock import Mock

from arcusd.contracts import OpInfo
from arcusd.daemon.arcusd_signals import task_after_run, task_before_run
from arcusd.data_access.tasks import get_task_info
from arcusd.types import OperationStatus, OperationType


def test_task_before_run():
    request_id = 'abcedfg'
    task_id = '123456789'
    task = Mock()
    task.request.origin = 'test-origin'
    task.request.args = None
    task.request.kwargs = {
        'a': 'a',
        'b': 1,
        'request_id': request_id,
    }
    task.request.retries = 0
    task_before_run(task_id, task)
    task_info = get_task_info({'request_id': request_id})
    assert task_info['request_id'] == request_id


def test_task_after_run():
    request_id = 'abcedfg'
    task_id = '123456789'
    task = Mock()
    task.request.origin = 'test-origin'
    task.request.args = None
    task.request.kwargs = {
        'a': 'a',
        'b': 1,
        'request_id': request_id,
    }
    task.request.retries = 0
    task.request.state = 'SUCCESS'
    task.request.eta = None
    op_info = OpInfo(request_id, OperationType.topup, OperationStatus.success)
    task_after_run(task_id, task, op_info, 'SUCCESS')
    task_info = get_task_info({'request_id': request_id})
    assert task_info['request_id'] == request_id
    assert 'task_state' in task_info
    assert 'task_eta' in task_info
    assert 'task_retval' in task_info
