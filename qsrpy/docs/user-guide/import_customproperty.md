# Description
Imports custom properties into Qlik Sense

## Endpoint
/qrs/custompropertydefinition/many

## Usage
```
"""
:param filename: Path and filename to JSON formatted file
"""
qrs.import_customproperty(r'c:\\some\\folder\\file.txt')
```

## File Format
```
        {
            "name": "FOO",
            "valueType": "BAR",
            "choiceValues":
                ["FOO",
                "BAR"],
            "objectTypes":
                ["App",
                 "RepositoryService"]}
        :usage: 
```

### Object Types
```
"App","ContentLibrary","DataConnection","EngineService","Extension","ProxyService","ReloadTask",
        "RepositoryService","SchedulerService","ServerNodeConfiguration","Stream","User","UserSyncTask",
        "VirtualProxyConfig"
```

## Returns
```
{'buildVersion': '12.14.0.0', 'buildDate': '9/20/2013 10:09:00 AM', 'databaseProvider': 'Devart.Data.PostgreSql', 'nodeType': 1, 'sharedPersistence': True, 'requiresBootstrap': False, 'schemaPath': 'About'}
```
