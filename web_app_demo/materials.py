"""
This is the families module and supports all the REST actions for the
families data
"""

from flask import make_response, abort
from config import db
from models import Family, Material, MaterialSchema


def read_all():
    """
    This function responds to a request for /api/families/materials
    with the complete list of materials, sorted by material timestamp

    :return:                json list of all materials for all families
    """
    # Query the database for all the materials
    materials = Material.query.order_by(Material.family_id, Material.material_name).all()

    # Serialize the list of materials from our data
    material_schema = MaterialSchema(many=True, exclude=["family.materials"])
    data = material_schema.dump(materials).data
    return data


def read_one(family_id, material_id):
    """
    This function responds to a request for
    /api/families/{family_id}/materials/{material_id}
    with one matching material for the associated family

    :param family_id:       Id of family the material is related to
    :param material_id:         Id of the material
    :return:                json string of material contents
    """
    # Query the database for the material
    material = (
        Material.query.join(Family, Family.family_id == Material.family_id)
        .filter(Family.family_id == family_id)
        .filter(Material.material_id == material_id)
        .one_or_none()
    )

    # Was a material found?
    if material is not None:
        material_schema = MaterialSchema()
        data = material_schema.dump(material).data
        return data

    # Otherwise, nope, didn't find that material
    else:
        abort(404, f"Material not found for Id: {material_id}")


def create(family_id, material):
    """
    This function creates a new material related to the passed in family id.

    :param family_id:       Id of the family the material is related to
    :param material:            The JSON containing the material data
    :return:                201 on success
    """
    # get the parent family
    family = Family.query.filter(Family.family_id == family_id).one_or_none()

    # Was a family found?
    if family is None:
        abort(404, f"Family not found for Id: {family_id}")

    # Create a material schema instance
    schema = MaterialSchema()
    new_material = schema.load(material, session=db.session).data

    # Add the material to the family and database
    family.materials.append(new_material)
    db.session.commit()

    # Serialize and return the newly created material in the response
    data = schema.dump(new_material).data

    return data, 201


def update(family_id, material_id, material):
    """
    This function updates an existing material related to the passed in
    family id.

    :param family_id:       Id of the family the material is related to
    :param material_id:         Id of the material to update
    :param content:            The JSON containing the material data
    :return:                200 on success
    """
    update_material = (
        Material.query.filter(Family.family_id == family_id)
        .filter(Material.material_id == material_id)
        .one_or_none()
    )

    # Did we find an existing material?
    if update_material is not None:

        # turn the passed in material into a db object
        schema = MaterialSchema()
        update = schema.load(material, session=db.session).data

        # Set the id's to the material we want to update
        update.family_id = update_material.family_id
        update.material_id = update_material.material_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated material in the response
        data = schema.dump(update_material).data

        return data, 200

    # Otherwise, nope, didn't find that material
    else:
        abort(404, f"Material not found for Id: {material_id}")


def delete(family_id, material_id):
    """
    This function deletes a material from the material structure

    :param family_id:   Id of the family the material is related to
    :param material_id:     Id of the material to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the material requested
    material = (
        Material.query.filter(Family.family_id == family_id)
        .filter(Material.material_id == material_id)
        .one_or_none()
    )

    # did we find a material?
    if material is not None:
        db.session.delete(material)
        db.session.commit()
        return make_response(
            "Material {material_id} deleted".format(material_id=material_id), 200
        )

    # Otherwise, nope, didn't find that material
    else:
        abort(404, f"Material not found for Id: {material_id}")
