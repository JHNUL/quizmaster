from invoke import task


@task
def test(ctx, include=""):
    ctx.run("rm -rf test-results/")
    ctx.run(f"python tests/run_tests.py {include}")


@task
def dev(ctx):
    ctx.run("FLASK_APP=src/app.py LOG_LEVEL=debug flask run --debug")


@task
def start(ctx):
    ctx.run("FLASK_APP=src/app.py flask run")
