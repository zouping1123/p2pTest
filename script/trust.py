import unittest
from random import random

import requests
import logging

from bs4 import BeautifulSoup

from api.loginApi import loginApi
from api.trustApi import TrustApi
from utils import assert_utils, third_api


class Trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginApi()
        self.trust_api = TrustApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    #开户
    def test1_open_account(self):
        #登录已认证的账号
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        #发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust register response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        # 3、 发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))

        #调用第三方接口
        response = third_api(self.session, form_data)

        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    #充值
    def test2_recharge(self):
        # 登录已认证的账号
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

        #获取充值验证码
        r = random()
        response = self.trust_api.get_recharge_verify_code(self.session,str(r))
        logging.info("recharge verify_code response = {}".format(response.text))
        self.assertEqual(200,response.status_code)

        #发送充值请求
        response = self.trust_api.recharge(self.session,"1000")
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        #第三方充值请求
        #获取响应中form表单数据
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))

        # 调用第三方接口
        response = third_api(self.session, form_data)

        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('NetSave OK', response.text)



