import requests
from requests_ntlm import HttpNtlmAuth
import json
import csv
import random
import string


requests.packages.urllib3.disable_warnings()

def set_xrf():
    characters = string.ascii_letters + string.digits
    return ''.join(random.sample(characters, 16))

xrf = set_xrf()

headers = {"X-Qlik-XrfKey": xrf,
            "Accept": "application/json",
            "X-Qlik-User": "UserDirectory=Internal;UserID=sa_repository",
            "Content-Type": "application/json"}

session = requests.session()

class ConnectQlik:
    """
    Instantiates the Qlik Repository Service Class
    """

    def __init__(self, server, certificate=False, root=False
        , userdirectory=False, userid=False, credential=False, password=False):
        """
        Establishes connectivity with Qlik Sense Repository Service
        :param server: servername.domain:4242
        :param certificate: path to client.pem and client_key.pem certificates
        :param root: path to root.pem certificate
        :param userdirectory: userdirectory to use for queries
        :param userid: user to use for queries
        :param credential: domain\\username for Windows Authentication
        :param password: password of windows credential
        """
        self.server = server
        self.certificate = certificate
        self.root = root
        if userdirectory is not False:
            headers["X-Qlik-User"] = "UserDirectory={0};UserID={1}".format(userdirectory, userid)
        self.credential = credential
        self.password = password

    @staticmethod
    def csvrowcount(filename):
        """
        Returns the count of rows minus the header of the file
        :param filename: Path and filename of the text or csv file to be imported
        """
        rowcount = 0
        with open(filename, 'rt') as f:
            for row in f:
                rowcount += 1
        return rowcount - 1

    @staticmethod
    def jsonfieldnames(filename):
        """
        Returns the header row of the file to create the structure of the json file
        :param filename: Path and filename of the text or csv file to be imported
        """
        jsonfieldnames = []
        with open(filename, 'rt') as f:
            for row in csv.reader(f, delimiter=','):
                jsonfieldnames.append(row)
        return jsonfieldnames[0]

    def concsvjson(self, filename):
        """
        Converts the text or csv file to a JSON file and returns the path and name of the file
        :param filename: Path and filename of the text or csv file to be imported
        """
        jsonfieldnames = self.jsonfieldnames(filename)
        csv_file = filename
        json_file = csv_file.split(".")[0] + ".json"
        with open(csv_file, 'rt') as f:
            next(f)
            csv_reader = csv.DictReader(f, jsonfieldnames)
            with open(json_file, 'w') as jf:
                data = json.dumps([r for r in csv_reader])
                jf.write(data)
        return json_file

    def get(self,endpoint,filterparam=None, filtervalue=None):
        """
        Function that performs GET method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        :param filterparam: Filter for endpoint, use None for no filtering
        :param filtervalue: Value to filter on, use None for no filtering
        """
        if self.credential is not False:
            session.auth = HttpNtlmAuth(self.credential, self.password, session)
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        if filterparam is None:
            if '?' in endpoint:
                response = session.get('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
                return (response.content)
            else:
                response = session.get('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
                return (response.content)
        else:
            response = session.get("https://{0}/{1}?filter={2} '{3}'&xrfkey={4}".format 
                                    (self.server, endpoint, filterparam, filtervalue, xrf), 
                                    headers=headers, verify=self.root, cert=self.certificate)
            return (response.content)

    def delete(self, endpoint):
        """
        Function that performs DELETE method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint: 
            response = session.delete('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.status_code)
        else:
            response = session.delete('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.status_code)

    def put(self, endpoint):
        """
        Function that performs PUT method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint:
            response = session.put('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.status_code)
        else:
            response = session.put('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.status_code)

    def post(self, endpoint, data=None):
        """
        Function that performs POST method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        :param data: Data that is posted as either JSON encoded or not.
        """
        if '?' in endpoint:
            if data is None:
                response = session.post('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return (response.status_code)
            else:
                response = session.post('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                return (response.status_code)
        else:
            if data is None:
                response = session.post('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return (response.status_code)
            else:
                response = session.post('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                return (response.status_code)

    def get_qps(self, endpoint):
        """
        Function that performs GET method to Qlik Proxy Service endpoints
        :param endpoint: API endpoint path
        """
        server = self.server
        qps = server[:server.index(':')]
        response = session.get('https://{0}/{1}?xrfkey={2}'.format (qps, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
        return (response.status_code)

    def get_about(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/about')))

    def get_app(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app', filterparam, filtervalue)))

    def get_dataconnection(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/dataconnection', filterparam, filtervalue)))

    def get_user(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/user', filterparam, filtervalue)))

    def get_license(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/license')))


    def get_lef(self, serial, control, user, organization, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/license/download?serial={0}&control={1}&user={2}&org={3}'.format 
            (serial, control, user, organization))))
    
    def get_appcount(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/count')))        

    def get_customproperty(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/custompropertydefinition', filterparam, filtervalue)))

    def get_tag(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/tag', filterparam, filtervalue)))
    
    def get_task(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/task', filterparam, filtervalue)))

    def get_systemrule(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/systemrule', filterparam, filtervalue)))

    def get_userdirectory(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/userdirectory', filterparam, filtervalue)))

    def get_exportappticket(self, appid, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/{0}/export'.format(appid))))
        
    def get_extension(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/extension', filterparam, filtervalue)))

    def get_stream(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/stream', filterparam, filtervalue)))

    def get_servernode(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration', filterparam, filtervalue)))

    def get_useraccesstype(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/license/useraccesstype', filterparam, filtervalue)))

    def get_loginaccesstype(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/license/loginaccesstype', filterparam, filtervalue)))

    def get_appobject(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/object', filterparam, filtervalue)))

    def get_apidescription(self, method, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/about/api/description?extended=true&method={0}&format=JSON'.format 
             (method))))

    def get_serverconfig(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration/local'))) 

    def get_emptyserverconfigurationcontainer(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration/local'))) 

    def get_contentlibrary(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/contentlibrary', filterparam, filtervalue)))

    def get_appprivileges(self, appid, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/{0}/privileges'.format (appid) , filterparam, filtervalue)))

    def delete_user(self, userid):
         return self.delete('qrs/user/{0}'.format (userid))

    def delete_license(self):
        license = self.get_license()
        licenseid = license['id']
        return self.delete('qrs/license/{0}'.format (licenseid))

    def delete_app(self, appid):
        return self.delete('qrs/app/{0}'.format (appid))

    def delete_stream(self, streamid):
        return self.delete('qrs/stream/{0}'.format (streamid))

    def delete_tag(self, tagid):
        return self.delete('qrs/tag/{0}'.format (tagid))

    def delete_customproperty(self, custompropertyid):
        return self.delete('qrs/custompropertydefinition/{0}'.format (custompropertyid))

    def delete_useraccesstype(self, useraccessid):
        return self.delete('qrs/license/useraccesstype/{0}'.format (useraccessid))

    def delete_appobject(self, objectid):
        return self.delete('qrs/app/object/{0}'.format (objectid))

    def delete_loginaccesstype(self, ruleid):
        return self.delete('qrs/license/loginaccesstype/{0}'.format (ruleid))

    def publish_app(self, appid, streamid, name):
        return self.put('qrs/app/{0}/publish?stream={1}&name={2}'.format (appid, streamid, name))

    def migrate_app(self, appid):
        return self.put('qrs/app/{0}/migrate'.format (appid)) 

    def publish_appobject(self, objid):
        return self.put('qrs/app/object/{0}/publish'.format (objid))

    def unpublish_appobject(self, objid):
        return self.put('qrs/app/object/{0}/unpublish'.format (objid))

    def replace_app(self, appid, replaceappid):
        return self.put('qrs/app/{0}/replace?app={1}'.format(appid, replaceappid))

    def set_license(self, control, serial, name, organization, lef):
        if lef is None:
            license = {
                "serial": serial,
                "name": name,
                "organization": organization
            }
            data = json.dumps(license)
            return self.post('qrs/license?control={0}'.format (control), data)
        else:
            license = {
                "serial": serial,
                "name": name,
                "organization": organization,
                "lef": lef
            }
            data = json.dumps(license)
            return self.post('qrs/license?control={0}'.format (control), data)

    def import_users(self, filename):
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post('qrs/user', users)
        else:
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post('qrs/user/many', users)

    def import_tag(self, filename):
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post('qrs/tag', tags)
        else:
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post('qrs/tag/many', tags)

    def start_task(self, taskid):
        return self.post('qrs/task/{0}/start'.format (taskid))

    def import_extension(self, filename):
        with open(filename, 'rb') as extension:
            return self.post('qrs/extension/upload', extension)

    def copy_app(self, appid, name):
        return self.post('qrs/app/{0}/copy?name={1}'.format (appid, name))

    def new_stream(self, name):
        stream = {'name': name}
        data = json.dumps(stream)
        return self.post('qrs/stream', data)

    def sync_userdirectory(self, userdirectoryid):
        udid = '["{0}"]'.format (userdirectoryid)
        return self.post('qrs/userdirectoryconnector/syncuserdirectories', udid)

    def export_certificates(self, machinename, certificatepassword, includesecret, exportformat):
        certificateinfo = {"machineNames": [machinename], "certificatePassword": certificatepassword,
                            "includeSecretsKey": includesecret, "ExportFormat": exportformat}
        data = json.dumps(certificateinfo)
        return self.post('qrs/certificatedistribution/exportcertificates', data)

    def new_node(self, name, hostname, engineenabled, proxyenabled, schedulerenabled, printingenabled):
        nodedata = {"configuration": {"name": name, "hostName": hostname, "engineEnabled": engineenabled,
                                  "proxyEnabled": proxyenabled, "schedulerEnabled": schedulerenabled,
                                  "printingEnabled": printingenabled}}
        data = json.dumps(nodedata)
        return self.post('qrs/servernodeconfiguration/container', data)
        # data = container.text
        # jdata = json.loads(data)
        # return jdata["configuration"]["id"]

    def new_dataconnection(self, username, password, name, connectionstring, conntype):
        dataconnection = {
                            "username": username,
                            "password": password,
                            "name": name,
                            "connectionstring": connectionstring,
                            "type": conntype
                        }
        data = json.dumps(dataconnection)
        return self.post('qrs/dataconnection', data)
  
    def import_app(self, name, filename):
        headers["Content-Type"] = "application/vnd.qlik.sense.app"
        headers["Connection"] = "Keep-Alive"
        with open(filename, 'rb') as app:
            return self.post('qrs/app/upload?name={0}'.format(name), app)

    def import_customproperty(self, filename):
        with open(filename) as customproperties:
            properties = json.loads(customproperties.read())
            data = json.dumps(properties)
            return self.post('qrs/custompropertydefinition/many', data)

    def import_librarycontent(self, library, filepath, contentname):
        with open(filepath, 'rb') as data:
            return self.post('qrs/contentlibrary/{0}/uploadfile?externalpath={1}'.format (library, filepath), data)

    def reload_app(self, appid):
        return self.post('qrs/app/{0}/reload'.format (appid))

    def delete_librarycontent(self, library, contentname):
        return self.delete('qrs/contentlibrary/{0}/deletecontent?externalpath={1}'.format (library, contentname))

    def delete_contentlibrary(self, library):
        return self.delete('qrs/contentlibrary/{0}'.format (library))

    def export_app(self, appid, filepath, filename):
        exportticket = self.get_exportappticket(appid)
        ticket = (exportticket['value'])
        data = self.get('qrs/download/app/{0}/{1}/{2}'.format (appid, ticket, filename))
        with open(filepath + filename, 'wb') as file:
            file.write(data)
        return ('Application: {0} written to {1}'.format (filename, filepath))

    def ping_proxy(self):
        try:
            return (self.get_qps('qps/user'))
        except requests.exceptions.RequestException as exception:
            return ('Qlik Sense Proxy down')

    def new_systemrule(self, filename):
        with open(self.concsvjson(filename), 'rb') as systemrule:
            rule = json.loads(systemrule.read())
            data = json.dumps(rule)
            print (data)
            return self.post('qrs/systemrule', data)

if __name__ == '__main__':
    qrs = ConnectQlik(server='qs2.qliklocal.net:4242', 
                    certificate=('C:/certs/qs2.qliklocal.net/client.pem',
                                      'C:/certs/qs2.qliklocal.net/client_key.pem'),
                    root='C:/certs/qs2.qliklocal.net/root.pem')
    if qrs.ping_proxy() == 200:
        print(qrs.get_about())

