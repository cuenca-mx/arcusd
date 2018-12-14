import requests
import os

from .contracts.operationinfo import OpInfo

ARCUSD_CALLBACK_URL = os.environ['ARCUSD_CALLBACK_URL']


class CallbackHelper:

    @classmethod
    def send_op_result(cls, op_info: OpInfo):
        try:
            requests.post(ARCUSD_CALLBACK_URL, json=op_info.to_dict())
        except Exception as exc:
            print(exc)
