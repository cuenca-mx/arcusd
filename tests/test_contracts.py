import json

from arcusd.contracts import OpInfo, Transaction
from arcusd.types import OperationStatus, OperationType


def test_to_dict():
    transaction = Transaction(
        id=987765,
        amount=1599900,
        currency='MXN',
        transaction_fee=1000,
        hours_to_fulfill=0,
        status='success'
    )
    op_info = OpInfo(
        tran_type=OperationType.payment,
        status=OperationStatus.success,
        operation=transaction
    )
    op_info.operation = transaction
    op_info_dict = op_info.to_dict()
    json_str = json.dumps(op_info_dict)
    assert json_str is not None
    assert 'tran_type' in op_info_dict
    assert 'status' in op_info_dict
    assert 'operation' in op_info_dict
    assert 'error_message' in op_info_dict
    assert op_info_dict['tran_type'] == 'payment'
    assert op_info_dict['status'] == 'success'
    assert 'id' in op_info_dict['operation']
    assert 'amount' in op_info_dict['operation']
    assert 'currency' in op_info_dict['operation']
    assert 'status' in op_info_dict['operation']
