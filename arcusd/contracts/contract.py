from enum import Enum

EXCLUDED_TYPES = (int, str, bool, dict, Enum)


def filter_item(item):
    return item if type(item) in EXCLUDED_TYPES else item.to_dict()


class Contract:
    def to_dict(self):
        contract_dict = self.__dict__.copy()
        for key, value in contract_dict.items():
            if type(value) in EXCLUDED_TYPES:
                continue
            if type(value) is list:
                contract_dict[key] = [filter_item(item)
                                      for item in contract_dict[key]]
            if isinstance(value, Enum):
                continue
            if not hasattr(value, 'to_dict'):
                continue
            contract_dict[key] = value.to_dict()
        return contract_dict
