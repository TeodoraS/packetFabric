import logging
import pytest

from framework.engines.rest_engine import RestEngine

logger = logging.getLogger()


@pytest.fixture(scope='module')
def session(request):
    logger.info("Initialize RestApi Engine")
    session = RestEngine()

    def close_session():
        session.close_session()

    request.addfinalizer(close_session)
    return session


@pytest.fixture(scope="module")
def build_path(request):
    return request.config.rootdir
