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
HTTP Status Code
```
