import unittest
import logging
import requests

from api.loginApi import loginApi
from api.tenderApi import tenderApi
from utils import assert_utils, third_api


class tender(unittest.TestCase):
    tender_id = 746

    def setUp(self) -> None:
        self.login_api = loginApi()
        self.tender_api = tenderApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    #投资产品详情
    def test1_getTenderInfo(self):
        response = self.tender_api.getTenderInfo(self.session, self.tender_id)
        logging.info("get_tender response={}".format(response.json()))
        #断言
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual("746", response.json().get("data").get("loan_info").get("id"))

    #投资
    def test2_tender(self):
        amount = 1000
        response = self.tender_api.tender(self.session,self.tender_id,amount)
        logging.info("tender response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200, response.json().get("status"))

        #获取HTML内容
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = third_api(self.session,form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('InitiativeTender OK', response.text)