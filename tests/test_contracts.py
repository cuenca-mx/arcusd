import json
import datetime
from arcusd.contracts.contract import Contract


class FooClass(Contract):
    def __init__(self, a: int, b: str):
        self.a = a
        self.b = b


class BarClass(Contract):
    def __init__(self, x: list, y: float, z: FooClass, date: datetime):
        self.x = x
        self.y = y
        self.z = z
        self.date = date


def test_to_dict():
    foo = FooClass(100, 'fooclass')
    bar = BarClass([1, 2, foo], 500.80, foo, datetime.datetime.now())
    test_dict = bar.to_dict()
    json_str = json.dumps(test_dict)
    assert 'x' in test_dict
    assert type(test_dict['x']) is list
    assert 'y' in test_dict
    assert 'z' in test_dict
    assert type(test_dict['z']) is dict
    assert type(test_dict['x'][2]) is dict
    assert json_str is not None
