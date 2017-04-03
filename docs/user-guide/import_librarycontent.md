# Description
Imports content to specified content library

## Endpoint
/qrs/contentlibrary/{libraryname}/uploadfile?externalpath={contentname}

## Usage
```
"""
:param: libraryname: The name of the library to import the content into
:param: contentname: The name of the content that will be called in the content library
:param: filename: The file to be imported

"""
qrs.import_librarycontent('Library', 'c:/some/folder/pic.gif', 'Picture.gif')
```
## Returns
```
HTTP Status Code
```