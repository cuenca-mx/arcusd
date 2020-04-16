from typing import Optional

import newrelic.agent

import arcusd.arcusactions
from arcusd.data_access.providers_mapping import get_biller_id
from .celery_app import app
from .utils import execute_op
from ..types import OperationType


@app.task
@newrelic.agent.background_task()
def topup(request_id: str, service_provider_code: str, phone_number: str,
          amount: int, currency: str = 'MXN',
          name_on_account: Optional[str] = None):
    execute_op(request_id, OperationType.topup,
               arcusd.arcusactions.bill_payments,
               get_biller_id(service_provider_code), phone_number, amount,
               currency, name_on_account)


@app.task
@newrelic.agent.background_task()
def query_bill(request_id: str, service_provider_code: str,
               account_number: str):
    execute_op(request_id, OperationType.query, arcusd.arcusactions.query_bill,
               get_biller_id(service_provider_code), account_number)


@app.task
@newrelic.agent.background_task()
def pay_bill_id(request_id: str, bill_id: int):
    execute_op(request_id, OperationType.payment,
               arcusd.arcusactions.pay_bill_id, bill_id)


@app.task
@newrelic.agent.background_task()
def pay_bill(request_id: str, service_provider_code: str, account_number: str,
             amount: Optional[int] = None):
    execute_op(request_id, OperationType.payment, arcusd.arcusactions.pay_bill,
               get_biller_id(service_provider_code), account_number,
               amount)


@app.task
@newrelic.agent.background_task()
def cancel_transaction(request_id: str, transaction_id: int):
    execute_op(request_id, OperationType.payment,
               arcusd.arcusactions.cancel_transaction, transaction_id)
