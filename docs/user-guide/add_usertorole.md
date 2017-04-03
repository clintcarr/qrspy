# Description
Adds the specified user to a role

## Endpoint
/qrs/user/{userid}

## Note
Only roles of RootAdmin, ContentAdmin, SecurityAdmin, AuditAdmin and DeploymentAdmin are available

## Usage
```
'''
:param user: The user name of the user to update
:param role: The role to add the user to
'''
qrs.update_userrole('user1', 'RootAdmin')
```
## Returns
```
HTTP Status Code
```