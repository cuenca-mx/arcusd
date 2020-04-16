import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


if os.environ.get('ARCUSD_PROD', 'true') == 'true':
    sentry_sdk.init(os.environ['ARCUSD_SENTRY_DSN'],
                    integrations=[CeleryIntegration()])
