import newrelic.agent

import arcusd
from arcusd.data_access.providers_mapping import get_biller_id

from ..types import OperationType
from .celery_app import app
from .utils import execute_op


@app.task
@newrelic.agent.background_task()
def query_bill(service_provider_code: str, account_number: str) -> dict:
    op_info = execute_op(
        None,
        OperationType.query,
        arcusd.arcusactions.query_bill,
        get_biller_id(service_provider_code),
        account_number,
        send_callback=False,
    )
    return op_info.to_dict()
