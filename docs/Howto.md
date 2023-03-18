# Instructions for development

## Prerequisites

- Docker
- psql
- folder `local/db` created at project root
- create an `.env` file with the following content

```
PG_PASSWORD=your_password
DATABASE_URL=database_uri_for_postgres_driver
FLASK_APP=src/app.py
```


## Instructions

Run `docker compose up` in the root folder to start a postgresql container available at localhost:5555. The `data` folder inside the container will be bound to `local/db` folder on the host so there is data persistence.

Then running the following command in the project root to initialize the database. Rerunning this will destroy existing database and reset a new one.
```sh
./scripts/reset_db.sh
```

Seed test data into the database. Users (-u), quizzers per user (-z) and questions per quiz (-q).
```python
python ./scripts/seed_data.py -u 2 -z 2 -q 5
```