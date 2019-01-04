from arcusd.arcusactions import cents_to_unit, unit_to_cents


def test_cents_to_unit():
    assert cents_to_unit(100) == 1.0


def test_unit_to_cents():
    assert unit_to_cents(1.0) == 100
