import app


class tenderApi:
    def __init__(self):
        self.get_loaninfo_url = app.BASE_URL + "/common/loan/loaninfo"
        self.tender_url = app.BASE_URL + "/trust/trust/tender"
        self.tenderlist_url = app.BASE_URL + "/loan/tender/mytenderlist"

    def getTenderInfo(self, session, tender_id):
        data = {"id": tender_id}
        response = session.post(self.get_loaninfo_url,data)
        return response

    def tender(self, session, tender_id, amount):
        data = {"id": tender_id,
                "depositCertificate":-1,
                "amount": amount}
        response = session.post(self.tender_url,data)
        return response

    def getTenderList(self, session,status):
        data = {"status": status}
        response = session.post(self.tenderlist_url, data=data)
        return response
