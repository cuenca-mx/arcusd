import pytest


@pytest.fixture(scope='module')
def vcr_config():
    return dict(
        ignore_hosts={'sentry.io'}
    )
