# Description
Returns the API endpoints for the Qlik Sense Repository Service

## Endpoint
/qrs/about/api/description?extended=true&method={method}&format=JSON

## Supports filter
False

## Usage
```
"""
:param method: HTTP Methods (GET, POST, DELETE, PUT)
"""
qrs.get_apidescription('GET')
```
## Returns
```
'{"method":"GET","path":"/qrs/about","extended":"[resource=manual, bodytype=Void, returntype=About]"}', '{"method":"GET","path":"/qrs/about/api/default/analyzeraccessgroup?listentries={listentries}","extended":"[resource=manual, bodytype=Void, returntype=LicenseAnalyzerAccessGroup, optional=listentries]"}', '{"method":"GET","path":"/qrs/about/api/default/analyzeraccesstype?listentries={listentries}","extended":"[resource=manual, bodytype=Void, returntype=LicenseAnalyzerAccessType, optional=listentries]"}', '{"method":"GET","path":"/qrs/about/api/default/analyzeraccessusage?listentries={listentries}","extended":"[resource=manual, bodytype=Void, returntype=LicenseAnalyzerAccessUsage, optional=listentries]"}', '{"method":"GET","path":"/qrs/about/api/default/app?listentries={listentries}","extended":"[resource=manual, bodyty
```
