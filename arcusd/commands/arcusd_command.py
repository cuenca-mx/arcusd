import click

from arcusd.data_access.tasks import get_task_info


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
    """Script to set the status of an operation on the db"""
    print(transaction_id)
    print(status)
    task = get_task_info({'tasks_kwargs.request_id': transaction_id})
    if task is None:
        print(f'trarnsaction does {transaction_id} not exists')
        return


