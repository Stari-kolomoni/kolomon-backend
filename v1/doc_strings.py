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


ENTRY_CREATE = "Creates a new entry. Requires 'lemma' field, the rest is optional (if supported and the 'language' " \
               "attribute is specified, it handles additional row insertions in language tables)."
LINK_CREATE = "Creates a new link and adds it to the entry with given ID. Only 'url' field is required, " \
              "the rest is optional."
GET_ENTRY_PAIR = "Gets a pair entry-translation together with status of translation. Translation and its state are " \
                 "allowed to be null if not found. If main entry is not found, 404 is raised."
CREATE_SUGGESTION = "Links two entries together into a suggestion. Parent entry ID should be specified as <entry_id> " \
                    "and the suggested translation ID should be given as a query parameter."
CREATE_TRANSLATION = "Links two entries into translation. Parent entry ID should be specified as <entry_id> " \
                     "and the translation ID should be given as a query parameter."
CREATE_RELATION = "Make one-sided relation between two entries. Parent entry ID should be specified as <entry_id> " \
                  "and the child ID should be given as a query parameter."
