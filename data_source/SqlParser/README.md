# SQL Parser

**SQL Parser** is a Python-based tool for parsing and interacting with SQL databases. This tool currently supports **PostgreSQL** and **MySQL** databases. It allows users to load data, query the database, and retrieve table information with ease.

## Features

- **PostgreSQL and MySQL Support**: Seamlessly interact with PostgreSQL and MySQL databases.
- **Table Listing**: Retrieve the list of all tables from the connected database.
- **Data Loading**: Execute custom SQL queries and load data from the database.
- **Environment Configuration**: Uses `.env` file for secure configuration of database credentials.

## Requirements

To use SQL Parser, you need to install the required dependencies. Install these using the provided `requirements.txt` file.

## Installation

1. Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up your environment variables in a `.env` file (located in the root directory of the project) with the following format:

    ```plaintext
    DB_TYPE=postgresql   # or 'mysql'
    DB_HOST=localhost    # your database host
    DB_PORT=5432         # for PostgreSQL, or 3306 for MySQL
    DB_NAME=your_database_name
    DB_USER=your_username
    DB_PASSWORD=your_password
   ```

