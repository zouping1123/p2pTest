import logging
import random
import time
import unittest

import requests
from parameterized import parameterized

from api.loginApi import loginApi
from utils import read_param_data, assert_utils


class login(unittest.TestCase):
    imgCode = '8888'
    phone1 = '13033447711'
    errorpwd = 'test1234'
    pwd = 'test123'

    def setUp(self) -> None:
        self.login_api = loginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    #获取图片验证码
    @parameterized.expand(read_param_data("imgVerify.json","test_get_img_verify_code","type,status_code"))
    def test01_get_img_code(self,type,status_code):
        # 根据不同的type类型准备不同的参数数据
        r = ''
        if type == 'float':
            r = str(random.random())
        elif type == 'int':
            r = str(random.randint(10000000, 90000000))
        elif type == 'char':
            r = ''.join(random.sample("abcdedfhijklmn", 8))
        # 发送请求
        response = self.login_api.getImgCode(self.session, r)
        logging.info("r = {} response = {}".format(r, response))
        # 对响应结果进行断言
        self.assertEqual(status_code, response.status_code)

    # 获取短信验证码
    @parameterized.expand(read_param_data("smsVerify.json","test_get_sms_verify_code","phone,img_code,status_code,status,description"))
    def test02_get_sms_code(self,phone,img_code,status_code,status,description):
        #1.获取图片验证码
        r = str(random.random())
        response = self.login_api.getImgCode(self.session, r)
        # 对响应结果进行断言
        self.assertEqual(200, response.status_code)

        #2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, phone, img_code)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, status_code, status, description)

    #注册
    @parameterized.expand(read_param_data("register.json","test_register","phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description"))
    def test03_register(self,phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description):
        # 1、获取图片验证码成功
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码成功
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、使用参数化的测试数据进行注册，并返回对应的结果
        # 发送注册请求
        response = self.login_api.register(self.session,phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone)
        assert_utils(self,response,status_code,status,description)

    @parameterized.expand(read_param_data("login.json","test_login","phone,pwd,status_code,status,description"))
    def test04_login(self,phone,pwd,status_code,status,description):
        data = {"phone": phone,
                "password": pwd}
        print(data)
        response = self.login_api.login(self.session,phone,pwd)
        logging.info("login request = {}".format(data))
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, status_code, status, description)

    # 登录成功
    def test5_login_pwderror(self):
        # 输入错误密码，提示错误一次
        response = self.login_api.login(self.session, self.phone1, self.errorpwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        # 输入错误密码，提示错误2次
        response = self.login_api.login(self.session, self.phone1, self.errorpwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        # 输入错误密码，提示被锁定
        response = self.login_api.login(self.session, self.phone1, self.errorpwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 输入正确密码，提示被锁定
        response = self.login_api.login(self.session, self.phone1, self.errorpwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        #等待60秒，输入正确密码登录成功
        time.sleep(60)

        # 输入正确密码，登录成功
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "登录成功")


