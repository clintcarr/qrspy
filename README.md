# qlik-qsr-python
Python wrapper for Qlik Sense Repository Service.

# Instructions
1. ensure requests is installed (pip install requests)
2. launch python
3. import qrs_py

#Examples

## Instantiate the ConnectQlik class
```
qs2 = qrs_py.ConnectQlik('qs2.qliklocal.net:4242', ('/home/user/Documents/certs/qs2/client.pem', '/home/user/Documents/certs/qs2/client_key.pem'), '/home/user/Documents/certs/qs2/root.pem')
```
## export apps in a stream
- parameter1 = appid
- parameter2 = path to export to
- parameter3 = app name
```
apps = qs2.get_app('stream.name eq', 'QlikStream1')
for k, v in apps.items():
    qs2.export_app(k, '/home/user/Documents/export/', r'%s.qvf' % v)
```  

## import the apps in a folder into a server
- parameter1 = name of the application
- parameter2 = path to the file
```
import os
for file in files os.listdir('/home/user/Documents/export'):
  if file.endswith('.qvf'):
      qs4.import_app((os.path.splitext(file)[0]), '/home/user/Documents/export/%s' % file)
```

## publish an application to a stream
- parameter1 = appid
- parameter2 = streamid
- parameter3 = new application name 
```
stream = qrs.get_stream('Name eq', 'QlikStream1')
    app = qrs.get_app('Name eq', 'ddo')
    for k,v in app.items():
        qrs.publish_app(k, stream, 'Milas New App')
```

## export certificates
- parameter1 = computer name
- parameter2 = password secret file
- parameter3 = include private key (True, False)
- parameter4 = certificate type (Windows, PEM)
```
qrs.export_certificates('PC1', 's', True, 'Windows')
```
