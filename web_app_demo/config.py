import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app
app.config['SECRET_KEY'] = 'lorem ipsum dolor sit amet'



# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:///" + os.path.join(basedir, "families.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure the Flask-user settings of the app instance
app.config['USER_APP_NAME'] = 'DEMO'
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)




# Initialize Marshmallow
ma = Marshmallow(app)
