from datetime import datetime

from celery.signals import task_postrun, task_prerun

from arcusd.contracts import Contract
from arcusd.data_access.tasks import save_task_info, update_task_info


@task_prerun.connect
def task_before_run(task_id, task, *args, **kwargs):
    request_id = task.request.kwargs.get('request_id', task_id)
    task_info = dict(
        task_id=task_id,
        task_sender=task.request.origin,
        task_args=task.request.args,
        task_kwargs=task.request.kwargs,
        task_retries=task.request.retries,
        task_start=datetime.utcnow(),
        request_id=request_id,
    )
    save_task_info(task_info)


@task_postrun.connect
def task_after_run(task_id, task, retval, state, *args, **kwargs):
    request_id = task.request.kwargs.get('request_id', task_id)
    task_info = dict(
        task_state=state,
        task_eta=task.request.eta,
        task_end=datetime.utcnow(),
    )
    if isinstance(retval, Contract):
        task_info['task_retval'] = retval.to_dict()
    update_task_info({'request_id': request_id}, task_info)
