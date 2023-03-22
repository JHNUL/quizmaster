from invoke import task


@task
def test(ctx):
    ctx.run("rm -rf test-results/")
    ctx.run("python tests/run_tests.py")


@task
def start(ctx):
    ctx.run("flask run --debug")
