# qlik-qsr-python
Python wrapper for Qlik Sense Repository Service.

# Instructions
1. ensure requests is installed (pip install requests)
2. export the qlik sense certificates in PEM format to a local folder
3. launch python
4. import qrs_py

#Examples

## Instantiate the ConnectQlik class
### Linux
```
qrs = qrs_py.ConnectQlik('qs2.qliklocal.net:4242', ('/home/user/Documents/certs/qs2/client.pem', '/home/user/Documents/certs/qs2/client_key.pem'), '/home/user/Documents/certs/qs2/root.pem')
```
### Windows
```
qrs = qrs_py.ConnectQlik('qs2.qliklocal.net:4242', ('c:/certs/qs2/client.pem', 'c:/certs/qs2/client_key.pem'), 'c:/certs/qs2/root.pem')
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
apps = qrs.get_app(None, None)
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
apps = qrs.get_app(None, None)
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
x = qrs.get_useraccesstype(None)
j = json.loads(x)
for i in range(len(j)):
    print (j[i]['id'])
```

## delete all user access tokens
- parameter1 = id
```
x = qrs.get_useraccesstype(None)
j = json.loads(x)
for i in range(len(j)):
    qrs.delete_useraccesstype (j[i]['id'])
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
- parameter1 = objId (None for all)
```
appobj = qrs.get_appobject(None)
```

## publish personal sheet called 'Test Sheet'
```
appobj = qrs.get_appobject(None)
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.publish_appobject(appobj[i]['id'])
```            

## unpublish sheet called 'Test Sheet'
```
appobj = qrs.get_appobject(None)
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.unpublish_appobject(o[i]['id'])
            qrs.delete_appobject(o[i]['id'])
```

## delete appobject called 'Test Sheet'
```
appobj = qrs.get_appobject(None)
    for i in range(len(appobj)):
        if appobj[i]['name'] == 'Test Sheet':
            qrs.delete_appobject(o[i]['id'])
```
