import os
from app import create_app, db
from app.models import User, Report
from flask.cli import with_appcontext
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('app/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test_coverage(coverage):
    """Run the unit tests with coverage."""
    if coverage:
        import coverage as cov
        COV = cov.coverage(branch=True, include='app/*')
        COV.start()
    
    import unittest
    tests = unittest.TestLoader().discover('app/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    if coverage:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report(directory='htmlcov')
        COV.erase()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Report=Report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
