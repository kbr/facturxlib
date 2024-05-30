import nox


@nox.session(name="check")
def ruff_check(session):
    # local development setup:
    # nox runs from a separate conda environment with also ruff installed.
    # so ruff runs external and no session.install() calls are necessary.
    session.run("ruff", "check", "facturxlib", external=True)


@nox.session(name="isort")
def ruff_isort(session):
    # local development setup:
    # nox runs from a separate conda environment with also ruff installed.
    # so ruff runs external and no session.install() calls are necessary.
    session.run("ruff", "check", "--select",  "I", "--fix", "facturxlib", external=True)


@nox.session(name="format")
def ruff_format(session):
    # local development setup:
    # nox runs from a separate conda environment with also ruff installed.
    # so ruff runs external and no session.install() calls are necessary.
    session.run("ruff", "format", "facturxlib", external=True)


@nox.session(name="mypy")
def mypy_check(session):
    # local development setup:
    # nox runs from a separate conda environment with also ruff installed.
    # so ruff runs external and no session.install() calls are necessary.
    session.run("mypy", "facturxlib", external=True)
