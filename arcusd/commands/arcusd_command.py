import click

from arcusd import OperationType
from arcusd.callbacks import CallbackHelper
from arcusd.contracts import OpInfo
from arcusd.data_access.tasks import get_task_info, update_task_info,\
    save_task_info
from datetime import datetime


@click.group()
def arcusd_cli():
    pass


@arcusd_cli.command()
@click.argument('transaction_id', type=str)
@click.argument('status', type=click.Choice(['success', 'failed']))
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
            amount = click.prompt('please enter amount paid in cents: ',
                                  type=int)
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


@arcusd_cli.command()
@click.argument('transaction_id', type=str)
@click.argument('status', type=str)
def cancel_task(transaction_id: str, status: str) -> None:
    """"script to change the status of a transaction from
    success to cancelled on refund"""

    task = get_task_info(dict(request_id=transaction_id))
    if task is None:
        click.echo(f'transaction id {transaction_id} does not exists')
        return
    else:
        try:
            date = datetime.now()
            Zendesk_link = click.prompt('please enter Zendesk link of ticket',
                                        type=str)
            update_task_info(dict(request_id=transaction_id), dict(
                op_info=dict(
                    status='CANCELLED'
                )
            ))
            save_task_info(dict(refund_details=dict(
                Zendesk_link=Zendesk_link,
                datetime=date,)))
        except ConnectionError:
            click.echo('connection error try again')
        finally:
            CallbackHelper.send_op_result(OpInfo(transaction_id,
                                                 OperationType.payment,
                                                 status))
            click.echo('Successfully changed')
