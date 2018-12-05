broker_url = 'rabbitmq'
task_serializer = 'json'
accept_content = ['json']
task_default_queue = 'arcusd.paymentservices'
include = ['arcusd.daemon.tasks']
backend = 'amqp'
