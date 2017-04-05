# Description
Copies an application within Qlik Sense, owner will be SA_Repository


## Endpoint
/qrs/app/{appid}/copy?name={newname}

## Usage
```
"""
:param name: Name of the new application
:param appid: ID of the Qlik Sense application to copy	
"""
qrs.copy_app('ce208cb0-ba39-4320-963c-457255cd2d38', 'CopyApp')
```
## Returns
```
[]
```
