# Description
Licenses the Qlik Sense Server.  If the server can reach the internet the LEF can be set to None

## Endpoint
/qrs/license?control={control}

## Usage
:param control: License control number
:param serial: License serial number
:param name: License name
:param organization: License organization
:lef: Set to None if server is internet connected else format as this
lef = "line1\{r}\{n}line2\{r}\{n}line3\{r}\{n}line4\{r}\{n}line5\{r}\{n}line6\{r}\{n}line7" (remove {})
"""
```
qrs.set_license({control}, {serial}, {user}, {organization}, {LEF or None})
```
## Returns
```
{'id': 'c517fae1-adbb-4848-b404-1d8a8d3748ad', 'createdDate': '2017-01-18T21:42:01.955Z', 'modifiedDate': '2017-01-18T21:42:01.955Z', 'modifiedByUserName': 'QLIKLOCAL\\administrator', 'lef': 'XXX\r\nInternal Qlik License 2017;;;\r\nQlik Sense Enterprise;;;\r\nPRODUCTLEVEL;50;;2018-01-30\r\nTOKENS;XXX;;\r\nTIMELIMIT;;;XXX-01-30\r\XXX', 'serial': 'XXX', 'check': '1100275618', 'name': 'Qlik', 'organization': 'Qlik', 'product': 2, 'numberOfCores': -1, 'isExpired': False, 'expiredReason': '', 'isBlacklisted': False, 'isInvalid': False, 'privileges': None, 'impactSecurityAccess': False, 'schemaPath': 'License'}
```
