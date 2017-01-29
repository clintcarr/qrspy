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
            response = session.get("https://{0}/{1}?filter={2} '{3}'&xrfkey={4}".format 
                                    (self.server, endpoint, filterparam, filtervalue, xrf), 
                                    headers=headers, verify=self.root, cert=self.certificate)
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

    def put(self, endpoint):
        """
        Function that performs PUT method to Qlik Repository Service endpoints
        :param endpoint: API endpoint path
        """
        if '?' in endpoint:
            response = session.put('https://{0}/{1}&xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
            return response.status_code
        else:
            response = session.put('https://{0}/{1}?xrfkey={2}'.format (self.server, endpoint, xrf),
                                            headers=headers, verify=self.root, cert=self.certificate)
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

    def get_about(self):
        """
        Returns system information
        :returns: JSON
        """
        return json.loads(self.get('qrs/about'))

    def get_app(self, filterparam=None, filtervalue=None):
        """
        Returns the applications
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/app', filterparam, filtervalue))

    def get_dataconnection(self, filterparam=None, filtervalue=None):
        """
        Returns the dataconnections
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/dataconnection', filterparam, filtervalue))

    def get_user(self, filterparam=None, filtervalue=None):
        """
        Returns the users
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/user', filterparam, filtervalue))

    def get_license(self):
        """
        Returns the License
        :returns: JSON
        """
        return json.loads(self.get('qrs/license'))


    def get_lef(self, serial, control, user, organization):
        """
        Gets the LEF from the Qlik license server
        :returns: JSON
        """
        return json.loads(self.get('qrs/license/download?serial={0}&control={1}&user={2}&org={3}'.format 
            (serial, control, user, organization)))
    
    def get_appcount(self, filterparam=None, filtervalue=None):
        """
        Returns the applications count
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/app/count', filterparam, filtervalue))       

    def get_customproperty(self, filterparam=None, filtervalue=None):
        """
        Returns the custom properties
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/custompropertydefinition', filterparam, filtervalue))

    def get_tag(self, filterparam=None, filtervalue=None):
        """
        Returns the tags
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/tag', filterparam, filtervalue))
    
    def get_task(self, filterparam=None, filtervalue=None):
        """
        Returns the tasks
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/task', filterparam, filtervalue))

    def get_systemrule(self, filterparam=None, filtervalue=None):
        """
        Returns the system rules
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/systemrule', filterparam, filtervalue))

    def get_userdirectory(self, filterparam=None, filtervalue=None):
        """
        Returns the user directory
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/userdirectory', filterparam, filtervalue))

    def get_exportappticket(self, appid):
        """
        Returns the an app export ticket for use in export_app
        :param appid: Application ID for export
        :returns: JSON
        """
        return json.loads(self.get('qrs/app/{0}/export'.format(appid)))
        
    def get_extension(self, filterparam=None, filtervalue=None):
        """
        Returns the extensions
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/extension', filterparam, filtervalue))

    def get_stream(self, filterparam=None, filtervalue=None):
        """
        Returns the streams
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/stream', filterparam, filtervalue))

    def get_servernode(self, filterparam=None, filtervalue=None):
        """
        Returns the server node
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/servernodeconfiguration', filterparam, filtervalue))

    def get_useraccesstype(self, filterparam=None, filtervalue=None):
        """
        Returns the users with user access type
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/license/useraccesstype', filterparam, filtervalue))

    def get_loginaccesstype(self, filterparam=None, filtervalue=None):
        """
        Returns the login access type rule
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/license/loginaccesstype', filterparam, filtervalue))

    def get_appobject(self, filterparam=None, filtervalue=None):
        """
        Returns the application objects
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/app/object', filterparam, filtervalue))

    def get_apidescription(self, method):
        """
        Returns the APIs of the QRS
        :param method: Method to return (get, put, post, delete)
        :returns: JSON
        """
        return json.loads(self.get('qrs/about/api/description?extended=true&method={0}&format=JSON'.format 
             (method)))

    def get_serverconfig(self):
        """
        Returns the server configuration
        :returns: JSON
        """
        return json.loads(self.get('qrs/servernodeconfiguration/local')) 

    def get_emptyserverconfigurationcontainer(self):
        """
        Returns an empty server configuration
        :returns: JSON
        """
        return json.loads(self.get('qrs/servernodeconfiguration/local')) 

    def get_contentlibrary(self, filterparam=None, filtervalue=None):
        """
        Returns the content library
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/contentlibrary', filterparam, filtervalue))

    def get_appprivileges(self, appid, filterparam=None, filtervalue=None):
        """
        Returns the privileges
        :param filterparam: Property and operator of the filter
        :param filtervalue: Value of the filter
        :returns: JSON
        """
        return json.loads(self.get('qrs/app/{0}/privileges'.format (appid) , filterparam, filtervalue))

    def delete_user(self, userid):
        """
        Deletes users
        :param userid: user ID to delete
        :returns: HTTP Status Code
        """
         return self.delete('qrs/user/{0}'.format (userid))

    def delete_license(self):
        """
        Deletes the server license
        :returns: HTTP Status Code
        """
        qliklicense = self.get_license()
        licenseid = qliklicense['id']
        return self.delete('qrs/license/{0}'.format (licenseid))

    def delete_app(self, appid):
        """
        Deletes an application
        :returns: HTTP Status Code
        """
        return self.delete('qrs/app/{0}'.format (appid))

    def delete_stream(self, streamid):
        """
        Deletes a stream
        :returns: HTTP Status Code
        """
        return self.delete('qrs/stream/{0}'.format (streamid))

    def delete_tag(self, tagid):
        """
        Deletes an Tag
        :returns: HTTP Status Code
        """
        return self.delete('qrs/tag/{0}'.format (tagid))

    def delete_customproperty(self, custompropertyid):
        """
        Deletes a custom property
        :returns: HTTP Status Code
        """
        return self.delete('qrs/custompropertydefinition/{0}'.format (custompropertyid))

    def delete_useraccesstype(self, useraccessid):
        """
        Deletes a user access token (quarantine)
        :returns: HTTP Status Code
        """
        return self.delete('qrs/license/useraccesstype/{0}'.format (useraccessid))

    def delete_appobject(self, objectid):
        """
        Deletes an application object
        :returns: HTTP Status Code
        """
        return self.delete('qrs/app/object/{0}'.format (objectid))

    def delete_loginaccesstype(self, ruleid):
        """
        Deletes a login access rule
        :returns: HTTP Status Code
        """
        return self.delete('qrs/license/loginaccesstype/{0}'.format (ruleid))

    def publish_app(self, appid, streamid, name):
        """
        Publishes an application to a stream
        :param appid: Application ID to publish
        :param streamid: Steam ID of stream to publish application
        :param name: Name of application once published
        :returns: HTTP Status Code
        """
        return self.put('qrs/app/{0}/publish?stream={1}&name={2}'.format (appid, streamid, name))

    def migrate_app(self, appid):
        """
        Migrates an application (usually automatically performed)
        :param appid: Application ID to migrate
        :returns: HTTP Status Code
        """
        return self.put('qrs/app/{0}/migrate'.format (appid)) 

    def publish_appobject(self, objid):
        """
        Publishes an application object
        :param objid: Object ID to publish
        :returns: HTTP Status Code
        """
        return self.put('qrs/app/object/{0}/publish'.format (objid))

    def unpublish_appobject(self, objid):
        """
        Unpublishes an application object
        :param objid: Object ID to publish
        :returns: HTTP Status Code
        """
        return self.put('qrs/app/object/{0}/unpublish'.format (objid))

    def replace_app(self, appid, replaceappid):"""
        Replaces an application
        :param appid: Application ID to copy
        :param replaceappid: Application ID that is being replaced
        :returns: HTTP Status Code
        """
        return self.put('qrs/app/{0}/replace?app={1}'.format(appid, replaceappid))

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
        if lef is None:
            qliklicense = {
                "serial": serial,
                "name": name,
                "organization": organization
            }
            data = json.dumps(qliklicense)
            return self.post('qrs/license?control={0}'.format (control), data)
        else:
            qliklicense = {
                "serial": serial,
                "name": name,
                "organization": organization,
                "lef": lef
            }
            data = json.dumps(qliklicense)
            return self.post('qrs/license?control={0}'.format (control), data)

    def import_users(self, filename):
        """
        Imports users from a text file in comma separated format
        :param filename: filename containing users
        :returns: HTTP Status Code
        """
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post('qrs/user', users)
        else:
            with open(self.concsvjson(filename), 'rb') as users:
                return self.post('qrs/user/many', users)

    def import_tag(self, filename):
        """
        Imports tags from a text file in comma separated format
        :param filename: filename containing tags
        :returns: HTTP Status Code
        """
        if self.csvrowcount(filename) == 1:
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post('qrs/tag', tags)
        else:
            with open(self.concsvjson(filename), 'rb') as tags:
                return self.post('qrs/tag/many', tags)

    def start_task(self, taskid):
        """
        Starts a task
        :param taskid: Task ID to start
        :returns: HTTP Status Code
        """
        return self.post('qrs/task/{0}/start'.format (taskid))

    def import_extension(self, filename):
        """
        Imports extensions from a zip file
        :param filename: filename containing extension objects
        :returns: HTTP Status Code
        """
        with open(filename, 'rb') as extension:
            return self.post('qrs/extension/upload', extension)

    def copy_app(self, appid, name):
        """
        Copies an existing application
        :param appid: Application ID to copy
        :param name: Name of new copy
        :returns: HTTP Status Code
        """
        return self.post('qrs/app/{0}/copy?name={1}'.format (appid, name))

    def new_stream(self, name):
        """
        Creates a new stream
        :param name: Name of stream
        :returns: HTTP Status Code
        """
        stream = {'name': name}
        data = json.dumps(stream)
        return self.post('qrs/stream', data)

    def sync_userdirectory(self, userdirectoryid):
        """
        Synchronizes a user directory
        :param userdirectoryid: Userdirectory ID to synchronize
        :returns: HTTP Status Code
        """
        udid = '["{0}"]'.format (userdirectoryid)
        return self.post('qrs/userdirectoryconnector/syncuserdirectories', udid)

    def export_certificates(self, machinename, certificatepassword, includesecret, exportformat):
        """
        Exports the Certificates from the Server
        :param machinename: name of the machine to create the certificates for
        :param: certificatepassword: password to secure certificates
        :param includesecret: Boolean for including secret or not
        :param exportformat: Windows or PEM format
        :returns: HTTP Status Code
        """
        certificateinfo = {"machineNames": [machinename], "certificatePassword": certificatepassword,
                            "includeSecretsKey": includesecret, "ExportFormat": exportformat}
        data = json.dumps(certificateinfo)
        return self.post('qrs/certificatedistribution/exportcertificates', data)

    def new_node(self, name, hostname, engineenabled, proxyenabled, schedulerenabled, printingenabled):
        """
        Create a new node (not operational)
        """
        nodedata = {"configuration": {"name": name, "hostName": hostname, "engineEnabled": engineenabled,
                                  "proxyEnabled": proxyenabled, "schedulerEnabled": schedulerenabled,
                                  "printingEnabled": printingenabled}}
        data = json.dumps(nodedata)
        return self.post('qrs/servernodeconfiguration/container', data)
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
        """
        Imports an application
        :param name: Name of application to import
        :param filename: Path and file of qvf
        :returns: HTTP Status Code
        """
        headers["Content-Type"] = "application/vnd.qlik.sense.app"
        headers["Connection"] = "Keep-Alive"
        with open(filename, 'rb') as app:
            return self.post('qrs/app/upload?name={0}'.format(name), app)

    def import_customproperty(self, filename):
        """
        Creates custom properties from file
        :param filename: File containing properties
        :returns: HTTP Status Code
        """
        with open(filename) as customproperties:
            properties = json.loads(customproperties.read())
            data = json.dumps(properties)
            return self.post('qrs/custompropertydefinition/many', data)

    def import_librarycontent(self, library, filepath):
        """
        Imports content into a content library
        :param library: library to import content into
        :param filepath: content to import
        :returns: HTTP Status Code
        """
        with open(filepath, 'rb') as data:
            return self.post('qrs/contentlibrary/{0}/uploadfile?externalpath={1}'.format (library, filepath), data)

    def reload_app(self, appid):
        """
        Reloads an application
        :param appid: Application ID to reload
        :returns: HTTP Status Code
        """
        return self.post('qrs/app/{0}/reload'.format (appid))

    def delete_librarycontent(self, library, contentname):
        """
        Deletes content from a content library
        :param library: library to delete content from
        :param contentname: content to delete
        :returns: HTTP Status Code
        """
        return self.delete('qrs/contentlibrary/{0}/deletecontent?externalpath={1}'.format (library, contentname))

    def delete_contentlibrary(self, library):
        """
        Deletes a content library
        :param library: library to delete
        :returns: HTTP Status Code
        """
        return self.delete('qrs/contentlibrary/{0}'.format (library))

    def export_app(self, appid, filepath, filename):
        """
        Exports an application to the filepath
        :param appid: application id to export
        :param filepath: location to store the exported app
        :param filename: name of file
        :returns: HTTP Status Code
        """
        exportticket = self.get_exportappticket(appid)
        ticket = (exportticket['value'])
        data = self.get('qrs/download/app/{0}/{1}/{2}'.format (appid, ticket, filename))
        with open(filepath + filename, 'wb') as file:
            file.write(data)
        return 'Application: {0} written to {1}'.format (filename, filepath)

    def ping_proxy(self):
        """
        Returns status code of Proxy service
        :returns: HTTP Status Code
        """
        try:
            return self.get_qps('qps/user')
        except requests.exceptions.RequestException as exception:
            return 'Qlik Sense Proxy down'

    def new_systemrule(self, filename):
        """
        Imports system rule (not operational)
        :param filename: file containing rule
        :returns: HTTP Status Code
        """
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

