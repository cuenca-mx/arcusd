import click

from arcusd import OperationType
from arcusd.callbacks import CallbackHelper
from arcusd.contracts import OpInfo
from arcusd.data_access.tasks import (
    get_task_info,
    update_insert_task_info,
    update_task_info,
)


@click.group()
def arcusd_cli():
    pass


@arcusd_cli.command()
@click.argument('transaction_id', type=str)
@click.argument('status', type=click.Choice(['success', 'failed']))
def change_status(transaction_id: str, status: str) -> None:
    """If status entered is success it completes op_info
    property on incomplete transactions and refunds
    transactions on failed status"""

    task = get_task_info(dict(request_id=transaction_id))
    if task is None:
        click.echo(f'transaction id {transaction_id} does not exists')
        return
    if 'op_info' in task and task['op_info']['status'] == 'failed':
        click.echo('transaction was already refunded')
        return
    else:
        if status == 'success':
            id_value = click.prompt('please enter arcus id: ', type=str)
            amount = click.prompt(
                'please enter amount paid in cents: ', type=int
            )
            update_task_info(
                dict(request_id=transaction_id),
                dict(
                    op_info=dict(
                        request_id=transaction_id,
                        tran_type='payment',
                        status=status,
                        operation=dict(
                            id=id_value, amount=amount, currency='MXN'
                        ),
                    )
                ),
            )
        else:
            update_insert_task_info(
                {'request_id': transaction_id},
                {
                    'op_info.request_id': transaction_id,
                    'op_info.tran_type': 'payment',
                    'op_info.status': status,
                },
            )
        try:
            CallbackHelper.send_op_result(
                OpInfo(transaction_id, OperationType.payment, status)
            )
        except ConnectionError:
            click.echo('connection error try again')
