import pytest


@pytest.fixture(scope='module')
def vcr_config():
    return dict(
        ignore_hosts={'sentry.io'}
    )


@pytest.fixture(scope='module')
def vcr(vcr):
    vcr.record_mode = 'new_episodes'
    return vcr
