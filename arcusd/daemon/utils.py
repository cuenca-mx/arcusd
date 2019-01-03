from sentry_sdk import capture_exception

from ..contracts.operationinfo import OpInfo
from ..types import OperationStatus, OperationType
from ..callbacks import CallbackHelper


def execute_op(op_type: OperationType,
               funct, *args, **kwargs) -> OpInfo:
    op_info = OpInfo(op_type)
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
    return op_info
