# qrspy (Qlik Sense Repository Python)
Python wrapper for Qlik Sense Repository Service.

# Instructions
1. ensure requests is installed (pip install requests)
2. ensure requests_ntlm is installed (pip install requests_ntlm)
3. export the qlik sense certificates in PEM format to a local folder
4. launch python
5. import qrspy

#Examples

## Instantiate the ConnectQlik class
- parameter1 = server and port
- parameter2 = certificate (pem certificate, pem key), leave blank for windows authentication
- parameter3 = root (pem root certificate), leave blank for windows authentication
- parameter4 = userdirectory (this is optional, if left blank will default to 'INTERNAL')
- parameter5 = userid (this is optional, if left blank will default to 'SA_Repository')
- parameter6 = credential (windows domain and userid to authenticate as), leave blank for certificate auth
- parameter7 = password (windows password), leave blank for certificate auth

### Linux
```
qrs = qrspy.ConnectQlik(server='qs2.qliklocal.net:4242', certificate=('/home/user/Documents/certs/qs2/client.pem', '/home/user/Documents/certs/qs2/client_key.pem'), root='/home/user/Documents/certs/qs2/root.pem')
```
### Windows authenticate with certificates
```
qrs = qrspy.ConnectQlik(server = 'qs2.qliklocal.net:4242', 
                        certificate = ('c:/certs/qs2/client.pem', 'c:/certs/qs2/client_key.pem'), 
                        root = 'c:/certs/qs2/root.pem')
```
### Windows authenticate with Windows Authentication (NTLM)
```
qrs = qrspy.ConnectQlik(server = 'qs2.qliklocal.net:4242', 
                        credential = 'qliklocal\\administrator', 
                        password = 'Qlik1234')
```

## display a list of QRS API endpoints by method
- parameter1 = method
```
method = ['get', 'put', 'post, delete']
    for i in method:
        qrs.get_apiendpoints(i)
```

## export apps in a stream
- parameter1 = appid
- parameter2 = path to export to
- parameter3 = app name
```
apps = qrs.get_app('stream.name eq', 'Monitoring Apps')
    for i in range(len(apps)):
        qrs.export_app(apps[i]['id'], 'c:/dev/export/', r'%s.qvf' % apps[i]['name'])
```  

## get a list of applications that are not published to a stream
```
apps = qrs.get_app()
    for i in range(len(apps)):
        if apps[i]['stream'] is None:
            print (apps[i]['id'] + ' ' + apps[i]['name'])
```

## import the apps in a folder into a server
- parameter1 = name of the application
- parameter2 = path to the file
```
import os
dir = os.listdir('/home/user/Documents/export')
for file in dir:
  if file.endswith('.qvf'):
      qs4.import_app((os.path.splitext(file)[0]), '/home/user/Documents/export/%s' % file)
```

## publish an application to a stream
- parameter1 = appid
- parameter2 = streamid
- parameter3 = new application name 
```
apps = qrs.get_app('Name eq', 'MapIdevio')
appid = apps[0]['id']
stream = qrs.get_stream('Name eq', 'NewStream')
streamid = stream[0]['id']

qrs.publish_app(appid, streamid, 'MapsPub')
```

## migrate applications
- parameter1 = appid
```
apps = qrs.get_app()
    for i in range(len(apps)):
        qrs.migrate_app(apps[0]['id'])
```

## export certificates
- parameter1 = computer name
- parameter2 = password secret file
- parameter3 = include private key (True, False)
- parameter4 = certificate type (Windows, PEM)
```
qrs.export_certificates('PC1', 's', True, 'Windows')
```

## set the server license
- parameter1 = control number
- parameter2 = serial number
- parameter3 = name
- parameter4 = organization
- parameter5 = lef
The lef is optional, if the server has internet connectivity set parameter5 to None.  Otherwise use the following format
"serial\r\nLine1;;;\r\nQlik Sense Enterprise;;;\r\nProductLevel info\r\nToken info;;\r\ntimelimit\r\ncode"

```
qrs.set_license(11111, 123456789, 'Foo', 'Bar', None)
```

## import users from a text file
- import file format
userId,userDirectory,name
humpty, fairytales, humpty dumpty
puss, fairytales, puss in boots
```
qrs.import_users(r'c:\\dev\\csv\\users.txt')
```

## get users id for all users that have user access tokens
- parameter1 = id (set to None for all)
```
x = qrs.get_useraccesstype()
        for i in range(len(x)):
        print (x[i]['id'])
```

## delete all user access tokens
- parameter1 = id
```
x = qrs.get_useraccesstype()
for i in range(len(x)):
    qrs.delete_useraccesstype (x[i]['id'])
```

## import several extensions (in this example Idevio Maps)
- parameter1 = extension path
```
import os
dir = os.listdir('C:\\Dev\\IdevioMaps-QSS-Extensions-5.7.4\\')
for file in dir:
    if file.endswith('.zip'):
        qrs.import_extension('c:\\Dev\\IdevioMaps-QSS-Extensions-5.7.4\\'+file)
```

## get personal sheets
- parameter1 = objId (leave empty for all)
```
appobj = qrs.get_appobject()
```

## publish personal sheet called 'Test Sheet'
```
appobj = qrs.get_appobject()
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.publish_appobject(appobj[i]['id'])
```            

## unpublish sheet called 'Test Sheet'
```
appobj = qrs.get_appobject()
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.unpublish_appobject(o[i]['id'])
            qrs.delete_appobject(o[i]['id'])
```

## delete appobject called 'Test Sheet'
```
appobj = qrs.get_appobject()
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.delete_appobject(o[i]['id'])
```
