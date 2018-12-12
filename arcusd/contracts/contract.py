from enum import Enum


class Contract:
    def to_dict(self):
        contract_dict = self.__dict__.copy()
        for key, value in contract_dict.items():
            if type(value) in (int, str, bool, dict, list, Enum):
                continue
            if isinstance(value, Enum):
                continue
            if not hasattr(value, 'to_dict'):
                continue
            contract_dict[key] = value.to_dict()
        return contract_dict
