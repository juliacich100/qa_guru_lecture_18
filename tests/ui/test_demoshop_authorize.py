import os
import requests
from selene.support.shared import browser
from allure_commons._allure import step
from selene import have
from dotenv import load_dotenv
from utils.base_session import BaseSession

load_dotenv()  # метод, котрый подгружает все из файла .env
LOGIN = "sponge@bob.com"
PASSWORD = "qwerty"
API_URL = os.getenv('API_URL')   # в этом проекте урл апишки совпадает в вебом, но так не всегда бывает
WEB_URL = os.getenv('WEB_URL')
browser.config.base_url = WEB_URL


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


'''Комбинируем апи-тест с юайным тестом'''


def test_login_through_api():
    response = requests.post(f'{API_URL}/login', data={'Email': 'sponge@bob.com', 'Password': 'qwerty'}, allow_redirects=False)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')
    print(authorization_cookie)

    browser.open("/Themes/DefaultClean/Content/images/logo.png")  # инициализируем веб драйвер (открываем быструю страницу)
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})  # подкладываем нашу куку авторизации
    browser.open('')  # открываем пустую страницу, чтобы кука подхватилась

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


'''Дальше апгрейдим наш тест: создаем папку utils с модулем base_session, в котором пишем класс, чтобы склейвать 
базовый урл с тем урлом, который передается'''


def test_login_through_api_with_base_session():
    demoshop = BaseSession(API_URL)     # создаем объект класса BaseSession
    response = demoshop.post('/login', data={'Email': 'sponge@bob.com', 'Password': 'qwerty'},
                             allow_redirects=False)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')
    print(authorization_cookie)

    browser.open(
        "/Themes/DefaultClean/Content/images/logo.png")  # инициализируем веб драйвер (открываем быструю страницу)
    browser.driver.add_cookie(
        {"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})  # подкладываем нашу куку авторизации
    browser.open('')  # открываем пустую страницу, чтобы кука подхватилась

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


'''Выносим объект demoshop в фикстуру в conftest.py, фикстура сессии будет передаваться в тесте'''


def test_login_through_api_with_base_session_fixture(demoshop):
    response = demoshop.post('/login', data={'Email': 'sponge@bob.com', 'Password': 'qwerty'},
                             allow_redirects=False)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')
    print(authorization_cookie)

    browser.open(
        "/Themes/DefaultClean/Content/images/logo.png")  # инициализируем веб драйвер (открываем быструю страницу)
    browser.driver.add_cookie(
        {"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})  # подкладываем нашу куку авторизации
    browser.open('')  # открываем пустую страницу, чтобы кука подхватилась

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


