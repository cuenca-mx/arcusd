import click

from arcusd import OperationStatus, OperationType
from arcusd.callbacks import CallbackHelper
from arcusd.contracts import OpInfo
from arcusd.data_access.tasks import get_task_info,  update_task_info


@click.group()
def arcusd_cli():
    pass


@arcusd_cli.command()
def test():
    """Example script."""
    click.echo('Hello World!')


@arcusd_cli.command()
@click.argument('transaction_id', type=str)
@click.argument('status', type=str)
def change_status(transaction_id: str, status: str) -> None:
    """Script to set the status of a transaction on the db"""

    task = get_task_info({'tasks_kwargs.request_id': transaction_id})
    if task is None:
        click.echo(f'transaction id {transaction_id} does not exists')

    else:
        if hasattr(task, 'op_info'):
            print('tasks was successfully handled')
        else:
            try:
                if status == OperationStatus.success:
                    print('request values')
                    id_value = click.prompt('please enter arcus id: ', type=int)
                    amount = click.prompt('please enter amount paid: ', type=int)
                    update_task_info({'request_id': transaction_id},
                                     {'op_info': {'request_id': transaction_id,
                                                  'tran_type': 'payment',
                                                  'status': status,
                                                  'operation': {
                                                      'id': id_value,
                                                      'amount': amount,
                                                      'currency': 'MXN'}
                                                  }
                                      })
                else:
                    update_task_info({'request_id': transaction_id},
                                     {'op_info': {'request_id': transaction_id, 'tran_type': 'payment', 'status': status}})
            except ConnectionError:
                click.echo('connection error, try again')
            finally:
                CallbackHelper.send_op_result(OpInfo(transaction_id, OperationType.payment, status))
