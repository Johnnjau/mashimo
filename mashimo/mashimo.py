import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =
'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)


class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255))

    def __repr__(self):
        return f'Technician({self.name}, {self.service})'


@app.route('/')
def home():
    technicians = Technician.query.all()
    return render_template('home.html', technicians=technicians)


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Technician': Technician}


if __name__ == '__main__':
    app.run(debug=True)
