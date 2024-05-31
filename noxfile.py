import nox


@nox.session(name="check")
def ruff_check(session):
    session.run("ruff", "check", "facturxlib", external=True)


@nox.session(name="isort")
def ruff_isort(session):
    session.run("ruff", "check", "--select",  "I", "--fix", "facturxlib", external=True)


@nox.session(name="format")
def ruff_format(session):
    session.run("ruff", "format", "facturxlib", external=True)


@nox.session(name="mypy")
def mypy_check(session):
    session.run("mypy", "facturxlib", external=True)


@nox.session(name="pytest")
def run_pytest(session):
    session.run("pytest", "tests", external=True)
