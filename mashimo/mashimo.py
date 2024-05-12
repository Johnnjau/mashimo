import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Technician, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Technician': Technician, 'User': User, 'Post': Post}

