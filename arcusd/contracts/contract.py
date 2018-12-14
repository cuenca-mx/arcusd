from enum import Enum
import datetime as dt
import json


class Contract:

    def to_dict(self):
        items = {}
        for key, value in self.__dict__.items():
            try:
                json.dumps(value)
            except TypeError as exc:
                if isinstance(value, Enum):
                    items[key] = value.value
                elif isinstance(value, dt.datetime):
                    items[key] = value.isoformat() + 'Z'
                elif hasattr(value, 'to_dict'):
                    items[key] = value.to_dict()
                else:
                    raise exc
            else:
                items[key] = value
        return items
