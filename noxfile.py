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
    session.run("poetry", "install")
    session.run("poetry", "run", "black", "./flexsea")
    session.run("poetry", "run", "pylint", "./flexsea")
