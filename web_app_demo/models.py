from datetime import datetime

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from flask_user import UserManager, UserMixin

from config import db, app

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'))
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


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

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)
