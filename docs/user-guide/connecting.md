# Connecting to Qlik Sense Server

1. From Powershell or Command Line run Python
2. Import qrspy
```Import qrspy```
3. Instantiate the class qrspy and authenticate using certificates
```python
qrs = qrspy.ConnectQlik(server='qs2.qliklocal.net:4242',certificate=('c:/certs/qs2.qliklocal.net/client.pem',root=c:/certs/qs2.qliklocal.net/client_key.pem'),
root='c:/certs/qs2.qliklocal.net/root.pem')
```

## Optional
The userdirectory and userid may be specified in the instantiation of the ConnectQlik class.  If these arguments are left blank it will default to 'INTERNAL', 'SA_REPOSITORY'

```python
qrs = qrspy.ConnectQlik(server='qs2.qliklocal.net:4242',certificate=('c:/certs/qs2.qliklocal.net/client.pem',root=c:/certs/qs2.qliklocal.net/client_key.pem'),
'c:/certs/qs2.qliklocal.net/root.pem', userdirectory='QLIK', userid='Administrator')
```
4. Instantiate the class qrspy and authenticate using Windows Authentication (NTLM)
```python
qrs = qrspy.ConnectQlik(server='qs2.qliklocal.net:4242',credential='domain\\userid',
password='password')
```


