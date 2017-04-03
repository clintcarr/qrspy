# Description
Returns the license that is configured on the server

## Endpoint
/qrs/license

## Usage
```
qrs.get_license()
```
## Returns
```
{'id': 'c517fae1-adbb-4848-b404-1d8a8d3748ad', 'createdDate': '2017-01-18T21:42:01.955Z', 'modifiedDate': '2017-01-18T21:42:01.955Z', 'modifiedByUserName': 'QLIKLOCAL\\administrator', 'lef': 'XXX\r\nInternal Qlik License 2017;;;\r\nQlik Sense Enterprise;;;\r\nPRODUCTLEVEL;50;;2018-01-30\r\nTOKENS;XXX;;\r\nTIMELIMIT;;;XXX-01-30\r\XXX', 'serial': 'XXX', 'check': '1100275618', 'name': 'Qlik', 'organization': 'Qlik', 'product': 2, 'numberOfCores': -1, 'isExpired': False, 'expiredReason': '', 'isBlacklisted': False, 'isInvalid': False, 'privileges': None, 'impactSecurityAccess': False, 'schemaPath': 'License'}
```
