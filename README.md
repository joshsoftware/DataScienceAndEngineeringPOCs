Code-analyser/
├── DataScienceAndEngineeringPOCs
│   ├── code_analyzer/
│       ├── .gitignore
│       ├── app.py
│       ├── Config.py
│       ├── models.py  # Data models for submissions, drives, evaluations
│       ├── utils.py   # Helper functions (e.g., hardcoded data, dummy API calls)
│       ├── LLM
│           ├── Client.py
│           ├── Utils/Lib.py
└─          └─ config.py # Configuration settings


## Steps to setup PostgreSQL;

## Prerequisites

- PostgreSQL 15 installed on your machine
- Python 3.10 installed
- Git installed
- Postman installed

## Step 1: Install PostgreSQL

1. **Download PostgreSQL**:
   - Visit the [PostgreSQL Downloads page](https://www.postgresql.org/download/) and download the appropriate installer for your operating system.

2. **Initialize the Database**:
   - During the installation, ensure you set a password for the `postgres` user and remember it, as you will need it to connect to the database.

4. **Start PostgreSQL Server**:
   - Use the following command to start the PostgreSQL server (adjust the paths as needed):

    "pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start"

5. 
**Overview**

This project involves the evaluation and analysis of code submissions using a mock server and a PostgreSQL database. The project ensures secure and accurate handling of submissions, provides evaluations, and manages database transactions effectively.

**Installation**
1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment and activate it.
4. Install the required packages.

**Configuration**
Create a .env file in the project root directory and add the necessary configurations for database and HMAC key.
Ensure your PostgreSQL database is set up and running.

**Usage**
- Start the mock server by running **npm run dev**
- Start the Json server by running **npm run json-server**
- Start the Flask application: **py app.py**
- The application will be accessible at http://127.0.0.1:5000.
- The mock server will be accessible at http://127.0.0.1:8787.
- The Json server will be accessible at http://127.0.0.1:3000.
- The clientapp.py will be accessible at http://127.0.0.1:6000.