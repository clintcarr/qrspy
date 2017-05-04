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

    def __init__(self, server, certificate = False, root = False
        ,userdirectory = False, userid = False, credential = False, password = False):
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
                return response.content
            else:
                response = session.get('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
                
                return response.content
        else:
            if filtervalue in [True, False]:
                response = session.get("https://{0}/{1}?filter={2} {3}&xrfkey={4}".format 
                                        (self.server, endpoint, filterparam, filtervalue, xrf), 
                                        headers=headers, verify=self.root, cert=self.certificate)
            else:
                response = session.get("https://{0}/{1}?filter={2} '{3}'&xrfkey={4}".format 
                                        (self.server, endpoint, filterparam, filtervalue, xrf), 
                                        headers=headers, verify=self.root, cert=self.certificate)
            print(response.url)
            return response.content

    def delete(self, endpoint):
        """
        Function that performs DELETE method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint: 
            response = session.delete('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return response.status_code
        else:
            response = session.delete('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return response.status_code

    def put(self, endpoint, data=None):
        """
        Function that performs PUT method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint:
            if data is None:
                response = session.put('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, verify=self.root, cert=self.certificate)
                return response.status_code
            else:
                response = session.put('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data,verify=self.root, cert=self.certificate)

                return response.status_code
        else:
            if data is None:
                response = session.put('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, verify=self.root, cert=self.certificate)
                return response.status_code
            else:
                response = session.put('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data, verify=self.root, cert=self.certificate)
                return response.status_code

    def post(self, endpoint, data=None):
        """
        Function that performs POST method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        :param data: Data that is posted in body of request.
        """
        if '?' in endpoint:
            if data is None:
                response = session.post('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return response.status_code
            else:
                response = session.post('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                print (response.url)
                return response.status_code
        else:
            if data is None:
                response = session.post('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, 
                                                verify=self.root, cert=self.certificate)
                return response.status_code
            else:
                response = session.post('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                                headers=headers, data=data, 
                                                verify=self.root, cert=self.certificate)
                print (response.url)
                return response.status_code

    def get_qps(self, endpoint):
        """
        Function that performs GET method to Qlik Proxy Service endpoints
        :param endpoint: API endpoint path
        """
        server = self.server
        qps = server[:server.index(':')]

        response = session.get('https://{0}/{1}?xrfkey={2}'.format (qps, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
        return response.status_code

    def get_health(self):
        """
        Function to GET the health information from the server
        :returns: JSON data
        """
        server = self.server
        engine = server[:server.index(':')]
        engine += ':4747'
        endpoint = 'engine/healthcheck'
        response = session.get('https://{0}/{1}?xrfkey={2}'.format (engine, endpoint, xrf),
                                        headers=headers, verify=self.root, cert=self.certificate)
        return json.loads(response.text)

    def get_about(self,opt=None):
        """
        Returns system information
        :returns: JSON
        """
        path = 'qrs/about'
        return json.loads(self.get(path).decode('utf-8'))

    def get_app(self, opt=None,filterparam=None, filtervalue=None):
        """
        Returns the applications
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/app'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_dataconnection(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the dataconnections
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/dataconnection'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_user(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the users
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/user'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_license(self):
        """
        Returns the License
        :returns: JSON
        """
        path = 'qrs/license'
        return json.loads(self.get(path).decode('utf-8'))

    def get_lef(self, serial, control, user, organization):
        """
        Gets the LEF from the Qlik license server
        :returns: JSON
        """
        path = 'qrs/license/download?serial={0}&control={1}&user={2}&org={3}'.format (serial, control, user, organization)
        return json.loads(self.get(path).decode('utf-8'))
    
    def get_appcount(self, filterparam=None, filtervalue=None):
        """
        Returns the applications count
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/app/count'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))       

    def get_customproperty(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the custom properties
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/custompropertydefinition'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_tag(self, opt= None, filterparam=None, filtervalue=None):
        """
        Returns the tags
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/tag'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))
    
    def get_task(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the tasks
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/task'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_systemrule(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the system rules
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/systemrule'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_userdirectory(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the user directory
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/userdirectory'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_exportappticket(self, appid):
        """
        Returns the an app export ticket for use in export_app
        :param appid: Application ID for export
        :returns: JSON
        """
        path = 'qrs/app/{0}/export'.format(appid)
        return json.loads(self.get(path).decode('utf-8'))
        
    def get_extension(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the extensions
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/extension'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_stream(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the streams
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/stream'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_servernode(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the server node
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/servernodeconfiguration'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_useraccesstype(self, opt=None,filterparam=None, filtervalue=None):
        """
        Returns the users with user access type
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/license/useraccesstype'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_loginaccesstype(self, opt=None,filterparam=None, filtervalue=None):
        """
        Returns the login access type rule
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/license/loginaccesstype'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_appobject(self, opt=None, filterparam=None, filtervalue=None):
        """
        Returns the application objects
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/app/object'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_apidescription(self, method, filterparam=None, filtervalue=None):
        """
        Returns the APIs of the QRS
        :param method: Method to return (get, put, post, delete)
        :returns: JSON
        """
        path = 'qrs/about/api/description?extended=true&method={0}&format=JSON'.format (method, filterparam, filtervalue)
        return json.loads(self.get(path).decode('utf-8'))

    def get_serverconfig(self):
        """
        Returns the server configuration
        :returns: JSON
        """
        path = 'qrs/servernodeconfiguration/local'
        return json.loads(self.get(path).decode('utf-8')) 

    def get_emptyserverconfigurationcontainer(self):
        """
        Returns an empty server configuration
        :returns: JSON
        """
        path = 'qrs/servernodeconfiguration/local'
        return json.loads(self.get(path).decode('utf-8')) 

    def get_contentlibrary(self, filterparam=None, filtervalue=None):
        """
        Returns the content library
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/contentlibrary'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_appprivileges(self, appid, filterparam=None, filtervalue=None):
        """
        Returns the privileges
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        path = 'qrs/app/{0}/privileges'.format (appid)
        return json.loads(self.get(path , filterparam, filtervalue).decode('utf-8'))

    def delete_user(self, userid):
        """
        Deletes users
        :param userid: user ID to delete
        :returns: HTTP Status Code
        """
        path = 'qrs/user/{0}'.format (userid)
        return self.delete(path)

    def delete_license(self):
        """
        Deletes the server license
        :returns: HTTP Status Code
        """
        qliklicense = self.get_license()
        licenseid = qliklicense['id']
        path = 'qrs/license/{0}'.format (licenseid)
        return self.delete(path)

    def delete_app(self, appid):
        """
        Deletes an application
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}'.format (appid)
        return self.delete(path)

    def delete_stream(self, streamid):
        """
        Deletes a stream
        :returns: HTTP Status Code
        """
        path = 'qrs/stream/{0}'.format (streamid)
        return self.delete(path)

    def delete_tag(self, tagid):
        """
        Deletes an Tag
        :returns: HTTP Status Code
        """
        path = 'qrs/tag/{0}'.format (tagid)
        return self.delete(path)

    def delete_customproperty(self, custompropertyid):
        """
        Deletes a custom property
        :returns: HTTP Status Code
        """
        path = 'qrs/custompropertydefinition/{0}'.format (custompropertyid)
        return self.delete(path)

    def delete_useraccesstype(self, useraccessid):
        """
        Deletes a user access token (quarantine)
        :returns: HTTP Status Code
        """
        path = 'qrs/license/useraccesstype/{0}'.format (useraccessid)
        return self.delete(path)

    def delete_appobject(self, objectid):
        """
        Deletes an application object
        :returns: HTTP Status Code
        """
        path = 'qrs/app/object/{0}'.format (objectid)
        return self.delete(path)

    def delete_loginaccesstype(self, ruleid):
        """
        Deletes a login access rule
        :returns: HTTP Status Code
        """
        path = 'qrs/license/loginaccesstype/{0}'.format (ruleid)
        return self.delete(path)

    def publish_app(self, appid, streamid, name):
        """
        Publishes an application to a stream
        :param appid: Application ID to publish
        :param streamid: Steam ID of stream to publish application
        :param name: Name of application once published
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}/publish?stream={1}&name={2}'.format (appid, streamid, name)
        return self.put(path)

    def migrate_app(self, appid):
        """
        Migrates an application (usually automatically performed)
        :param appid: Application ID to migrate
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}/migrate'.format (appid)
        return self.put(path) 

    def publish_appobject(self, objid):
        """
        Publishes an application object
        :param objid: Object ID to publish
        :returns: HTTP Status Code
        """
        path = 'qrs/app/object/{0}/publish'.format (objid)
        return self.put(path)

    def unpublish_appobject(self, objid):
        """
        Unpublishes an application object
        :param objid: Object ID to publish
        :returns: HTTP Status Code
        """
        path = 'qrs/app/object/{0}/unpublish'.format (objid)
        return self.put(path)

    def replace_app(self, appid, replaceappid):
        """
        Replaces an application
        :param appid: Application ID to copy
        :param replaceappid: Application ID that is being replaced
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}/replace?app={1}'.format(appid, replaceappid)
        return self.put(path)

    def set_license(self, control, serial, name, organization, lef):
        """
        Sets the Qlik Sense License (if connected to internet omit LEF)
        :param control: Control number of license
        :param serial: Serial Number
        :param name: Name to license to
        :param organization: Organization to license to
        :param lef: LEF in JSON or leave as None to retrieve from Qlik License Server
        :returns: HTTP Status Code
        """
        path = 'qrs/license?control={0}'.format (control)
        if lef is None:
            qliklicense = {
                "serial": serial,
                "name": name,
                "organization": organization
            }
            data = json.dumps(qliklicense)
            return self.post(path, data)
        else:
            qliklicense = {
                "serial": serial,
                "name": name,
                "organization": organization,
                "lef": lef
            }
            data = json.dumps(qliklicense)
            return self.post(path, data)

    def import_users(self, filename):
        """
        Imports users from a text file in comma separated format
        :param filename: filename containing users
        :returns: HTTP Status Code
        """
        path = 'qrs/user'
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post(path, users)
        else:
            path += '/many'
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post(path, users)

    def import_tag(self, filename):
        """
        Imports tags from a text file in comma separated format
        :param filename: filename containing tags
        :returns: HTTP Status Code
        """
        path = 'qrs/tag'
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post(path, tags)
        else:
            path += '/many'
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post(path, tags)

    def start_task(self, taskid):
        """
        Starts a task
        :param taskid: Task ID to start
        :returns: HTTP Status Code
        """
        path = 'qrs/task/{0}/start'.format (taskid)
        return self.post(path)

    def import_extension(self, filename):
        """
        Imports extensions from a zip file
        :param filename: filename containing extension objects
        :returns: HTTP Status Code
        """
        path = 'qrs/extension/upload'
        with open(filename, 'rb') as extension:
            return self.post(path, extension)

    def copy_app(self, appid, name):
        """
        Copies an existing application
        :param appid: Application ID to copy
        :param name: Name of new copy
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}/copy?name={1}'.format (appid, name)
        return self.post(path)

    def new_stream(self, name):
        """
        Creates a new stream
        :param name: Name of stream
        :returns: HTTP Status Code
        """
        path = 'qrs/stream'
        stream = {'name': name}
        data = json.dumps(stream)
        return self.post(path, data)

    def sync_userdirectory(self, userdirectoryid):
        """
        Synchronizes a user directory
        :param userdirectoryid: Userdirectory ID to synchronize
        :returns: HTTP Status Code
        """
        path = 'qrs/userdirectoryconnector/syncuserdirectories'
        udid = '["{0}"]'.format (userdirectoryid)
        return self.post(path, udid)

    def export_certificates(self, machinename, certificatepassword, includesecret, exportformat):
        """
        Exports the Certificates from the Server
        :param machinename: name of the machine to create the certificates for
        :param: certificatepassword: password to secure certificates
        :param includesecret: Boolean for including secret or not
        :param exportformat: Windows or PEM format
        :returns: HTTP Status Code
        """
        path = 'qrs/certificatedistribution/exportcertificates'
        certificateinfo = {"machineNames": [machinename], "certificatePassword": certificatepassword,
                            "includeSecretsKey": includesecret, "ExportFormat": exportformat}
        data = json.dumps(certificateinfo)
        return self.post(path, data)

    def new_node(self, name, hostname, engineenabled, proxyenabled, schedulerenabled, printingenabled):
        """
        Create a new node (not operational)
        """
        path = 'qrs/servernodeconfiguration/container'
        nodedata = {"configuration": {"name": name, "hostName": hostname, "engineEnabled": engineenabled,
                                  "proxyEnabled": proxyenabled, "schedulerEnabled": schedulerenabled,
                                  "printingEnabled": printingenabled}}
        data = json.dumps(nodedata)
        return self.post(path, data)
        # data = container.text
        # jdata = json.loads(data)
        # return jdata["configuration"]["id"]

    def new_dataconnection(self, username, password, name, connectionstring, conntype):
        """
        Creates a new data connection
        :param username: username to run connection string as
        :param password: password of user
        :param name: name of connection string
        :param connectionstring: connection string
        :param conntype: type of connection string
        :returns: HTTP Status Code
        """
        path = 'qrs/dataconnection'
        dataconnection = {
                            "username": username,
                            "password": password,
                            "name": name,
                            "connectionstring": connectionstring,
                            "type": conntype
                        }
        data = json.dumps(dataconnection)
        return self.post(path, data)
  
    def import_app(self, name, filename):
        """
        Imports an application
        :param name: Name of application to import
        :param filename: Path and file of qvf
        :returns: HTTP Status Code
        """
        path = 'qrs/app/upload?name={0}'.format(name)
        headers["Content-Type"] = "application/vnd.qlik.sense.app"
        headers["Connection"] = "Keep-Alive"
        with open(filename, 'rb') as app:
            return self.post(path, app)

    def import_customproperty(self, filename):
        """
        Creates custom properties from file
        :param filename: File containing properties
        :returns: HTTP Status Code
        """
        path = 'qrs/custompropertydefinition/many'
        with open(filename) as customproperties:
            properties = json.loads(customproperties.read())
            data = json.dumps(properties)
            return self.post(path, data)

    def import_librarycontent(self, library, filepath):
        """
        Imports content into a content library
        :param library: library to import content into
        :param filepath: content to import
        :returns: HTTP Status Code
        """
        path = 'qrs/contentlibrary/{0}/uploadfile?externalpath={1}'.format (library, filepath)
        with open(filepath, 'rb') as data:
            return self.post(path, data)

    def reload_app(self, appid):
        """
        Reloads an application
        :param appid: Application ID to reload
        :returns: HTTP Status Code
        """
        path = 'qrs/app/{0}/reload'.format (appid)
        return self.post(path)

    def delete_librarycontent(self, library, contentname):
        """
        Deletes content from a content library
        :param library: library to delete content from
        :param contentname: content to delete
        :returns: HTTP Status Code
        """
        path = 'qrs/contentlibrary/{0}/deletecontent?externalpath={1}'.format (library, contentname)
        return self.delete(path)

    def delete_contentlibrary(self, library):
        """
        Deletes a content library
        :param library: library to delete
        :returns: HTTP Status Code
        """
        path = 'qrs/contentlibrary/{0}'.format (library)
        return self.delete(path)

    def export_app(self, appid, filepath, filename):
        """
        Exports an application to the filepath
        :param appid: application id to export
        :param filepath: location to store the exported app
        :param filename: name of file
        :returns: HTTP Status Code
        """
        path = 'qrs/download/app/{0}/{1}/{2}'.format (appid, ticket, filename)
        exportticket = self.get_exportappticket(appid)
        ticket = (exportticket['value'])
        data = self.get(path)
        with open(filepath + filename, 'wb') as file:
            file.write(data)
        return 'Application: {0} written to {1}'.format (filename, filepath)

    def delete_userdirectoryandusers(self, userdirectoryid):
        """
        Deletes specified user directory and all users within
        :param userdirectoryid: ID of user directory to delete
        :returns: HTTP Status Code
        """
        path = 'qrs/userdirectoryconnector/deleteudandusers?userdirectoryid={0}'.format (userdirectoryid)
        return self.delete(path)

    def delete_userdirectory(self, userdirectoryid):
        """
        Deletes specified user directory
        :param userdirectoryid: ID of userdirectory to delete
        :returns: HTTP Status Code
        """
        path = 'qrs/userdirectory/{0}'.format (userdirectoryid)
        return self.delete(path)

    def ping_proxy(self):
        """
        Returns status code of Proxy service
        :returns: HTTP Status Code
        """
        path = 'qps/user'
        try:
            return self.get_qps(path)
        except requests.exceptions.RequestException as exception:
            return 'Qlik Sense Proxy down'

    def new_systemrule(self, filename=None, category=None, name=None,
                        rule=None, resourcefilter=None, actions=None, comment=None, disabled=None):
        """
        Creates system rules from provided text file
        :param filename: file containing rule (optional)
        :param category: category of rule (Security, Sync, License)
        :param name: Name of the rule
        :param rule: Conditions of the rule
        :param resourcefilter: Resource filter to apply
        :param actions: Actions for rule (INT)
        :param comment: Comment
        :param disabled: Boolean
        :returns: HTTP Status Code
        """
        path = 'qrs/systemrule'
        if filename is None:
            data = {"category": category, 
                    "type": "Custom", 
                    "name": name, 
                    "rule": rule, 
                    "resourceFilter": resourcefilter, 
                    "actions": actions, 
                    "comment": comment, 
                    "disabled": disabled}
            json_data = json.dumps(data)
            return self.post(path, json_data)
        else:
            if self.csvrowcount(filename) == 1:
                with open(self.concsvjson(filename), 'rb') as systemrule:
                    response = json.loads(systemrule.read())
                    data = (json.dumps(response[0]))
                    return self.post(path, data)
            else:
                path += '/many'
                with open(self.concsvjson(filename), 'rb') as systemrule:
                    response = json.loads(systemrule.read())
                    data = json.dumps(response)
                    return self.post(path, data)

    def get_virtualproxy(self, opt=None, filterparam=None, filtervalue=None):
        path = 'qrs/virtualproxyconfig'
        if opt:
            path += '/full'
        return json.loads(self.get(path, filterparam, filtervalue).decode('utf-8'))

    def get_proxycertificate(self, opt=None):
        path = 'qrs/proxyservicecertificate'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_taskoperational(self, opt=None):
        path = 'qrs/taskoperational'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def update_userrole(self, user, role):
        """
        Adds the specified role to the specified user
        :param user: The username to update
        :param role: The role to add ('RootAdmin', 'ContentAdmin', 'DeploymentAdmin', 'AuditAdmin', 'SecurityAdmin')
        :returns: HTTP Status Code
        """
        roles = ['RootAdmin', 'ContentAdmin', 'DeploymentAdmin', 'AuditAdmin', 'SecurityAdmin']  
        if role in roles:   
            data = self.get_user(filterparam='name eq', filtervalue=user, opt='full')
            userid = data[0]['id']
            path = 'qrs/user/{0}'.format (userid)
            data[0]['roles'] = ["{0}".format (role)]
            json_data = json.dumps(data[0])
            return self.put(path, json_data)
        else:
            return ('Nonexistent role.')
    
    def get_enum(self, opt=None):
        """
        Return the enums from the about endpoint
        :returns: JSON enum information
        """
        path = 'qrs/about/api/enums'
        return json.loads(self.get(path).decode('utf-8'))

    def update_systemrule(self, rule, disabled=None, tag_name=None):
        """
        Updates system rule specified
        :param disabled: True -disables rule False -enables rule
        :param tag: associates Tag to rule
        :returns: http status
        """
        data = self.get_systemrule(filterparam='name eq', filtervalue=rule, opt='full')
        ruleid = data[0]['id']
        path = 'qrs/systemrule/{0}'.format(ruleid)
        if disabled is not None:
            data[0]['disabled'] = disabled
        if tag_name is not None:
            tag = self.get_tag(filterparam='name eq', filtervalue=tag_name)
            data[0]['tags'] = tag
        json_data = json.dumps(data[0])
        return self.put(path,json_data)

    def get_systeminfo(self, opt=None):
        """
        Returns the system information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/systeminfo'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_engine(self, opt=None):
        """
        Returns the engine information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/engineservice'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_proxy(self, opt=None):
        """
        Returns the proxy information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/proxyservice'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_scheduler(self, opt=None):
        """
        Returns the scheduler information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/schedulerservice'
        if opt:
            path += '/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_servicecluster(self, opt=None):
        """
        Returns the service cluster information (Shared Persistence)
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/servicecluster/full'
        return json.loads(self.get(path).decode('utf-8'))

    def get_systemruleaudit(self, opt=None):
        """
        Generates CSV files on the central node containing all audit information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/systemrule/security/audit/export'
        return json.loads(self.get(path).decode('utf-8'))
        
    def get_repositoryservice(self, opt=None):
        """
        Returns the repository service information
        :param opt: Allows the retrieval of full json response
        :returns: json response
        """
        path = 'qrs/repositoryservice'
        if opt:
            path+= '/full'
        return json.loads(self.get(path).decode('utf-8'))

if __name__ == '__main__':
    qrs = ConnectQlik(server='qs2.qliklocal.net:4242', 
                    certificate=('C:/certs/qs2.qliklocal.net/client.pem',
                                      'C:/certs/qs2.qliklocal.net/client_key.pem'),
                    root='C:/certs/qs2.qliklocal.net/root.pem')

    qrsntlm = ConnectQlik(server='qs2.qliklocal.net', 
                    credential='qliklocal\\administrator',
                    password='Qlik1234')
