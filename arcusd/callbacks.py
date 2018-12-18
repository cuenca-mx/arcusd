import json
import requests
import os

from .contracts import ContractEncoder, OpInfo

ARCUSD_CALLBACK_URL = os.environ['ARCUSD_CALLBACK_URL']


class CallbackHelper:

    @classmethod
    def send_op_result(cls, op_info: OpInfo):
        requests.post(
            ARCUSD_CALLBACK_URL,
            data=json.dumps(op_info, cls=ContractEncoder),
            headers={'Content-Type': 'application/json'})
