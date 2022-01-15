import unittest
import requests

from api.approveApi import ApproveApi
from api.loginApi import loginApi
from utils import assert_utils
import logging

class approve(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    realname = '张三'
    cardId = '110117199003070995'

    def setUp(self) -> None:
        self.approveApi = ApproveApi()
        self.login_api = loginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    #认证成功
    def test1_approveSuccess(self):
        #登录
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

        #认证
        response = self.approveApi.approve(self.session,self.realname,self.cardId)
        logging.info("approve response = {}".format(response.json()))
        assert_utils(self,response,200,200,"提交成功!")

    # 获取认证信息
    def test04_get_approve(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone1)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取认证请求
        response = self.approveApi.getApprove(self.session)
        logging.info('approve response = {}'.format(response.json()))
        # 对结果进行断言
        self.assertEqual(200, response.status_code)

