# qlik-qsr-python
Python wrapper for Qlik Sense Repository Service.

## example - export apps in a stream

qs2 = qrs_py.ConnectQlik('qs2.qliklocal.net:4242', ('/home/user/Documents/certs/qs2/client.pem', '/home/user/Documents/certs/qs2/client_key.pem'), '/home/user/Documents/certs/qs2/root.pem')

apps = qs2.get_app('stream.name eq', 'QlikStream1')

for k, v in apps.iteritems():

  qs2.export_app(k, '/home/user/Documents/export/', r'%s.qvf' % v)
  

## example - import apps into a new server

qs4 = qrs_py.ConnectQlik('qs4.qliklocal.net:4242', ('/home/user/Documents/certs/qs4/client.pem', '/home/user/Documents/certs/qs4/client_key.pem'), '/home/user/Documents/certs/qs4/root.pem')

import os

for file in files os.listdir('/home/user/Documents/export'):

  if file.endswith('.qvf'):
  
    qs4.import_app((os.path.splitext(file)[0]), '/home/user/Documents/export/%s' % file)


