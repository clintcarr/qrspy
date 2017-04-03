import requests
import string
import json
import random

requests.packages.urllib3.disable_warnings()

def set_xrf():
    characters = string.ascii_letters + string.digits
    return ''.join(random.sample(characters, 16))

xrf = set_xrf()

headers = {
    'content-type': 'application/json',
    'X-Qlik-Xrfkey': xrf,
}

class ConnectQlik:
    def __init__(self, server, virtualproxy=None, certificate = False, root = False
        ,userdirectory = False, userid = False):
        self.server = server
        self.virtualproxy = virtualproxy
        self.certificate = certificate
        self.root = root
        self.userdirectory = userdirectory
        self.userid = userid

    def get_ticket(self):
        payload = {'UserDirectory': self.userdirectory, 'UserId': self.userid}
        json_payload = json.dumps(payload)
        url = 'https://{0}:4243/qps/ticket?Xrfkey={1}'.format(self.server,xrf)
        if self.virtualproxy is not None:
            url = 'https://{0}:4243/qps/{1}/ticket?Xrfkey={2}'.format(self.server,self.virtualproxy,xrf)
        response = requests.post(url
            ,data=json_payload, headers=headers, verify=self.root, cert=self.certificate)
        return response.json().get('Ticket')

if __name__ == '__main__':

    qlik = ConnectQlik(server='qs2.qliklocal.net',
        virtualproxy='ticketing',
        certificate=('C:/certs/qs2.qliklocal.net/client.pem', 'c:/certs/qs2.qliklocal.net/client_key.pem'), 
        root='C:/certs/qs2.qliklocal.net/root.pem',
        userdirectory='qliklocal',
        userid='administrator')

    print(qlik.get_ticket())



