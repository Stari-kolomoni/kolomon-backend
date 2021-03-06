GET_ROLES = "Retrieves a list of roles. Use 'limit' and 'skip' for pagination."
GET_ROLE = "Retrieves existing role. Role ID required."
POST_ROLE = "Creates a new role. Requires name and permission number, where each bit represent a permission."
PUT_ROLE = "Updates existing role. Role ID required. No field is required, which makes it similar to PATCH method."
DELETE_ROLE = "Deletes an existing role. Role ID required."

# LOGIN = "Uses OAuth2 authentication. Use like in docs. Username and password required."


CREATE_ENTRY = "Creates a new entry. Requires 'lemma' field, the rest is optional (if supported and the 'language' " \
               "attribute is specified, it handles additional row insertions in language tables)."
UPDATE_ENTRY = "Updates entry information. Requires all entry attributes to be passed."
DELETE_ENTRY = "Deletes the entry. Also removes any foreign references to it. If entry is not found, throws 404 error."
LINK_CREATE = "Creates a new link and adds it to the entry with given ID. Only 'url' field is required, " \
              "the rest is optional."
GET_ENTRY_PAIR = "Gets a pair entry-translation together with status of translation. Translation and its state are " \
                 "allowed to be null if not found. If main entry is not found, 404 is raised."
CREATE_SUGGESTION = "Links two entries together into a suggestion. Parent entry ID should be specified as <entry_id> " \
                    "and the suggested translation ID should be given as a query parameter."
CREATE_TRANSLATION = "Links two entries into translation. Parent entry ID should be specified as <entry_id> " \
                     "and the translation ID should be given as a query parameter."
CREATE_RELATION = "Make one-way relation between two entries. Parent entry ID should be specified as <entry_id> " \
                  "and the child ID should be given as a query parameter."
DELETE_SUGGESTION = "Removes specific suggestion with ID <child_id> from entry with ID <entry_id>. Does not care " \
                    "weather suggestion connection already exists."
DELETE_TRANSLATION = "Removes all translations from entry with ID <entry_id>."
DELETE_RELATION = "Removes specific relation with ID <related_id> from entry with ID <entry_id>."
