<h1 align="center">
    Stari Kolomoni (Backend)
</h1>

<p align="center">
    <span align="center">
        <a href="https://www.python.org/">
            <img src="https://img.shields.io/badge/python-3.9%2B-4584b6?logo=python&logoColor=white"
                 alt="Python 3.9+" />
        </a>
    </span>
    <span align="center">
        <a href="https://python-poetry.org/">
            <img src="https://img.shields.io/badge/package%20manager-Poetry-007fc7?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABH5JREFUeNqsV11rXEUYfmbmnGz3eyvolZVY0QuvAqLEFC9CsQZRJDdCVZDilZf+g+YHVBtvRFC0iEq1FwuCd2UjKBG1dWMxjZuSbEiy2Xw1S4wk3c2e8T1fu3PmnOzZFYfMzszO2Xme93k/5oRBaec+mZfLo0+hZjFASsDyujO3umvLW0ttbenPWdH7Fx9nPiZXCfz0xw6e+62CR9F2D7c7vNGbuk12Bwl1Q2nKb2TUfgQBEK9ieQej5Xs4wyzlAPXQCDIqUNRvENif6UkAnOHGrS08X17EGW51XRAA1pSBrsLJFscq4HTTwDe/72Dszj08JhRfd1yiyd8hpxGNmgPlHgSY12meMHH91jbOLyzjXFI5PKBIBHAwOKIUmYtXgHmTVAKf/VzHk39WMZZiYYuiYiJktU5SxsRAh4h3YjaJz2dreOLuCkaTSnrqIOghf1eBKt48W+1DAXRdYfdcCl/MruFsZRXPpnR3eOdbiHZNMEuKvYMwoILsEqDMQC6Dr2bXMby4jvM5roGd0AF9fS0+CzojC8oi6NF8Gt/+UkN2YQ2vnRYRQan7PhAfMyR/OUYBLwugukFxhUGPp0+heLuO1vw6JnQSVi8icqqPOiC70ndEUFxhf1B64pSJ7+c20bpbw3heBIEsGREj0rZ+pr9ChAhwP4r9zEgmHCI357fRqmxgLCe0i0tPP7zXXyVUMwGKEiozf59UgBD4sbKL1mIdLxQMmAxRwTiFt8K+j1FAaoAy6Ca/alKhsjPk1+U9NCp1PJMVMPzId1Uok/SX+78LQir0+K6jhEvizuo+7i9u4ukUh3BJNMiOycEuo1AKRtxs+kUn6Nkh0/lJpX6AxtI2hhPMBh8n6atxBIwTd1iUW1hQCX+0a4R9VLuN1ZVdZG/ermaOmtWDga/jE1NChl2iP2oIsMMmkpUqZFuOGPl8qXDx68J/IKBc9sw3nGnSa36ggBP1XaT/WoZpmjAyaTCDjzDBSw+9faMwAAEZnjKEM0D96qiJxFIN6ZUNmOkUBHVmq0EpSuMI47z08DvFwoBp6INp6SgVcq1jmGtbyMwvIbl/ACOXBadg5ATOSQVu0mgY9nqE1Cg98u53hcGC0AFiYd83WzC395DYuk8JwMApDRm9wpGl5CnmjHZaMuUNi/6GifOw/joWQUAGwbl07/njFoy9fRiNv2H8c0gFUASA7VTkDgEX3CHAuV+vysTm0uaHL5djFWA7ew1SvoDjNvjhEXjbAn/QhDh64MjLhobAU0nPx9y12u/Ct95e+7coowtITtavTjT6qgPm3MI4N4dKZFnBto4Lw7Uym3UBO104IAES3ty13gGf2nj/wuW4NAxld+qlj530oV5wgAKAQiPhWa4QIQJVioVLtSsvzvTzf0Fkecm88qlHQhQClnM7tVwgTgQgmEqkQcDTtT6sjiXgvAxPXusowXXLgyo0CHyajrq68cGFBgZsvQos8q9/6RQSxx2Ga7VCoEx70yR5sT49MTBwXwTsdvqN674SNugM9R+oF7c+erWK/6H9K8AAjNFYo5qYUdkAAAAASUVORK5CYII=" 
                 alt="Python Package Manager: Poetry" />
        </a>
    </span>
