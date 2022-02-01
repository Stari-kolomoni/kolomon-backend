# Backend for the website Stari kolomoni

![Bintray](https://img.shields.io/badge/Python-3.9-blue)
![Bintray](https://img.shields.io/badge/fastapi-0.68.2-yellowgreen)
![Bintray](https://img.shields.io/badge/PostgreSQL-10-yellow)
![Bintray](https://img.shields.io/badge/Poetry-1.1.8-red)

## 1. Project structure

## 2. Development setup (Windows)
- Set up a [PostgreSQL](https://www.postgresql.org/) database locally.  
  a) Installer option: download the PostgreSQL installer and follow the instructions, depending on your platform.  
  b) Portable option: download the [portable binaries](https://www.enterprisedb.com/download-postgresql-binaries) and extracting them into `pgsql` in the main directory.
     Then use the provided `scripts/postgres-init.ps1` and `scripts/postgres-run.ps1` script to initialize and run the database.
- Fill out the configuration.  
  Copy the `data/configuration.TEMPLATE.toml` file to `data/configuration.toml` and fill out the required values (database settings, etc.).
- With the fresh database running, run `alembic upgrade head` to set up database tables.
- To start the development server, use `scripts/kolomoni-run.ps1` or simply run `uvicorn main:app --reload`.


## 3. License
> **TODO!**

More on OGL: https://www.thearcanelibrary.com/blogs/news/how-to-use-the-open-game-license
