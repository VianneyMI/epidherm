"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_user import current_user, login_required, roles_required


# Local modules
import config


# Get the application instance
connex_app = config.connex_app
print(type(config.app))



# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# Limiter
limiter = Limiter(
    config.app,
    key_func=get_remote_address,
    default_limits=["100 per day", "20 per hour"]
)

# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


# Create a URL route in our application for "/families"
@connex_app.route("/families")
@connex_app.route("/families/<int:family_id>")
@limiter.limit(limiter._default_limits)
@login_required    # User must be authenticated
def families(family_id=""):
    """
    This function just responds to the browser URL
    localhost:5000/families

    :return:        the rendered template "families.html"
    """
    return render_template("families.html", family_id=family_id)


# Create a URL route to the materials page
@connex_app.route("/families/<int:family_id>")
@connex_app.route("/families/<int:family_id>/materials")
@connex_app.route("/families/<int:family_id>/materials/<int:material_id>")
@roles_required('Admin')    # Use of @roles_required decorator
def materials(family_id, material_id=""):
    """
    This function responds to the browser URL
    localhost:5000/materials/<family_id>

    :param family_id:   Id of the family to show materials for
    :return:            the rendered template "materials.html"
    """
    return render_template("materials.html", family_id=family_id, material_id=material_id)


if __name__ == "__main__":
    connex_app.run(debug=True)
