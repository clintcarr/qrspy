# Description
Deletes content from a specified content library

## Endpoint
/qrs/contentlibrary/{libraryname}/deletecontent?externalpath={contentname}

## Usage
```
"""
:param: libraryname: The name of the library to delete the content from
:param: contentname: The name of the content to deleye

"""
qrs.delete_librarycontent('Library', 'Pic.gif')
```
## Returns
```
HTTP Status Code
```