from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields
from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)

    # Step 1: Protect the password_hash property
    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    # Step 2: Set password hash property using bcrypt
    @password_hash.setter
    def password_hash(self, password):
        # Generate the hash and decode it to a string for storage
        hashed = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed.decode('utf-8')

    # Step 3: Authenticate method
    def authenticate(self, password):
        # Check the provided password against the stored hash
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()