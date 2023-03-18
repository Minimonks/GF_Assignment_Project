from app import create_app, db
from app.models import User, Role, UserRequest, SoftwareRequest
import click

app  = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, UserRequest=UserRequest, SoftwareRequest=SoftwareRequest)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)