</p>

---

## 1. Project architecture
Built on top of the following main technologies:
- REST API built with Python's [FastAPI](https://fastapi.tiangolo.com/) library ([SQLAlchemy](https://www.sqlalchemy.org/) for database models, [alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations)
- [PostgreSQL](https://www.postgresql.org/)
- [Uvicorn](https://www.uvicorn.org/) web server
- [JWT tokens](https://jwt.io/) for authentication

## 1.1 Structure
The components are split into different parts based on their function. 
The root directory contains:
 - `main.py` - the main script that defines the top-level FastAPI application. 
   Logging initialization, error handling as well as basic API endpoints (i.e. `ping`),
 - `v1` - API logic and data access for API version 1,
 - `tests` - unit and coverage tests,
 - `scripts` - convenience shell scripts for different running or initialization tasks,
 - `data` - local configuration and other persistent data,
 - `core` - core models, schemas and functions used in the entire backend.


### `v1` module
In this folder, the API logic is present. The API is, for the ease of management, split into modules.

The file `api.py` combines and registers endpoints from all modules.

More about `dependencies.py` can be found [here](https://fastapi.tiangolo.com/tutorial/dependencies/).

`doc_string.py` is an inconvenient way the user-friendly text descriptions are stored
(has to be changed later to something more manageable).

Each module is stored in its own directory. It contains DALs (Data Access Layers), which form and send database requests,
and routers, which expose endpoints and check data before processing.
Current modules are:
 - `lex` - The lexicon part of the application; In charge of handling terms, suggestions and translations.
 - `users` - In charge of registration, login, authentication and user management.


### `tests` module

Tests are divided into categories:
 - `model_tests` - concerning model and database fetching behaviour
 - `logic_tests` - concerning server general logic
 - `v1` - concerning API endpoint and schemas behaviour

The tool used for testing is `pytest`. Tests are run by executing
```
> pytest
```
in command line. The database is cleaned before and after testing.

Currently, the tests are executed on development database. *(TODO: Should it be reasonable to add a testing database?)*


### `core` module
Logging configuration (`log.py`), database connection and persistent data (`models`),
data schemas (`schemas`) and exception handlers (`exceptions.py`). 
Other additional configuration is managed in `configuration.py`.

---

## 2. Development
Before running the development server, make sure you have the following prerequisites installed on your system:
- [Python 3.9+](https://www.python.org/)
- [Poetry (package manager)](https://python-poetry.org/)

Clone the repository and execute `poetry install` to create a local virtual Python environment 
and install the project dependencies.

## 2.1. Setup on Windows
- Set up a [PostgreSQL](https://www.postgresql.org/) database locally.  
  a) Installer option: download the PostgreSQL installer and follow the instructions, depending on your platform.  
  b) Portable option: download the [portable binaries](https://www.enterprisedb.com/download-postgresql-binaries) and extracting them into `pgsql` in the main directory.
     Then use the provided `scripts/postgres-init.ps1` and `scripts/postgres-run.ps1` script to initialize and run the database.
- Fill out the configuration.  
  Copy the `data/configuration.TEMPLATE.toml` file to `data/configuration.toml` and fill out the required values (database settings, etc.).
- With the fresh database running, run `alembic upgrade head` to set up database tables.
- To start the development server, use `scripts/kolomoni-run.ps1` or simply run `uvicorn main:app --reload`.

## 2.2. Setup on Linux
> Shouldn't be too different, but TODO.


---


## 3. License
> **TODO!** The license doesn't impact the way we're able to license this software.
> 
> More on OGL: https://www.thearcanelibrary.com/blogs/news/how-to-use-the-open-game-license 
