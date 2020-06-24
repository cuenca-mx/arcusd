from arcusd.arcusactions import cents_to_unit, clean, unit_to_cents


def test_cents_to_unit():
    assert cents_to_unit(100) == 1.0


def test_unit_to_cents():
    assert unit_to_cents(1.0) == 100


def test_clean_phone_number():
    assert clean('(555) 555 5555') == '5555555555'
    assert clean('555-555') == '555555'
    assert clean('555?444') == '555444'
    assert clean('-.-5544MMCCXX**') == '5544MMCCXX'
