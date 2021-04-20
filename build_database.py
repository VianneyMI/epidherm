import os
from datetime import datetime

from config import db
from models import Family, Material, User, Role, user_manager

# Data to initialize database with
from data import FAMILIES

# Delete database file if it exists currently
if os.path.exists("families.db"):
    os.remove("families.db")

# Create the database
db.create_all()

# iterate over the FAMILIES structure and populate the database
for family in FAMILIES:
    fam = Family(family_name=family.get("family_name"))

    # Add the materials for the family
    for material in family.get("materials"):
        material_name, masse_surfacique, masse_combustible, timestamp = material
        fam.materials.append(
            Material(
                material_name = material_name,
                masse_surfacique = masse_surfacique,
                masse_combustible = masse_combustible,
                timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
            )
        )
    db.session.add(fam)

# Create 'member@example.com' user with no roles
if not User.query.filter(User.email == 'member@example.com').first():
    user = User(
        email='member@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password('Password1'),
    )
    db.session.add(user)


# Create 'admin@example.com' user with 'Admin' and 'Agent' roles
if not User.query.filter(User.email == 'admin@example.com').first():
    user = User(
        email='admin@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password('Password1'),
    )
    user.roles.append(Role(name='Admin'))
    user.roles.append(Role(name='Agent'))
    db.session.add(user)

db.session.commit()
