from typing import Union

from arcus.exc import ArcusException
from requests import HTTPError
from sentry_sdk import capture_exception

from ..callbacks import CallbackHelper
from ..contracts.operationinfo import OpInfo
from ..data_access.tasks import update_task_info
from ..errors_dict import errors_dict
from ..types import OperationStatus, OperationType


def execute_op(
    request_id: str, op_type: OperationType, funct, *args, **kwargs
) -> OpInfo:
    op_info = OpInfo(request_id, op_type)
    try:
        transaction = funct(*args)
    except (ArcusException, HTTPError) as exc:
        op_info.status = OperationStatus.failed
        op_info.notification = error_interpreter(exc)
        if hasattr(exc, 'message'):
            op_info.error_message = exc.message
        else:
            op_info.error_message = format(exc)
        if not op_info.notification:
            capture_exception(exc)
    else:
        op_info.operation = transaction
        op_info.status = OperationStatus.success
    update_task_info(
        {'request_id': request_id}, {'op_info': op_info.to_dict()}
    )
    if kwargs.get('send_callback', True):
        try:
            resp = CallbackHelper.send_op_result(op_info)
        except ConnectionError:
            resp = {'status': 'failed: ConnectionError'}
        finally:
            update_task_info(
                {'request_id': request_id}, {'callback_response': resp}
            )
    return op_info


def error_interpreter(error: Union[ArcusException, HTTPError]) -> str:
    error_type = type(error)
    notification = errors_dict.get(error_type, None)
    return notification
