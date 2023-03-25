from invoke import task


@task
def test(ctx, include=""):
    ctx.run("rm -rf test-results/")
    ctx.run(f"python tests/run_tests.py {include}")


@task
def start(ctx):
    ctx.run("flask run --debug")
