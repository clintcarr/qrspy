# Description
Returns the data connections from the Qlik Sense Server

## Endpoint
/qrs/dataconnection

## Usage
```
qrs.get_dataconnection()
```
## Returns
```
[{'id': 'eedec08b-4717-468e-9b19-4353273ee1fc', 'name': 'qvd', 'connectionstring': 'd:\\Scalability Tests\\QVD\\', 'type': 'folder', 'engineObjectId': 'eedec08b-4717-468e-9b19-4353273ee1fc', 'username': '', 'password': '', 'logOn': 0, 'architecture': 0, 'privileges': None}, {'id': 'c682b800-bbdd-45e0-a26e-329db38471f3', 'name': 'ValueAdd', 'connectionstring': 'd:\\Scalability Tests\\Apps\\ValueAddedData\\', 'type': 'folder', 'engineObjectId': 'c682b800-bbdd-45e0-a26e-329db38471f3', 'username': '', 'password': '', 'logOn': 0, 'architecture': 0, 'privileges': None}, {'id': '4065146f-a3e8-4ef7-a6f7-2d8429dd2aff', 'name': 'qrs_task', 'connectionstring': 'CUSTOM CONNECT TO "provider=QvRestConnector.exe;url=https://localhost/qrs/task/full;timeout=180;method=GET;autoDetectResponseType=true;keyGenerationStrategy=0;useWindowsAuthentication=true;forceAuthenticationType=false;useCertificate=No;certificateStoreLocation=CurrentUser;certificateStoreName=My;queryParameters=xrfkey%20000000000000000;queryHeaders=X-Qlik-XrfKey%20000000000000000
```
