from sentry_sdk import capture_exception

from requests import HTTPError
from arcus.exc import ArcusException
from ..callbacks import CallbackHelper
from ..contracts.operationinfo import OpInfo
from ..data_access.tasks import update_task_info
from ..exc import UnknownServiceProvider
from ..types import OperationStatus, OperationType, ServiceProvider


def execute_op(request_id: str, op_type: OperationType, funct,
               *args, **kwargs) -> OpInfo:
    op_info = OpInfo(request_id, op_type)
    try:
        transaction = funct(*args)
    except (ArcusException, HTTPError) as exc:
        op_info.status = OperationStatus.failed
        if hasattr(exc, 'message'):
            op_info.error_message = exc.message
        else:
            op_info.error_message = format(exc)
        capture_exception(exc)
    else:
        op_info.operation = transaction
        op_info.status = OperationStatus.success
    update_task_info({'request_id': request_id},
                     {'op_info': op_info.to_dict()})
    if kwargs.get('send_callback', True):
        try:
            resp = CallbackHelper.send_op_result(op_info)
        except ConnectionError:
            resp = {'status': 'failed: ConnectionError'}
        finally:
            update_task_info({'request_id': request_id},
                             {'callback_response': resp})
    return op_info


def mapping(service_provider: str) -> int:
    if service_provider in ServiceProvider.__members__:
        return ServiceProvider[service_provider].value
    else:
        raise UnknownServiceProvider(service_provider)
