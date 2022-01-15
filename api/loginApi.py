import app


class loginApi:
    def __init__(self):
        self.imgCode_url = app.BASE_URL + "/common/public/verifycode1/"
        self.smsCode_url = app.BASE_URL + "/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL + "/member/public/login"

    def getImgCode(self,session,r):
        url = self.imgCode_url + r
        response = session.get(url)
        return response

    def getSmsCode(self,session,phone,imgVerifyCode):
        data = {'phone': phone, 'imgVerifyCode': imgVerifyCode, 'type': 'reg'}
        response = session.post(self.smsCode_url,data=data)
        return response

    def register(self,session,phone,pwd,imgVerifyCode,phoneCode,dyServer,invitePhone):
        data = {"phone": phone,
                "password": pwd,
                "verifycode": imgVerifyCode,
                "phone_code": phoneCode,
                "dy_server": dyServer,
                'invite_phone': invitePhone}
        response = session.post(self.register_url, data=data)
        return response

    def login(self,session,phone='13033447711',pwd='test123'):
        data = {"keywords": phone,
                "password": pwd}
        response = session.post(self.login_url, data=data)
        return response