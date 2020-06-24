import base64
import json
import os

import requests

from .contracts import ContractEncoder, OpInfo

ARCUSD_CALLBACK_URL = os.environ['ARCUSD_CALLBACK_URL']
ARCUSD_CALLBACK_API_KEY = os.environ['ARCUSD_CALLBACK_API_KEY']
ARCUSD_CALLBACK_SECRET = os.environ['ARCUSD_CALLBACK_SECRET']


def auth_header(username: str, password: str) -> str:
    creds = base64.b64encode(f'{username}:{password}'.encode('ascii')).decode(
        'utf-8'
    )
    return f'Basic {creds}'


class CallbackHelper:
    @classmethod
    def send_op_result(cls, op_info: OpInfo):
        resp = requests.post(
            ARCUSD_CALLBACK_URL,
            data=json.dumps(op_info, cls=ContractEncoder),
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_header(
                    ARCUSD_CALLBACK_API_KEY, ARCUSD_CALLBACK_SECRET
                ),
            },
        )
        return resp.json()
