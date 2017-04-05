# Description
Creates a new System rule


## Endpoint
qrs/systemrule

## file format
category|type|name|rule|resourceFilter|actions|comment|disabled
--------|----|----|----|--------------|-------|-------|--------
Security|Custom|ClintRule4|!user.Anonymous()|App_*|34|Clints new rule|False

## actions
The action column is an enum
None = 0,
Create = 1,
Read = 2,
Update = 4,
Delete = 8,
Export = 16,
Publish = 32,
ChangeOwner = 64,
ChangeRole = 128,
ExportData = 256

to combine actions (for example Read And Create simply add the values. In other words Create = 1, Read = 2 so Read and Create = 3)

## Usage
```
"""
:param filename: file containing rule
"""

qrs.new_systemrule('c:\\some\\folder\\systemrule.txt')
```
## Returns
```
HTTP Status Code
```
