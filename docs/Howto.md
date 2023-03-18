# Instructions for development

## Prerequisites

- Python v3.11+
- Docker
- psql
- folder `local/db` created at project root
- create an `.env` file with the following content

```
PG_PASSWORD=your_postgres_password
DATABASE_URL=postresql_database_uri
FLASK_APP=src/app.py
```

Install project dependencies from `requirements*.txt` files.

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Instructions

Run `docker compose up` in the root folder to start a postgresql container available at localhost:5555. The `data` folder inside the container will be bound to `local/db` folder on the host so there is data persistence.

### Initializing the database
Run the following command in the project root to initialize the database. Rerunning this overwrite existing database.
```sh
./scripts/reset_db.sh
```

Optionally seed test data into the database. Users (-u), quizzers per user (-z) and questions per quiz (-q).
```python
python ./scripts/seed_data.py -u 2 -z 2 -q 5
```

Start app with
```python
flask run
```

## Testing

Project uses Robot Framework to run system tests against the running application. To run the test suite locally use the following command.

```python
python ./scripts/run_tests_py
```

The test report is generated to `test-results` folder.