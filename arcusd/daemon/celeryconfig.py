import os

broker_url = os.environ['ARCUSD_AMPQ_ADDRESS']
task_serializer = 'json'
accept_content = ['json']
task_default_queue = os.environ['ARCUSD_PAYMENTS_QUEUE']
imports = [
    'arcusd.daemon.arcusd_signals',
]
include = [
    'arcusd.daemon.tasks',
    'arcusd.daemon.tasks_sync',
]
result_backend = 'amqp'
