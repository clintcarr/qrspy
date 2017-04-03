# Description
Replaces app 1 with app 2 (app 1 is not removed)

## Endpoint
qrs/app/{appid}/replace?app={replaceappid}

## Usage
```
"""
:param appid: ID of the app to duplicate
:param replaceappid: ID of the app that is to be replaced
"""

qrs.replaceapp('ce208cb0-ba39-4320-963c-457255cd2d38', 'fasdscb0-ba39-4320-963c-457d55cd2328')
```
## Returns
```
HTTP Status Code
```
