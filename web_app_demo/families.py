"""
This is the families module and supports all the REST actions for the
families data
"""

from flask import make_response, abort

from config import db
from models import Family, FamilySchema, Material, MaterialSchema


def read_all():
    """
    This function responds to a request for /api/families
    with the complete lists of families

    :return:        json string of list of families
    """
    # Create the list of families from our data
    families = Family.query.order_by(Family.family_name).all()

    # Serialize the data for the response
    family_schema = FamilySchema(many=True)
    data = family_schema.dump(families).data

    return data


def read_one(family_id):
    """
    This function responds to a request for /api/families/{family_id}
    with one matching family from families

    :param family_id:   Id of family to find
    :return:            family matching id
    """
    # Build the initial query
    family = (
        Family.query.filter(Family.family_id == family_id)
        .outerjoin(Material)
        .one_or_none()
    )

    # Did we find a family?
    if family is not None:

        # Serialize the data for the response
        family_schema = FamilySchema()
        data = family_schema.dump(family).data
        return data

    # Otherwise, nope, didn't find that family
    else:
        abort(404, f"Family not found for Id: {family_id}")


def get_nb_materials(family_id):
    # Build the initial query
    family = (
        Family.query.filter(Family.family_id == family_id)
        .outerjoin(Material)
        .one_or_none()
    )

    # Did we find a family?
    if family is not None:

        # Serialize the data for the response
        #family_schema = FamilySchema()
        #data = family_schema.dump(family).data
        return len(family.materials)

    # Otherwise, nope, didn't find that family
    else:
        abort(404, f"Family not found for Id: {family_id}")

def get_min_ms(family_id):
    material = (
        Material.query.filter(Material.family_id == family_id)
        .outerjoin(Family)
        .order_by(Material.masse_surfacique)
        .first()
    )
    if material is not None:

        return material.masse_surfacique
    else:

        abort(404, f"Family not found for Id: {family_id}")

def get_max_ms(family_id):
    material = (
        Material.query.filter(Material.family_id == family_id)
        .outerjoin(Family)
        .order_by(db.desc(Material.masse_surfacique))
        .first()
    )
    if material is not None:

        return material.masse_surfacique
    else:

        abort(404, f"Family not found for Id: {family_id}")

def get_min_mc(family_id):
    material = (
        Material.query.filter(Material.family_id == family_id)
        .outerjoin(Family)
        .order_by(Material.masse_combustible)
        .first()
    )
    if material is not None:

        return material.masse_combustible
    else:

        abort(404, f"Family not found for Id: {family_id}")

def get_max_mc(family_id):
    material = (
        Material.query.filter(Material.family_id == family_id)
        .outerjoin(Family)
        .order_by(db.desc(Material.masse_combustible))
        .first()
    )
    if material is not None:

        return material.masse_combustible
    else:

        abort(404, f"Family not found for Id: {family_id}")


def create(family):
    """
    This function creates a new family in the families structure
    based on the passed in family data

    :param family:  family to create in families structure
    :return:        201 on success, 406 on family exists
    """
    family_name = family.get("family_name")


    existing_family = (
        Family.query.filter(Family.family_name == family_name)
        .one_or_none()
    )

    # Can we insert this family?
    if existing_family is None:

        # Create a family instance using the schema and the passed in family
        schema = FamilySchema()
        new_family = schema.load(family, session=db.session).data

        # Add the family to the database
        db.session.add(new_family)
        db.session.commit()

        # Serialize and return the newly created family in the response
        data = schema.dump(new_family).data

        return data, 201

    # Otherwise, nope, family exists already
    else:
        abort(409, f"Family {family_name}  exists already")


def update(family_id, family):
    """
    This function updates an existing family in the families structure

    :param family_id:   Id of the family to update in the families structure
    :param family:      family to update
    :return:            updated family structure
    """
    # Get the family requested from the db into session
    update_family = Family.query.filter(
        Family.family_id == family_id
    ).one_or_none()

    # Did we find an existing family?
    if update_family is not None:

        # turn the passed in family into a db object
        schema = FamilySchema()
        update = schema.load(family, session=db.session).data

        # Set the id to the family we want to update
        update.family_id = update_family.family_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated family in the response
        data = schema.dump(update_family).data

        return data, 200

    # Otherwise, nope, didn't find that family
    else:
        abort(404, f"Family not found for Id: {family_id}")

def calculate(family_id):
    nb_materials = get_nb_materials(family_id)
    min_ms = get_min_ms(family_id)
    max_ms = get_max_ms(family_id)
    min_mc = get_min_mc(family_id)
    max_mc = get_max_mc(family_id)

    return ({
        'nb_materials':nb_materials,
        'min_ms':min_ms,
        'max_ms':max_ms,
        'min_mc':min_mc,
        'max_mc':max_mc
    })

def delete(family_id):
    """
    This function deletes a family from the families structure

    :param family_id:   Id of the family to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the family requested
    family = Family.query.filter(Family.family_id == family_id).one_or_none()

    # Did we find a family?
    if family is not None:
        db.session.delete(family)
        db.session.commit()
        return make_response(f"Family {family_id} deleted", 200)

    # Otherwise, nope, didn't find that family
    else:
        abort(404, f"Family not found for Id: {family_id}")
