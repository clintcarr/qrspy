import requests
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

class ConnectQlik:
    """
    Instantiates the Qlik Repository Service Class
    """

    def __init__(self, server, certificate, root):
        """
        Establishes connectivity with Qlik Sense Repository Service
        :param server: servername.domain:4242
        :param certificate: path to client.pem and client_key.pem certificates
        :param root: path to root.pem certificate
        """
        self.server = server
        self.certificate = certificate
        self.root = root
    
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
        if filterparam is None:
            if '?' in endpoint:
                response = requests.get('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
                return (response.content)
            else:
                response = requests.get('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
                return (response.content)
        else:
            response = requests.get("https://%s/%s?filter=%s '%s'&xrfkey=%s" % 
                (self.server, endpoint, filterparam, filtervalue, xrf), 
                headers=headers, verify=self.root, cert=self.certificate)
            return (response.content)

    def delete(self, endpoint):
        """
        Function that performs DELETE method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        response = requests.delete('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
        return (response.text)

    def put(self, endpoint):
        """
        Function that performs PUT method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint:
            response = requests.put('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.text)
        else:
            response = requests.put('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return (response.text)

    def post(self, endpoint, data=None):
        """
        Function that performs POST method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        :param data: Data that is posted as either JSON encoded or not.
        """
        if '?' in endpoint:
            if data is None:
                response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return (response.text)
            else:
                response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                return (response.text)
        else:
            if data is None:
                response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return (response.text)
            else:
                response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                return (response.text)

    def get_qps(self, endpoint):
        """
        Function that performs GET method to Qlik Proxy Service endpoints
        :param endpoint: API endpoint path
        :param filterparam: Filter for endpoint, use None for no filtering
        :param filtervalue: Value to filter on, use None for no filtering
        """
        server = self.server
        qps = server[:server.index(':')]
        response = requests.get('https://%s/%s?xrfkey=%s' % (qps, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
        return (response.status_code)

    def get_about(self, filterparam=None, filtervalue=None):
        return (self.get('qrs/about'))

    def get_app(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app', filterparam, filtervalue)))

    def get_dataconnection(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/dataconnection', filterparam, filtervalue)))

    def get_user(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/user', filterparam, filtervalue)))

    def get_license(self, filterparam=None, filtervalue=None):
        try:
            return (json.loads(self.get('qrs/license')))
        except TypeError:
            return ('Server not licensed')

    def get_lef(self, serial, control, user, organization, filterparam=None, filtervalue=None):
        return self.get('qrs/license/download?serial=%s&control=%s&user=%s&org=%s' % 
            (serial, control, user, organization))
    
    def get_appcount(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/count')))        

    def get_customproperty(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/custompropertydefinition', filterparam, filtervalue)))

    def get_tag(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/tag', filterparam, filtervalue)))
    
    def get_task(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/task', filterparam, filtervalue)))

    def get_securityrule(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/systemrule', filterparam, filtervalue)))

    def get_securityrule(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/userdirectory', filterparam, filtervalue)))

    def get_exportappticket(self, appid, filterparam=None, filtervalue=None):
        response = (json.loads(self.get('qrs/app/%s/export' % appid)))
        return response

    def get_extension(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/extension', filterparam, filtervalue)))

    def get_stream(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/stream', filterparam, filtervalue)))

    def get_servernode(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration', filterparam, filtervalue)))

    def get_useraccesstype(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/license/useraccesstype', filterparam, filtervalue)))

    def get_appobject(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/app/object', filterparam, filtervalue)))

    def get_apidescription(self, method, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/about/api/description?extended=true&method=%s&format=JSON' 
            % method)))

    def get_serverconfig(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration/local'))) 

    def get_emptyserverconfigurationcontainer(self, filterparam=None, filtervalue=None):
        return (json.loads(self.get('qrs/servernodeconfiguration/local'))) 

    def delete_user(self, userid):
         return self.delete('qrs/user/%s' % userid)

    def delete_license(self):
        license = self.get_license()
        licenseid = license['id']
        return self.delete('qrs/license/%s' % licenseid)

    def delete_app(self, appid):
        return self.delete('qrs/app/%s' % appid)

    def delete_stream(self, streamid):
        return self.delete('qrs/stream/%s' % streamid)

    def delete_tag(self, tagid):
        return self.delete('qrs/tag/%s' % tagid)

    def delete_stream(self, custompropertyid):
        return self.delete('qrs/custompropertydefinition/%s' % custompropertyid)

    def delete_useraccesstype(self, useraccessid):
        return self.delete('qrs/license/useraccesstype/%s' % useraccessid)

    def delete_appobject(self, objectid):
        return self.delete('qrs/app/object/%s' % objectid)

    def publish_app(self, appid, streamid, name):
        return self.put('qrs/app/%s/publish?stream=%s&name=%s' % (appid, streamid, name))

    def migrate_app(self, appid):
        return self.put('qrs/app/%s/migrate' % appid  ) 

    def publish_appobject(self, objid):
        return self.put('qrs/app/object/%s/publish' % objid)

    def unpublish_appobject(self, objid):
        return self.put('qrs/app/object/%s/unpublish' % objid)

    def set_license(self, control, serial, name, organization, lef):
        if lef is None:
            license = {
                "serial": serial,
                "name": name,
                "organization": organization
            }
            data = json.dumps(license)
            return self.post('qrs/license?control=%s' % control, data)
        else:
            license = {
                "serial": serial,
                "name": name,
                "organization": organization,
                "lef": lef
            }
            data = json.dumps(license)
            return self.post('qrs/license?control=%s' % control, data)

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

    def start_task(self, taskid, data=None):
        return self.post('qrs/task/%s/start' % taskid)

    def import_extension(self, filename):
        with open(filename, 'rb') as extension:
            return self.post('qrs/extension/upload', extension)

    def copy_app(self, appid, name, data=None):
        return self.post('qrs/app/%s/copy?name=%s' % (appid, name))

    def new_stream(self, name):
        stream = {'name': name}
        data = json.dumps(stream)
        return self.post('qrs/stream', data)

    def sync_userdirectory(self, userdirectoryid):
        udid = '["%s"]' % userdirectoryid
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
            return self.post('qrs/app/upload?name=%s' % name, app)

    def import_customproperty(self, filename):
        '''
         Imports custom properties into Qlik Sense
         :param filename: Path and filename to JSON file
         "App","ContentLibrary","DataConnection","EngineService","Extension","ProxyService","ReloadTask",
         "RepositoryService","SchedulerService","ServerNodeConfiguration","Stream","User","UserSyncTask",
         "VirtualProxyConfig"
         {
             "name": "FOO",
             "valueType": "BAR",
             "choiceValues":
                 ["FOO",
                 "BAR"],
             "objectTypes":
                 ["App",
                  "RepositoryService"]}
         :usage: import_customproperty(r'c:\\some\\folder\\file.txt')
         '''
        with open(filename) as customproperties:
            properties = json.loads(customproperties.read())
            data = json.dumps(properties)
            return self.post('qrs/custompropertydefinition/many', data)

    def export_app(self, appid, filepath, filename):
        """
        Exports the Qlik Sense application
        :param appid: The application id name to export
        :param filepath: The path to the file
        :param filename: The path and filename to export the application to
        :usage: export_app(r'8dadc1f4-6c70-4708-9ad7-8eda34da0106', r'c:\\some\folder\\', 'app.qvf')
        """
        exportticket = self.get_exportappticket(appid)
        ticket = (exportticket['value'])
        with open(filepath + filename, 'wb') as file:
            file.write(self.get('qrs/download/app/%s/%s/%s' % (appid, ticket, filename), None, None))
        return ('Application: %s written to %s' % (filename, filepath))

    def ping_proxy(self):
        try:
            return (self.get_qps('qps/user'))
        except requests.exceptions.RequestException as exception:
            return ('Qlik Sense Proxy down')

if __name__ == '__main__':
    qrs = ConnectQlik('qs2.qliklocal.net:4242', ('C:/certs/qs2.qliklocal.net/client.pem',
                                      'C:/certs/qs2.qliklocal.net/client_key.pem'),
           'C:/certs/qs2.qliklocal.net/root.pem')
    if qrs.ping_proxy() == 200:
        print(qrs.get_about())
      
