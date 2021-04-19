from datetime import datetime
from config import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class Family(db.Model):
    __tablename__ = "family"
    family_id = db.Column(db.Integer, primary_key=True)
    family_name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    materials = db.relationship(
        "Material",
        backref="family",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Material.timestamp)",
    )


class Material(db.Model):
    __tablename__ = "material"
    material_id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey("family.family_id"))
    material_name = db.Column(db.String(32), nullable=False)
    masse_surfacique = db.Column(db.Integer, nullable=False)
    masse_combustible = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class FamilySchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Family
        sqla_session = db.session

    materials = fields.Nested("FamilyMaterialSchema", default=[], many=True)


class FamilyMaterialSchema(ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    material_id = fields.Int()
    family_id = fields.Int()
    material_name = fields.Str()
    masse_surfacique = fields.Int()
    masse_combustible = fields.Int()
    timestamp = fields.Str()


class MaterialSchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Material
        sqla_session = db.session

    family = fields.Nested("MaterialFamilySchema", default=None)


class MaterialFamilySchema(ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    family_id = fields.Int()
    family_name = fields.Str()
    timestamp = fields.Str()
