// TODO Missing HTTP status codes.



## Ping (`api/ping`)

```markdown
GET /api/ping
	Ping the kolomon API.
	
	Request parameters: /
	
	Response:
		{
			message: "Pong!"
		}
```





## Categories (`/api/categories`)

// TODO Maybe we could use just "tags" instead of full-blown registerable categories?

```markdown
GET /api/categories
	Get a list of all available categories.

	Request parameters:
		page: int
    
	Response:
		A list of category objects.
		{
			categories: [
				{
					id: int,
					name: str,
					description: str,
				},
				...
			]
		}


```

```markdown
POST /api/categories
	Submit a new category.

	Request parameters:
		name: str
		description: str
        
    Response:
    	Newly-created category object.
        {
            id: int,
            name: str,
            description: str,
        }
```

```markdown
GET /api/categories/{id}
	Request info on a specific category.

	Request parameters: /
	
	Response:
		Information on the requested category.
        {
            id: int,
            name: str,
            description: str,
        }
```

```markdown
PATCH /api/categories/{id}
	Edit the title or description of a specific category.
	
	Request:
		At least one of `name`, `description` must be provided.
	Request parameters:
		name: Optional[str]
		description: Optional[str]
        
    Response: /
```

```markdown
DELETE /api/categories/{id}
	Delete a specific category.

	Request parameters: /
	
	Response: /
```



## Search (`/api/search`)

```markdown
GET /api/search/quick
	Perform a quick word search.

	Request parameters:
		query: str
        
	Response:
		A list of quick search results ordered by decreasing relevance.
		{
			id: int,
			language: str,
			word: str,
			description: str,
		}
```

```markdown
GET /api/search/full
	Perform a full search, returning translated word pairs if possible.

	Request parameters:
		query: str
	
	Response:
		A list of search result pairs, ordered by decreasing relevance.
        {
        	english (can be null): {
        		id: int,
        		word: str,
        		description: str,
        	},
        	slovene (can be null): {
        		id: int,
        		word: str,
        		description: str,
        	}
        }
        Note: either the english or slovene object must exist (or both; but not neither).
```



## Recent & orphans

```markdown
GET /api/recent
	Request a list of recent edits or creations.

	Request parameters:
		count: int
		order_by: "any" | "edits" | "created"
		
	Response:
		A list of last `count` edits or creations.
        {
        	TODO: Low priority.
        }
```

```markdown
GET /api/orphans
	Request a list of english/slovene words that are missing their counterparts.

	Request parameters:
		count: int
		order_by: "random" | "alphabetical"
		
	Response:
		A list of orphaned words.
        {
        	// Scheme is the same as `/api/search/simple`
        	id: int,
			language: str,
			word: str,
			description: str,
        }
```




## English words (`/api/english`)

```markdown
GET /api/english
	Request a list of all english words in the dictionary (paginated).

	Request parameters:
		page: int
		
	Response:
		A list of english words. This endpoint returns a simple version of the english word schema.
        {
            id: int,
            word: str,
            description: str,
            translation_state: int,
            created_at: int,
            edited_at: int,
        }
```

```markdown
POST /api/english
	Submit a new english word.

	Request parameters:
		word: str
		description: Optional[str]
		// TODO Maybe we could add support for adding categories/links/suggestions/related words directly here, but should we?
		
	Response: /
```

```markdown
GET /api/english/{id}
	Request information about a specific english word.

	Response:
		Information about the requested english word. This endpoint returns the full version of the english word schema.
			{
				id: int,
				word: str,
				description: str,
				translation_state: int,
				translation_comment: str,
				created_at: int,
				edited_at: int,
				edited_by: int, // TODO User ID probably?
				categories: [
					{
						id: int,
						name: str,
						description: str,
					},
					...
				],
				links: [
					{
						title: str,
						url: str,
					},
					...
				],
				suggestions: [
					{
						suggestion: str,
						separate_gender_form: bool,
						comment: str,
						created_at: int,
						edited_at: int,
					},
					...
				],
				related_words: [
					{
						id: int,
						word: str,
					},
					...
				],
			}
```

```markdown
PATCH /api/english/{id}
	Modify an english word or its description.

	Request parameters:
		word: Optional[str]
		description: Optional[str]
		
	Response: /	
```

```markdown
DELETE /api/english/{id}
	Delete a specific english word entry.

	Request parameters: /
	
	Response: /
```



### Translation suggestions

```markdown
GET /api/english/{id}/suggestions
	Request an english word's translation suggestions.
	
	Request parameters: /
	
	Response:
		A list of translation suggestions.
		A single suggestion has this structure:
		{
			id: int,
			suggestion: str,
			comment: str,
			created_at: int,
			edited_at: int,
		}
```

