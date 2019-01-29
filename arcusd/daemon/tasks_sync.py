import arcusd
from .celery_app import app
from .utils import execute_op, mapping
from ..types import OperationType


@app.task
def query_bill(service_provider_code: str, account_number: str) -> dict:
    op_info = execute_op(None, OperationType.query,
                         arcusd.arcusactions.query_bill,
                         mapping(service_provider_code), account_number,
                         send_callback=False)
    return op_info.to_dict()
