import arcusd
from .celery_app import app
from .utils import execute_op
from ..contracts.operationinfo import OpInfo
from ..types import OperationType


@app.task
def query_bill(biller_id: int, account_number: str) -> OpInfo:
    return execute_op(OperationType.query, arcusd.arcusactions.query_bill,
                      biller_id, account_number, send_callback=False)
