# Description
Gets the system health


## Endpoint
:4747/engine/healthcheck

## Usage
```

qrs.get_health()
```
## Returns
```
{'version': '12.2.1', 'started': '20170221T171446.000+1100', 'mem': {'comitted': 83.68359375, 'allocated': 219.8203125, 'free': 2444.64453125}, 'cpu': {'total': 0}, 'session': {'active': 0, 'total': 0}, 'apps': {'active_docs': [], 'loaded_docs': [], 'calls': 3039, 'selections': 1}, 'users': {'active': 0, 'total': 0}, 'cache': {'hits': 0, 'lookups': 0, 'added': 0, 'replaced': 0, 'bytes_added': 0}}
[Finished in 0.7s]
```
