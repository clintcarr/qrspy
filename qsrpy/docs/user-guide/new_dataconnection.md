# Description
 Adds a data connection to Qlik Sense

## Endpoint
/qrs/dataconnection/

## Usage
```
"""
:param username: The user the data connection will connect using
:param password: The password of the user to connect
:param name: The name of the data connection
:param connectionstring: The connection string
:param conntype: The type of connection
"""
qrs.new_dataconnection()
```
## Returns
```
[]
```
