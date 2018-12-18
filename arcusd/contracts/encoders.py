import datetime as dt
import json
from enum import Enum


class ContractEncoder(json.JSONEncoder):

    def default(self, obj):
        try:
            super().default(obj)
        except TypeError as exc:
            if isinstance(obj, Enum):
                encoded = obj.value
            elif isinstance(obj, dt.datetime):
                encoded = obj.isoformat() + 'Z'
            elif hasattr(obj, 'to_dict'):
                encoded = obj.to_dict()
            else:
                raise exc
        return encoded
