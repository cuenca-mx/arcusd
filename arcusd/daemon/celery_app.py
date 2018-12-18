from celery import Celery

app = Celery('arcusd')
app.config_from_object('arcusd.daemon.celeryconfig')

if __name__ == '__main__':
    app.start()
