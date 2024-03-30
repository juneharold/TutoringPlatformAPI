from flask import Flask, render_template
from models import db
from api.tutor_api import tutor_api
from api.tutee_api import tutee_api
from models.models import Tutor, Tutee

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the database to the app
db.init_app(app)

# Register Blueprints
app.register_blueprint(tutor_api, url_prefix='/api')
app.register_blueprint(tutee_api, url_prefix='/api')


def populate_dummy_users():
    """
    adds two tutors and two tutees so that the platform has some users
    """
    if Tutor.query.count() == 0:
        tutor1 = Tutor(name="John Doe", type="tutor")  # id = 1
        tutor2 = Tutor(name="Jane Smith", type="tutor")  # id = 2
        tutee1 = Tutee(name="George Brown", type="tutee")  # id = 3
        tutee2 = Tutee(name="Harold Davis", type="tutee")  # id = 4

        db.session.add(tutor1)
        db.session.add(tutor2)
        db.session.add(tutee1)
        db.session.add(tutee2)

        db.session.commit()
        print("Added dummy users to the database.")


@app.route('/')
def hello_world():
    return render_template("/index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_dummy_users()
    app.run(debug=True)

