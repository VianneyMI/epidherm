import os
from datetime import datetime
from config import db
from models import Family, Material

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

db.session.commit()
