# Description
Imports users from a text file

## Endpoint
/qrs/users

## Usage

```
'''
:param filename: Path and filename to txt or csv file containing users
        :example import_users(r'c:\\some\\folder\\file.txt')
'''
qrs.import_users('c:/some/folder/users.txt')
```

## File format

userID | userDirectory | name
-------| ------------- | -----
user1  | DirectoryName | Bob Smith


## Returns
```
HTTP Status Code
```
