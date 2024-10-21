from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(200), default="default.jpg")
    bio = db.Column(db.Text, default="")
    
    def set_password(self, password):
        """Set the password hash."""
        self._password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check the hashed password."""
        return check_password_hash(self._password_hash, password)

class Recipe(db.Model):
    """Recipe model."""
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='recipes')

User.recipes = db.relationship('Recipe', back_populates='user', lazy=True)
