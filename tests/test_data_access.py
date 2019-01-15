from arcusd.data_access import tasks
from uuid import uuid4


def test_save_task_info():
    task_id = str(uuid4())
    task_info = dict(
        task_id=task_id,
        task_name='arcusd.tasks.mytask',
    )
    tasks.save_task_info(task_info)
    db_task_info = tasks.get_task_info({'task_id': task_id})
    assert db_task_info['task_id'] == task_id


def test_update_task_info():
    task_id = str(uuid4())
    task_info1 = dict(
        task_id=task_id,
        task_name='arcusd.tasks.mytask',
    )
    tasks.save_task_info(task_info1)
    task_info2 = dict(
        task_result='task_result',
        op_info={
            'prop1': 123234,
            'prop2': 'abcdf'
        }
    )
    tasks.update_task_info({'task_id': task_id}, task_info2)
    db_task_info = tasks.get_task_info({'task_id': task_id})
    assert db_task_info['task_id'] == task_info1['task_id']
    assert db_task_info['task_name'] == task_info1['task_name']
    assert db_task_info['task_result'] == task_info2['task_result']
    assert db_task_info['op_info']['prop1'] == task_info2['op_info']['prop1']
    assert db_task_info['op_info']['prop2'] == task_info2['op_info']['prop2']
