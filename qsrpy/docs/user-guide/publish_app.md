# Description
Publishes an application to a stream

## Endpoint
qrs/app/{appid}/publish?stream={streamid}&name={new app name}

## Usage
```
"""
:param appid: ID of the application to publish
:param stream: Stream name to publish the application to
:param name: Name of application once published
"""
qrs.publish_app('00ee092c-3bf0-4818-b3bd-61fe45846d00', '91176367-ce28-4ece-bd0c-668b13ab03dd', 'NewApp')
```
## Returns
```
[]
```
