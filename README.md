# arcusd
[Build Status](https://travis-ci.com/cuenca-mx/arcusd.svg?branch=master)](https://travis-ci.com/cuenca-mx/arcusd)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/arcusd/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/arcusd?branch=master)

arcus daemon

### Requirements
- Python v3+
- RabbitMQ
- Docker

### Testing
You can test arcusd using `make` tool.

If you want to run tests inside a container you should run

`make docker-test`

### Running arcusd

```bash
docker-compose up
```




### Basic usage
With arcusd you can pay services as phone line, electricity, water and top-ups using Arcus API.

First you need to create a client code in order to send payment requests. Example:

```python
import os

from celery import Celery

ARCUSD_BROKER_URL = os.environ['ARCUSD_BROKER_URL']
ARCUSD_QUEUE = os.environ['ARCUSD_QUEUE']

app = Celery('tasks')
app.conf.update(
    broker_url=ARCUSD_BROKER_URL,
    task_serializer='json',
    task_default_queue=ARCUSD_QUEUE,
    result_backend='amqp'
)

```

Once you have your arcusd client, you have to send the action you want to execute in arcusd.
######Action responses will be send back using a `POST` callback (not implemented yet). 
For instance, if you want to know your CFE service bill you have to send the following message:
 
##### Get Bill
```python
app.send_task('arcusd.daemon.tasks.query_bill', kwargs={
    'biller_id': 35,
    'account_number': '501000000007'
})

```
 
##### Pay Bill
Now for paying a bill:

```python
app.send_task('arcusd.daemon.tasks.pay_bill', kwargs={
    'biller_id': 35,
    'account_number': '501000000007'
})
```

##### Cancel Transaction
After you pay, there are some bills that requires some hours to be fulfilled and 
some of them can be canceled before that limit of time. You can cancel with the following message:
 
```python
my_transaction_id = 9876543

app.send_task('arcusd.daemon.tasks.cancel_bill', kwargs={
    'transaction_id': my_transaction_id
})
```

##### Top-up
For topups you have to send the following message:
Note that `amount` must be expressed in cents. The example code make a top-up of MXN $100.00
```python
app.send_task('arcusd.daemon.tasks.topup', kwargs={
    'biller_id': 13599,
    'phone_number': '5599999999',
    'amount': 10000,
    'currency': 'MXN'
})
```
