# Description
Imports a binary QVF Qlik Sense application to Qlik Sense Server

## Endpoint
/qrs/app/upload?name={name}

## Usage
```
"""
:param name: The name of the application that will be displayed in Qlik Sense
:param filename: The path and filename for the QVF file
"""
qrs.import_app('NewApp', 'c:/some/folder/app.qvf')
```
## Returns
```
HTTP Status Code
```

### Note
If the application should be owned by a specific user, include the userdirectory and userid in the instantiation of the class.
