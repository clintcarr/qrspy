# Description
Returns the tasks

## Endpoint
/qrs/task

## Supports filter
True

## Usage
```
qrs.get_task()
```
## Returns
```
[{'id': '96e580be-8d71-4bbb-8a7f-0609633e4ebc', 'operational': {'id': 'f6fe824b-271b-4980-ad27-e6751ec953fc', 'lastExecutionResult': {'id': '9c100694-6369-4eb7-8537-3dc2e62ed4ef', 'executingNodeName': '', 'status': 7, 'startTime': '2017-01-20T01:46:27.831Z', 'stopTime': '2017-01-20T01:47:17.615Z', 'duration': 49784, 'fileReferenceID': '2030ee32-cd06-4bb6-8960-37320c7eb68a', 'scriptLogAvailable': False, 'details': [{'id': 'e8e2dd10-3930-46ca-babf-5afcde9e0886', 'detailsType': 2, 'message': 'Changing task state to Triggered', 'detailCreatedDate': '2017-01-20T01:46:28.645Z', 'privileges': None}, {'id': 'e2db88ed-4b81-404c-8964-a3b2ca2a569d', 'detailsType': 2, 'message': 'Trying to start task. Sending task to slave-node qs2.qliklocal.net', 'detailCreatedDate': '2017-01-20T01:46:28.869Z', 'privileges': None}, {'id': 'b695ead8-4d6a-42fd-a79d-0313b3db9e5b', 'detailsType': 2, 'message': 'Changing task state 
```
