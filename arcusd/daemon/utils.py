from sentry_sdk import capture_exception

from ..callbacks import CallbackHelper
from ..contracts.operationinfo import OpInfo
from ..data_access.tasks import update_task_info
from ..types import OperationStatus, OperationType


def execute_op(request_id: str, op_type: OperationType, funct,
               *args, **kwargs) -> OpInfo:
    op_info = OpInfo(request_id, op_type)
    try:
        transaction = funct(*args)
    except Exception as exc:
        op_info.status = OperationStatus.failed
        op_info.error_message = exc.message
        capture_exception(exc)
    else:
        op_info.operation = transaction
        op_info.status = OperationStatus.success
    if kwargs.get('send_callback', True):
        CallbackHelper.send_op_result(op_info)
    update_task_info({'request_id': request_id},
                     {'op_info': op_info.to_dict()})
    return op_info
