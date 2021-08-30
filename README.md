# Backend for the website Stari kolomoni

![Bintray](https://img.shields.io/badge/Python-3.9-blue)
![Bintray](https://img.shields.io/badge/Django-3.2.6-yellowgreen)
![Bintray](https://img.shields.io/badge/PostgreSQL-10-yellow)
![Bintray](https://img.shields.io/badge/Poetry-1.1.8-red)

## Project structure
The main project is split into multiple apps, each acting as a more or less
fully independent component. For now only the "Leksikon" app is being developed.

Root folders:
* ``kolomon`` - stores all settings and global urls
* ``leksikon`` - stores all files for Leksikon app

Each app typically has a few files to aid different functionalities:
* ``admin.py`` - covers everything relating to admin management pages (model registration, admin forms...)
* ``apps.py`` - used for app registration in settings
* ``models.py`` - used to register database models
* ``tests.py`` - for possible tests
* ``views.py`` - for serving web pages and data
* ``urls.py`` - for local urls

## Leksikon app
This is the application for English->Slovene translations management.

### The API

The API urls are located in the ``api.py`` file.

|HTTP request | Path  | Description | Parameters |
--- | --- | --- | ---
|GET|/api/english|Returns the list of all English entries||
|POST|/api/english|Adds a new English entry|  |
|GET|/api/english/{id}|Returns the information on the specified English entry| full: boolean <br> &#160;&#160;True: all info <br> &#160;&#160;False: only basics |
|PUT|/api/english/{id}|Edits the specified English entry||
|DELETE|/api/english/{id}|Deletes the specified English entry||
|GET|/api/english/recent|Returns the list of recent English entries|sort_by: str <br> &#160;&#160;"any": recently created or modified <br> &#160;&#160;"edits": recently modified <br> &#160;&#160;"created": recently created|
|GET|/api/english/search|Searches through the English entries|search_term: str|
|GET|/api/english/{id}/suggestions|Returns all suggestions for the given entry||
|POST|/api/english/{id}/suggestions|Adds a new suggestion for the given entry||
|PUT|/api/english/{id}/suggestions/{id}|Edits the specified suggestion||
|DELETE|/api/english/{id}/suggestions/{id}|Deletes the specified suggestion||
|GET|/api/slovene|Returns the list of all Slovene entries||
|POST|/api/slovene|Adds a new Slovene entry||
|GET|/api/slovene/{id}|Returns the information about specified Slovene entry||
|PATCH|/api/slovene/{id}|Edits the specified Slovene entry ||
|DELETE|/api/slovene/{id}|Deletes the specified Slovene entry||
|GET|/api/slovene/recent|Returns the list of recent Slovene entries|sort_by: str <br> &#160;&#160;"any": recently created or modified <br> &#160;&#160;"edits": recently modified <br> &#160;&#160;"created": recently created|
|GET|/api/slovene/search|Searches through the Slovene entries|search_term: str|
|GET|/api/all|Returns the list of all entries||
|GET|/api/recent|Returns the list of all recent entries||
|GET|/api/search|Searches through all possible entries|search_term: str|
|GET|/api/ping|Pong||
|GET|/api/token|Takes a set of user credentials and returns an access and refresh web token pair to prove the authentication of those credentials|username: str <br> password: str|
|GET|/api/token/refresh|Takes a refresh type web token and returns an access type web token if the refresh token is valid|refresh: str|


## Development database
All necessary details for the development database are stored in ``settings.py`` in ``kolomon`` folder.
These details are referenced in following instructions with capitalized names (for example, **NAME**). The settings can be
changed for local development but are advised not to be pushed to the repository to avoid confusion.

Note that it is expected that PostgreSQL is already installed (preferably with PgAdmin) and has been
run at least once.

**TODO:** Figure out a better way for personalized settings (possible external file??).

1. Run the PostgreSQL server on host **HOST** with port **PORT**.
2. Create a new user with the name **USER** and password **PASSWORD**. Make sure to apply all necessary permissions (such as permission to manage databases).
3. Create a new database with the name **NAME** and add **USER** as the owner.
4. ...
5. Profit.


## Running Django server
First make sure that the PostgreSQL server is running. Then run
```shell
$ python manage.py runserver
```
in the console from the root directory. The server should start up.

## Migrations
If you changed the database structure in ``models.py`` in any way,
the migration should be performed. In the root directory run
```shell
$ python manage.py makemigrations
```
in the console.

Once the migrations have been made, they need to be applied. The following step also applies if
the migration was made by someone else and commited to repository (the indicator of these changes
are new files that appear in the ``migrations`` folder inside the app folder.)
To apply these migrations to your local database, simply run
```shell
$ python manage.py migrate
```
in the console from the root directory.

## License
**TODO!!!**

More on OGL: https://www.thearcanelibrary.com/blogs/news/how-to-use-the-open-game-license
