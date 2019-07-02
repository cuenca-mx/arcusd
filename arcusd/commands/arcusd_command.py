import click

from arcusd import OperationType
from arcusd.callbacks import CallbackHelper
from arcusd.contracts import OpInfo
from arcusd.data_access.tasks import get_task_info, update_task_info


@click.command()
@click.argument('transaction_id', type=str)
@click.argument('status', type=str)
def change_status(transaction_id: str, status: str) -> None:
    """Script to set the status of a transaction on the db"""

    task = get_task_info(dict(request_id=transaction_id))
    if task is None:
        click.echo(f'transaction id {transaction_id} does not exists')
        return
    if 'op_info' in task:
        click.echo('tasks was successfully handled')
    else:

        if status == 'success':

            id_value = click.prompt('please enter arcus id: ', type=str)
            amount = click.prompt('please enter amount paid: ', type=str)
            update_task_info(dict(request_id=transaction_id), dict(
                op_info=dict(
                    request_id=transaction_id,
                    tran_type='payment',
                    status=status,
                    operation=dict(
                        id=id_value,
                        amount=amount,
                        currency='MXN'
                    )
                )
            ))
        else:
            update_task_info(dict(request_id=transaction_id), dict(
                op_info=dict(
                    request_id=transaction_id,
                    tran_type='payment',
                    status=status
                )))
        try:
            CallbackHelper.send_op_result(OpInfo(transaction_id,
                                                 OperationType.payment,
                                                 status))
        except ConnectionError:
            click.echo('connection error try again')
