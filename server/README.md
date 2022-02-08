# Sales Automation - Python 3 (FastAPI)

## Pre-Requisites

- [Python 3.7+](https://www.python.org/downloads/) - used to run the main server locally
- [PostgreSQL 11+](https://www.postgresql.org/download/) - used to run the database for this server

### Database Setup

You'll need PostgreSQL installed on your local machine (see the pre-requisites section). We also recommend you install a CLI to PostgreSQL, like psql, so you can run queries and see what is in the database. You can find instructions on how to install psql [here](https://blog.timescale.com/tutorials/how-to-install-psql-on-mac-ubuntu-debian-windows/).

Once PostgreSQL is installed, you'll need to create a databases for this exercise called `sales_automation`. If you don't like this name, you can change the database name in the [.env](./.env). **Note:** you may have to adjust your postgres credentials to match your setup.

In order to create the database, you can do something like this in psql:

```
psql                                     // To launch the postgres terminal
CREATE DATABASE sales_automation;        // To create the development database
\q                                       // Exit the terminal
```

You can now relaunch the psql terminal and connect to a specific database using a command like `psql -d sales_automation`.

### Virtual environment

Create and activate your virtual environment and install all dependencies with `pip install -r requirements.txt`

Note: you may be prompted to install rust, since the cryptography package [depends on rust](https://cryptography.io/en/latest/faq/#why-does-cryptography-require-rust)

##### Note for VS Code users:

- if it doesn't detect your venv automatically, make sure to set your python environment manually to, for example `server/venv/bin/python`.
- to maximize the typing benefits, it is encouraged to use the Pylance `python.languageServer` vscode setting.

### Seeding the Postgres database

### Create the tables
 
`python db_init.py` (use `python db_init.py drop` to reset the database at any point)

### Populate the seed data

`python seed.py`

### Run the server

`python main.py`


## Auto-generated OpenAPI Documentation

Once you have the server running, go to `localhost:3001/docs` or `localhost:3001/redoc`

## Formatting

[Black](https://pypi.org/project/black/) formatter is included in the environment, and **should be run before committing your code**.

From the server folder run `black .`
