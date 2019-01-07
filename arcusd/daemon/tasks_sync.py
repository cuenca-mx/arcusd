import arcusd
from .celery_app import app
from .utils import execute_op
from ..types import OperationType


@app.task
def query_bill(biller_id: int, account_number: str) -> dict:
    op_info = execute_op(None, OperationType.query,
                         arcusd.arcusactions.query_bill, biller_id,
                         account_number, send_callback=False)
    return op_info.to_dict()
