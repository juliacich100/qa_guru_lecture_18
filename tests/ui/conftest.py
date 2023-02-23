import pytest
from utils.base_session import BaseSession
import os

# from selene.support.shared import browser
#
#
# @pytest.fixture(scope='session', autouse=True)
# def browser_management():
#     browser.config.base_url = 'https://demowebshop.tricentis.com'
#     browser.config.window_height = 1080
#     browser.config.window_width = 1920
#
#     yield
#
#     browser.quit()


@pytest.fixture(scope='session')
def demoshop():
    api_url = os.getenv("API_URL")
    return BaseSession(api_url)