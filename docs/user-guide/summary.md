# Summary

The functionality of QRSpy is broken up by the HTTP Method the API endpoint requires.

The following table outlines the currently supported processes.

GET 				| PUT 					| POST 					| DELETE
------------ 		| -------------			|--------------------	| 
get_about 			| publish_app 			| set_license			| delete_user
get_app 			| migrate_app 			| import_users 			| delete_license
get_dataconnection	| publish_appobject 	| import_tag 			| delete_app
get_user 			| unpublish_appobject 	| start_task 			| delete_stream
get_license			| replace_app   		| import_extension 		| delete_tag
get_lef				| update_userrole		| copy_app 				| delete_customproperty
get_appcount		| 						| new_stream 			| delete_useraccesstype
get_customproperty	| 						| sync_userdirectory 	| delete_appobject
get_tag				| 						| export_certificates 	| delete_librarycontent
get_task			| 						| new_dataconnection 	| delete_contentlibrary
get_securityrule	| 						| import_app			| delete_loginaccesstype
get_userdirectory	| 						| import_customproperty | delete_userdirectoryandusers
get_extension		| 	 	 	 	 		| import_librarycontent |
get_stream	 		|	 	 	 	 		| reload_app			|
get_servernode		|	 	 	 	 	    | new_system_rule       |
get_useraccesstype 	|	 	 	 	 	 	 
get_appobject	 	| 	 	 	 	 
get_apidescription	| 	 	 	 	 	 
export_app 			|
get_contentlibrary	|
get_appprivileges	|
get_loginaccesstype	|
get_health          |
get_virtual_proxy   |