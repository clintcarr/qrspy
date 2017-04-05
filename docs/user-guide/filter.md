# Optional Parameters

##Filtering GET requests

By default all GET requests return all the information pertaining to the API Endpoint.

QRSpy supports the use of filtering on most GET functions.

The following format should be used.

## Examples

qrs.get_app(filterparam='Name eq', filtervalue='Operations Monitor')

## Format
[property] [operator] [value]

## Operators

operator | Description
-------- | -----------
eq | equal
ne | Not equal
gt | Greater than
ge | Greater than or equal
lt | Less than
le | Less than or equal
sw | Starts with
ew | Ends with
so | Substring of

## Retrieve all details

By default the APIs will return summarised information.

QRSpy supports the use of retrieving full details.

## Examples

qrs.get_app(opt='full')

