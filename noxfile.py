import nox


PYTHON_TEST_VERSIONS = ("3.9", "3.10", "3.11", "3.12", "3.13", "3.14")


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


@nox.session(name="pytest", python=PYTHON_TEST_VERSIONS)
def run_pytest(session):
    session.run("pytest", "tests", external=True)
