# Instructions for development

### Prerequisites

- Python v3.11+
- Docker
- psql
- create an `.env` file with the following content

```
PG_PASSWORD=your_postgres_password
DATABASE_URL=postresql_database_uri
SECRET_KEY=cookie_signing_key
FLASK_APP=src/app.py
```

(for testing only)
- Chrome browser
- Chromedriver with matching version

Install project dependencies from `requirements-dev.txt` file. In addition to runtime dependencies, it contains development related libraries that are not used in production installation. Also `psycopg2-binary` is used for easier compatibility between different platforms in development.

```sh
pip install -r requirements-dev.txt
```

## Starting the app

Run `docker compose up` in the root folder to start a postgresql container available at localhost:5555. If you want data persistence, the `data` folder inside the postgres container must be bound to a folder on the host. This is not enabled by default. For docker compose a directive like the following will accomplish this.
```yml
volumes:
- ./folder/on/host:/var/lib/postgresql/data
```

- Run the following command in the project root to initialize the database. Rerunning this will overwrite existing database.
```sh
PGPASSWORD=your_postgres_password ./scripts/reset_db.sh
```

- Start app with
```sh
invoke start
```

## Testing

Project uses Robot Framework to run system tests against the running application. The automated tests support **only Chrome**. You need to have Chrome browser and Chromedriver installed. To run the test suite locally use the following command.

```sh
invoke test

# optionally pass test tags
invoke test --include=some_tag_in_robot_files
```

If you want to see the stuff happening in the browser, comment out the headless option. You can also add some delay after selenium commands using the `DELAY` variable.
```python
# tests/Selenium.py
- self.options.add_argument('--headless')
+ # self.options.add_argument('--headless')

# tests/variables.py
- DELAY = "0 seconds"
+ DELAY = "0.5 seconds"
```

The test report is generated to `test-results` folder.

## CI

In CI environment, tests are run against containerized application. See the `.github/workflows` folder for details of the configuration. In CI a special test-runner container is pulled to run the robot tests in headless mode. It is possible to use the test-runner container against a locally running service. `test-results` folder should exist in the project root before running the tests.

The test-runner container only supports headless.

```sh
docker run --network="host" \
 --volume ./tests:/home/testrunner/tests \
 --volume ./test-results:/home/testrunner/test-results \
 juhanir/test-runner:0.1.2
```

The tests are run on every pull request made in the source repository (owner+collaborators). Target is to always keep it green.

![badge](assets/test_badge.png)