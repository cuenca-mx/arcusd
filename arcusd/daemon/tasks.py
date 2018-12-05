from .celery_app import app


@app.task
def topup(biller_id: int,
          phone_number: str,
          amount: float,
          currency: str = 'MXN') -> int:
    process = f'{biller_id}, {phone_number}, {amount}, {currency}'
    print(process)
    return process
