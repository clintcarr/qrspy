# Description
Exports certificates from the Central Node - saved to C:\ProgramData\Qlik\Sense\Repository\Exported Certificates
        
## Endpoint
/qrs/certificatedistribution/exportcertificates

## Usage
```
"""
:param machinename: Computername to link to the certificates
:param certificatepassword: Password to secure certificate private key
:param includesecret: Include private key (True, False)
:param exportformat: Format of export (Windows, Pem)
"""
qrs.export_certificates('ccsurface', 's', 'True', 'Pem')
```
## Returns
```
HTTP Status Code
```
