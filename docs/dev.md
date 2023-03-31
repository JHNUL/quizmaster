# Instructions for development

## Prerequisites

- Python v3.9+
- Create virtual environment with venv (optional but recommended)
- run `pip install -r requirements-dev.txt`
  <br>Note that `requirements.txt` is for production use and contains minimal dependencies.
- [Docker](https://docs.docker.com/get-docker/) and [docker compose](https://docs.docker.com/compose/install/) (not required if you want to use PostgreSQL installed on your OS)
- PostgreSQL command line tool `psql`.
- create an `.env` file with the following content using your own passwords and secrets

```
PG_PASSWORD=<your_postgres_password_for_user_postgres>
DATABASE_URL=postgresql+psycopg2://postgres:<PG_PASSWORD>@localhost:5432/quizdeveloper
SECRET_KEY=cookie_signing_key
```

- Chrome browser (Optional, for testing)
- [Chromedriver](https://chromedriver.chromium.org/downloads) with matching version, needs to be in path. (Optional, for testing)
- Node.js v18+ (Optional, for building styles with tailwindcss)
  - If building styles, run `npm install` in the `tailwind` folder, then `invoke styles` at the project root. This builds css stylesheets to `src/static/css` folder.

## Starting the app

First, postgres must be running and available at `localhost:5432`. Easy way is to run `docker compose up` in the root folder to start a postgresql container that is isolated from the rest or your system. If you want data persistence, the `data` folder inside the postgres container must be bound to a folder on the host. This is not enabled by default. For docker compose a directive like the following will accomplish this.

```yml
# in the docker-compose.yml
quizdb:
  # ...
  volumes:
    - /folder/on/host:/var/lib/postgresql/data
```

- Once the database service is running it must be initialized. Run the following command in the project root. Rerunning this will overwrite existing database.

```sh
PGPASSWORD=your_postgres_password ./scripts/initialize_db.sh
```

- Start the flask app with

```sh
invoke dev
```

## Testing

This project uses Robot Framework to run system tests against the running application. The automated tests support only Chrome. You need to have Chrome browser and Chromedriver installed. To run the test suite locally use the following command.

```sh
invoke test

# optionally pass test tags
invoke test --include=some_tag_in_robot_files
```

If you want to see the stuff happening in the browser, comment out the headless option.

```python
# tests/Selenium.py
- self.options.add_argument('--headless')
+ # self.options.add_argument('--headless')
```

The test report is generated to `test-results` folder and when accessed in the browser will look something like this, where individual test cases can be expanded and reviewed at keyword level.

![testreport](assets/robot_report.png)
