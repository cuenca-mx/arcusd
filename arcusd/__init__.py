import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from .types import OperationType, OperationStatus

sentry_sdk.init(os.environ['ARCUSD_SENTRY_DSN'],
                integrations=[CeleryIntegration()])
