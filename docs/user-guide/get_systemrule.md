# Description
Returns the rules

## Endpoint
/qrs/systemrule

## Supports filter
True

## Usage
```
qrs.get_securityrule()
```
## Returns
```
[{'id': '087cfb97-2d1f-4d74-9500-b180fa0bd4ec', 'category': 'Security', 'type': 'Default', 'name': 'StreamEveryoneAnonymous', 'rule': 'user.IsAnonymous()', 'resourceFilter': 'Stream_aaec8d41-5201-43ab-809f-3063750dfafd', 'actions': 2, 'comment': 'The default stream called Everyone should be visible for anonymous users', 'disabled': False, 'privileges': None}, {'id': '0911753c-58c2-4088-a82b-c0a71ac37956', 'category': 'Security', 'type': 'Default', 'name': 'SecurityAdminServerNodeConfiguration', 'rule': 'user.roles = "SecurityAdmin"', 'resourceFilter': 'ServerNodeConfiguration_*', 'actio
```
