# Connecting to Qlik Sense Server

1. From Powershell or Command Line run Python
2. Import QSR_py
```Import QSR_py```
3. Instantiate the class qrs_py
```
qrs = qrs_py.ConnectQlik('qs2.qliklocal.net:4242',('c:/certs/qs2.qliklocal.net/client.pem',c:/certs/qs2.qliklocal.net/client_key.pem'),
'c:/certs/qs2.qliklocal.net/root.pem')
```