```markdown
POST /api/english/{id}/suggestions
	Submit a new translation suggestion for the english word.
	
	Request parameters:
		suggestion: str
		comment: str
        
    Response: /
    // TODO: POST requests like these could also return the newly-created object (complete with the ID and stuff, but is that useful)?
```

```markdown
GET /api/english/{id}/suggestions/{suggestion_id}
	Get information about a specific translation suggestion.
	
	Request parameters: /
	
	Response:
		Information about the translation suggestion.
		{
			id: int,
			suggestion: str,
			comment: str,
			created_at: int,
			edited_at: int,
		}
```

```markdown
PATCH /api/english/{id}/suggestions/{suggestion_id}
	Edit a suggestion.
	
	Request parameters:
		suggestion: Optional[str]
		comment: Optional[str]
		
	Response: /
```

```markdown
DELETE /api/english/{id}/suggestions/{suggestion_id}
	Delete a suggestion.
	
	Request parameters: /
	
	Response: /
```



### Related words

// TODO This one is a bit different, I'm not sure how to do this best - if there is only a word_id, this is likely the best way.

```markdown
GET /api/english/{id}/related
	Request related words for a specific english word.
	
	Request parameters: /
	
	Response:
		A list of objects containing related words.
		A single related word has this structure:
		{
			word_id: int,
		}
```

```markdown
POST /api/english/{id}/related
	Add a related word to an english entry.
	
	Request parameters:
		word_id: int
    
    Response: /
```

```markdown
DELETE /api/english/{id}/related
	Remove the related word.
	
	Request parameters:
		word_id: int
```



### Links

```markdown
GET /api/english/{id}/links
	Request a list of links associated with this english word.
	
	Request parameters: /
	
	Response:
		A list of links. A single link has this structure:
		{
			id: int,
			title: str,
			url: str,
		}
```

```markdown
POST /api/english/{id}/links
	Add a new link to associate with the specifiec english word.
	
	Request parameters:
		title: str
		url: str
	
	Response: /
```

```markdown
GET /api/english/{id}/links/{link_id}
	Request info about a specific link.
	
	Request parameters: /
	
	Response:
		{
			id: int,
			title: str,
			url: str,
		}
```

```markdown
PATCH /api/english/{id}/links/{link_id}
	Edit a link's title or URL.
	
	Request parameters:
		title: Optional[str]
		url: Optional[str]
	
	Response: /
```

```markdown
DELETE /api/english/{id}/links/{link_id}
	Delete a link associated with an english entry.
	
	Request parameters: /
	
	Response: /
```



### Categories

// TODO not sure yet



### Translation counterparts

```markdown
GET /api/english/{id}/translation
	Request an english word's slovene translation, if available.

	Request parameters: /

	Response:
		Information about the slovene word. This endpoint returns the full slovene word schema:
        {
            id: int,
            word: str,
            description: str,
            created_at: int,
            edited_at: int,
            word_female_form: str,
            
            # hmmm
            type: str,
            
            related_words: [
            	{
                    id: int,
                    word: str,
                },
                ...
            ]
        }
```





## Slovene words (`/api/slovene`)

```markdown
GET /api/slovene
	Request a list of all slovene words in the dictionary (paginated).

	Request parameters:
		page: int
		
	Response:
		A list of slovene words. This endpoint returns a simple version of the slovene word schema:
		{
			id: int,
			word: str,
            description: str,
            created_at: int,
            edited_at: int,
		}
```

```markdown
POST /api/slovene
	Create a new slovene word entry.
	
	Request parameters:
		word: str
		description: str
```

```markdown
GET /api/slovene/{id}
	Request information about a specific slovene word entry.
	
    Request parameters: /
    
    Response:
    	Information about the slovene word. This endpoint returns the full slovene word schema:
        {
            id: int,
            word: str,
            description: str,
            created_at: int,
            edited_at: int,
            word_female_form: str,
            
            # hmmm
            type: str,
            
            related_words: [
            	{
                    id: int,
                    word: str,
                },
                ...
            ]
        }
```

```markdown
PATCH /api/slovene/{id}
	Modify a slovene word or its description.
	
	Request parameters:
		word: Optional[str]
		description: Optional[str]
		
	Response: /	
```

```markdown
DELETE /api/slovene/{id}
	Delete a slovene word entry.
	
	Request parameters: /
	
	Response: /
```



### Related words

// TODO see note for `/api/english/{id}/related`

```markdown
GET /api/slovene/{id}/related
	Request related words for a specific slovene word.
	
	Request parameters: /
	
	Response:
		A list of objects containing related words.
		A single related word has this structure:
		{
			word_id: int,
		}
```

```markdown
POST /api/slovene/{id}/related
	Add a related word to an english entry.
	
	Request parameters:
		word_id: int
    
    Response: /
```

```markdown
DELETE /api/slovene/{id}/related
	Remove the related word.
	
	Request parameters:
		word_id: int
```





