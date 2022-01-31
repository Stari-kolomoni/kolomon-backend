
GET_USERS = "Retrieves a list of general information about users. Use 'limit' and 'skip' for pagination."
GET_USER = "Retrieves detailed information about existing user. User ID required."
POST_USER = "Creates a new user. Requires username and password, display_name is optional."
PUT_USER = "Updates information about existing user. User ID required. Only display_name and password can be changed." \
           " No field is required, which makes it similar to PATCH method."
DELETE_USER = "Deletes an existing user. User ID required."
GET_USER_ROLES = "Retrieves roles of existing user. User ID required. Use 'limit' and 'skip' for pagination."
POST_USER_ROLES = "Adds new roles to existing user. User ID required. As request body accepts a list of role IDs to" \
                  " append."
DELETE_USER_ROLES = "Removes roles from existing user. User ID required. As request body accepts a list of role IDs" \
                    " to remove."

GET_ROLES = "Retrieves a list of roles. Use 'limit' and 'skip' for pagination."
GET_ROLE = "Retrieves existing role. Role ID required."
POST_ROLE = "Creates a new role. Requires name and permission number, where each bit represent a permission."
PUT_ROLE = "Updates existing role. Role ID required. No field is required, which makes it similar to PATCH method."
DELETE_ROLE = "Deletes an existing role. Role ID required."

LOGIN = "Uses OAuth2 authentication. Use like in docs. Username and password required."
