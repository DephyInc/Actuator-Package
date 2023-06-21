import nox


# ============================================
#                    lint
# ============================================
@nox.session
def lint(session: nox.Session) -> None:
    """
    Runs the code linting suite.
    """
    session.install("poetry")
    session.run("poetry", "install", "--all-extras")
    session.run("poetry", "run", "pre-commit", "run", "--all-files")
