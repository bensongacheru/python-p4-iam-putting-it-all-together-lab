import pytest
from app import create_app
from models import db, User, Recipe
from sqlalchemy.exc import IntegrityError  # Add this import

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

class TestUser:
    """User in models.py"""

    def test_has_attributes(self, app):
        """has attributes username, _password_hash, image_url, and bio."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username="Liz")
            user.set_password("whosafraidofvirginiawoolf")  # Set the password using the method
            
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter(User.username == "Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url is not None  # Check the default value
            assert created_user.bio == ""

            with pytest.raises(AttributeError):
                created_user.password_hash

    def test_requires_username(self, app):
        """requires each record to have a username."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User()  # User without username
            user.set_password("securepassword")  # Set password

            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self, app):
        """requires each record to have a unique username."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user_1 = User(username="Ben")
            user_2 = User(username="Ben")
            user_1.set_password("password1")
            user_2.set_password("password2")

            db.session.add(user_1)
            db.session.commit()  # Commit the first user

            with pytest.raises(IntegrityError):
                db.session.add(user_2)
                db.session.commit()

    def test_has_list_of_recipes(self, app):
        """has records with lists of recipes records attached."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username="Prabhdip")
            user.set_password("securepassword")  # Set password

            recipe_1 = Recipe(
                title="Delicious Shed Ham",
                instructions="This recipe requires you to cook ham for 60 minutes.",
                minutes_to_complete=60,
            )
            recipe_2 = Recipe(
                title="Hasty Party Ham",
                instructions="This recipe requires you to cook ham for 30 minutes.",
                minutes_to_complete=30,
            )

            user.recipes.append(recipe_1)
            user.recipes.append(recipe_2)

            db.session.add(user)
            db.session.commit()

            # check that all were created in db
            assert user.id
            assert recipe_1.id
            assert recipe_2.id

            # check that recipes were saved to user
            assert recipe_1 in user.recipes
            assert recipe_2 in user.recipes
