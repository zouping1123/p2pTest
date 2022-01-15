import app


class ApproveApi:
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.getapprove_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self,session,realname,cardId):
        data = {"realname":realname, "card_id":cardId}
        response = session.post(self.approve_url, data, files={"x":"y"})
        return response

    def getApprove(self,session):
        response = session.post(self.getapprove_url)
        return response