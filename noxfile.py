import nox


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def tests(session: nox.Session) -> None:
    session.install("pytest", "coverage")
    session.install("-e", ".")
    session.run("coverage", "run", "--source", "automapper", "-m", "pytest")
    session.run("coverage", "report", "-m", "--fail-under=100")
