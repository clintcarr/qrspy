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
    def headers():
        return {
            "X-Qlik-XrfKey": xrf,
            "Accept": "application/json",
            "X-Qlik-User": "UserDirectory=Internal;UserID=sa_repository",
            "Content-Type": "application/json"
        }

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

    def get(self,endpoint,filterparam, filtervalue):
        if filterparam is None:
            if '?' in endpoint:
                response = requests.get('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=self.headers(), verify=self.root, cert=self.certificate)
                return (response.text)
            else:
                response = requests.get('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=self.headers(), verify=self.root, cert=self.certificate)
                return (response.text)
        else:
            response = requests.get("https://%s/%s?filter=%s '%s'&xrfkey=%s" % 
                (self.server, endpoint, filterparam, filtervalue, xrf), 
                headers=self.headers(), verify=self.root, cert=self.certificate)
            return (response.text)

    def delete(self, endpoint):
        response = requests.delete('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                        headers=self.headers(), verify=self.root, cert=self.certificate)
        return (response.text)

    def put(self, endpoint):
        if '?' in endpoint:
            response = requests.put('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=self.headers(), verify=self.root, cert=self.certificate)
            return (response.text)
        else:
            response = requests.put('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=self.headers(), verify=self.root, cert=self.certificate)
            return (response.text)

    def post(self, endpoint):
        if '?' in endpoint:
            response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=self.headers(), data=self.data, verify=self.root, cert=self.certificate)
            return (response.text)
        else:
            response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                            headers=self.headers(), data=self.data, verify=self.root, cert=self.certificate)
            return (response.text)

    def get_about(self):
        return (self.get('qrs/about', None, None))

    def get_app(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/app', filterparam, filtervalue)))

    def get_dataconnection(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/dataconnection', filterparam, filtervalue)))

    def get_user(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/user', filterparam, filtervalue)))

    def get_license(self):
        try:
            return (json.loads(self.get('qrs/license', None, None)))
        except TypeError:
            return ('Server not licensed')

    def get_lef(self, serial, control, user, organization):
        return self.get('qrs/license/download?serial=%s&control=%s&user=%s&org=%s' % 
            (serial, control, user, organization), None, None)
    
    def get_appcount(self):
        return (json.loads(self.get('qrs/app/count', None, None)))        

    def get_customproperty(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/custompropertydefinition', filterparam, filtervalue)))

    def get_tag(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/tag', filterparam, filtervalue)))
    
    def get_task(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/task', filterparam, filtervalue)))

    def get_securityrule(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/systemrule', filterparam, filtervalue)))

    def get_securityrule(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/userdirectory', filterparam, filtervalue)))

    def get_exportappticket(self, appid):
        response = (json.loads(self.get('qrs/app/%s/export' % appid, None, None))) 
        return response['value']

    def get_extension(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/extension', filterparam, filtervalue)))

    def get_stream(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/stream', filterparam, filtervalue)))

    def get_servernode(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/servernodeconfiguration', filterparam, filtervalue)))

    def get_useraccesstype(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/license/useraccesstype', filterparam, filtervalue)))

    def get_appobject(self, filterparam, filtervalue):
        return (json.loads(self.get('qrs/app/object', filterparam, filtervalue)))

    def get_apidescription(self, method):
        return (json.loads(self.get('qrs/about/api/description?extended=true&method=%s&format=JSON' 
            % method, None, None)))

    def get_serverconfig(self):
        return (json.loads(self.get('qrs/servernodeconfiguration/local', None, None))) 

    def get_emptyserverconfigurationcontainer(self):
        endpoint = 'qrs/servernodeconfiguration/container'
        return (json.loads(self.get('qrs/servernodeconfiguration/local', None, None))) 

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

    def import_users(self, filename):
        """
        Posts users from file into Qlik Sense
        :param filename: Path and filename to txt or csv file containing users
        :example import_users(r'c:\\some\\folder\\file.txt')
        """
        if self.csvrowcount(filename) == 1:
            endpoint = 'qrs/user'
        else:
            endpoint = 'qrs/user/many'
        with open(self.concsvjson(filename), 'rb') as users:
            response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=self.headers(), data=users, verify=self.root, cert=self.certificate)
        return (response.text)

    def set_license(self, control, serial, name, organization, lef):
        """
        Licenses Qlik Sense Server
        :param control: License control number
        :param serial: License serial number
        :param name: License name
        :param organization: License organization
        :lef: Set to None if server is internet connected else format as this
        lef = "line1\{r}\{n}line2\{r}\{n}line3\{r}\{n}line4\{r}\{n}line5\{r}\{n}line6\{r}\{n}line7" (remove {})
        """
        if lef is None:
            endpoint = 'qrs/license?control=%s' % control
            data = {
                "serial": serial,
                "name": name,
                "organization": organization
            }
            response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=self.headers(), data=json.dumps(data), verify=self.root, cert=self.certificate)
            return (response.text)
        else:
            endpoint = 'qrs/license?control=%s' % control
            data = {
                "serial": serial,
                "name": name,
                "organization": organization,
                "lef": lef
            }
            response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=self.headers(), json=data, verify=self.root, cert=self.certificate)
            return (response.text)

    def import_app(self, name, filename):
        """
        Imports a binary QVF Qlik Sense application to Qlik Sense Server
        :param name: The name of the application that will be displayed in Qlik Sense
        :param filename: The path and filename for the QVF file
        """
        endpoint = 'qrs/app/upload?name=%s' % name
        headers = {
            "X-Qlik-XrfKey": xrf,
            "Accept": "application/json",
            "X-Qlik-User": "UserDirectory=Internal;UserID=sa_repository",
            "Content-Type": "application/vnd.qlik.sense.app",
            "Connection": "Keep-Alive"
        }
        with open(filename, 'rb') as app:
            response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=headers, data=app, verify=self.root, cert=self.certificate)
        return (response.text)

    def import_tag(self, filename):
        """
        Imports Tags from a text or csv file
        :param filename: The path and filename of the text or csv file
        :usage import_tag(r'c:\\some\\folder\\file.txt')
        """
        if self.csvrowcount(filename) == 1:
            endpoint = 'qrs/tag'
        else:
            endpoint = 'qrs/tag/many'
        with open(self.concsvjson(filename), 'rb') as tags:
            response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=self.headers(), data=tags, verify=self.root, cert=self.certificate)
        return (response.text)

    def start_task(self, taskid):
        """
        Start a task (for example, a reload task), identified by {id}, so that it runs on a Qlik
                                                                Sense Scheduler Service (QSS).
        :param taskid: id of the task
        """
        endpoint = 'qrs/task/%s/start' % taskid
        response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                 headers=self.headers(), verify=self.root, cert=self.certificate)
        return (response.status_code)

    def export_app(self, appid, filepath, filename):
        """
        Exports the Qlik Sense application
        :param appid: The application id name to export
        :param filepath: The path to the file
        :param filename: The path and filename to export the application to
        :usage: export_app(r'8dadc1f4-6c70-4708-9ad7-8eda34da0106', r'c:\\some\folder\\', 'app.qvf')
        """
        ticket = self.get_exportappticket(appid)
        endpoint = 'qrs/download/app/%s/%s/%s' % (appid, ticket, filename)
        response = requests.get('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                headers=self.headers(), verify=self.root, cert=self.certificate)
        if response.status_code == 200:
            with open(filepath + filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        print (response.status_code)
        print ('Application: %s written to path: %s' % (appid, filepath))

    def import_extension(self, filename):
        """
        Imports the extension to Qlik Sense
        :param filename: The path and filename of the extension (make sure its a zip archive)
        :usage: import_extension(r'c:\\some\folder\\file.zip')
        """
        endpoint = 'qrs/extension/upload'
        with open(filename, 'rb') as extension:
            response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                     headers=self.headers(), data=extension, verify=self.root, cert=self.certificate)
        return (response.text)

    def import_customproperty(self, filename):
        """
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
        """
        endpoint = 'qrs/custompropertydefinition/many'
        with open(filename) as customproperties:
            cpjson = json.loads(customproperties.read())
            response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                          headers=self.headers(), json=cpjson, verify=self.root, cert=self.certificate)

        return (response.text)

    def copy_app(self, name, appid):
        """
        Copies an application within Qlik Ssnese
        :param name: Name of the new application
        :param appid: ID of the Qlik Sense application to copy
        """

        endpoint = 'qrs/app/%s/copy?name=%s' % (appid, name)
        response = requests.post('https://%s/%s&xrfkey=%s' % (self.server, endpoint, xrf),
                      headers=self.headers(), verify=self.root, cert=self.certificate)
        return (response.text)

    
        return (response.text)

    def add_stream(self, name):
        """
        Adds a new Stream to the Qlik Sense server
        :param name: The name of the new Stream
        """
        data = {"name": name}
        endpoint = 'qrs/stream'
        response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                 headers=self.headers(), json=data, verify=self.root, cert=self.certificate)
        return (response.text)

    def sync_userdirectory(self, id):
        """
        Synchronises the user directory specified by the id
        :param id: id of the user directory
        """
        endpoint = 'qrs/userdirectoryconnector/syncuserdirectories'
        udid = '["%s"]' % id
        response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                 headers=self.headers(), data=udid, verify=self.root, cert=self.certificate)
        return (response.status_code)

    def export_certificates(self, machinename, certificatepassword, includesecret, exportformat):
        """
        Exports certificates from the Central Node - saved to C:\ProgramData\Qlik\Sense\Repository\Exported Certificates
        :param machinename: Computername to link to the certificates
        :param certificatepassword: Password to secure certificate private key
        :param includesecret: Include private key (True, False)
        :param exportformat: Format of export (Windows, Pem)
        """
        data = {"machineNames": [machinename], "certificatePassword": certificatepassword,
                "includeSecretsKey": includesecret, "ExportFormat": exportformat}
        endpoint = 'qrs/certificatedistribution/exportcertificates'
        response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                 headers=self.headers(), json=data, verify=self.root, cert=self.certificate)
        if 200 <= response.status_code < 300:
            return ('Certificates exported')

    def add_node(self, name, hostname, engineenabled, proxyenabled, schedulerenabled, printingenabled):
        """
        Adds a node to an existing Qlik Sense site
        :param name: The name of the node
        :param hostname: server hostname / FQDN
        :param engineenabled: Booleen value for whether new node has an engine
        :param proxyenabled: Booleen value for whether new node has an proxy
        :param schedulerenabled: Booleen value for whether new node has an schedulder
        :param printingenabled: Booleen value for whether new node has printing
        """
        endpoint = 'qrs/servernodeconfiguration/container'
        data = {"configuration": {"name": name, "hostName": hostname, "engineEnabled": engineenabled,
                                  "proxyEnabled": proxyenabled, "schedulerEnabled": schedulerenabled,
                                  "printingEnabled": printingenabled}}
        container = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                  headers=self.headers(), json=data, verify=self.root, cert=self.certificate)
        data = container.text
        jdata = json.loads(data)
        return jdata["configuration"]["id"]

    def add_dataconnection(self, username, password, name, connectionstring, conntype):
        """
        Adds a data connection to Qlik Sense
        :param username: The user the data connection will connect using
        :param password: The password of the user to connect
        :param name: The name of the data connection
        :param connectionstring: The connection string
        :param conntype: The type of connection
        :return:
        """
        endpoint = 'qrs/dataconnection/'
        data = {
            "username": username,
            "password": password,
            "name": name,
            "connectionstring": connectionstring,
            "type": conntype
        }
        response = requests.post('https://%s/%s?xrfkey=%s' % (self.server, endpoint, xrf),
                                 headers=self.headers(), json=data, verify=self.root, cert=self.certificate)
        return (response.text)

    def ping_proxy(self):
        """
        This function uses the QPS API to ping the anonymous endpoint /qps/user.  This allows the user 
        to know whether the Qlik Sense Proxy is operational.
        :return: HTTP status code
        """
        server = self.server
        qps = server[:server.index(':')]
        endpoint = '/qps/user'
        try:
            response = requests.get('https://%s/%s/' % (qps, endpoint), verify=self.root, cert=self.certificate)
            return (response.status_code)
        except requests.exceptions.RequestException as exception:
            return ('Qlik Sense Proxy down')

if __name__ == '__main__':
    qrs = ConnectQlik('qs2.qliklocal.net:4242', ('C:/certs/qs2.qliklocal.net/client.pem',
                                      'C:/certs/qs2.qliklocal.net/client_key.pem'),
           'C:/certs/qs2.qliklocal.net/root.pem')
    if qrs.ping_proxy() == 200:
        print(qrs.get_about())

        #qrs.delete_license()
        print(qrs.set_license(57486, 9999000000001069, 'Qlik', 'Qlik', None))

        print (qrs.get_license())
        