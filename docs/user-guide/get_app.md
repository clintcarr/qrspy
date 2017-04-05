# Description
Returns the list of applications on the server

## Endpoint
/qrs/app

## Supports filter
True

## Usage
```
qrs.get_app()
```
## Returns
```
[{'id': '8882427d-de1f-4d1a-a30f-4d8bb99258fc', 'name': 'License Monitor', 'appId': '', 'publishTime': '2017-01-18T21:41:25.689Z', 'published': True, 'stream': {'id': 'a70ca8a5-1d59-4cc9-b5fa-6e207978dcaf', 'name': 'Monitoring apps', 'privileges': None}, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}, {'id': 'bbba08d3-42a8-42aa-8fe8-6660eb4edeed', 'name': 'Operations Monitor', 'appId': '', 'publishTime': '2017-01-18T21:41:38.860Z', 'published': True, 'stream': {'id': 'a70ca8a5-1d59-4cc9-b5fa-6e207978dcaf', 'name': 'Monitoring apps', 'privileges': None}, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}, {'id': '3ca17181-0cad-4769-a037-b79c4664bd2c', 'name': 'Contentx', 'appId': '', 'publishTime': '2017-01-19T03:46:31.277Z', 'published': True, 'stream': {'id': 'aaec8d41-5201-43ab-809f-3063750dfafd', 'name': 'Everyone', 'privileges': None}, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}, {'id': '00ee092c-3bf0-4818-b3bd-61fe45846d00', 'name': 'SampleApp', 'appId': '', 'publishTime': '1753-01-01T00:00:00.000Z', 'published': False, 'stream': None, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}, {'id': 'ef1dd8f6-0638-41e5-a473-ce939e708cd8', 'name': 'Sales Dashboard', 'appId': '', 'publishTime': '1753-01-01T00:00:00.000Z', 'published': False, 'stream': None, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}, {'id': '899c4d4f-d8f9-4b2f-b100-274df7387a5e', 'name': '100m', 'appId': '', 'publishTime': '1753-01-01T00:00:00.000Z', 'published': False, 'stream': None, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}]
```
