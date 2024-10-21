import pytest
from app import create_app
from models import db, User, Recipe

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

class TestRecipe:
    """Recipe model tests."""

    def test_recipe_creation(self, app):
        """Test creating a recipe."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username="TestUser")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
                title="Sample Recipe",
                instructions="This is a valid recipe instruction with enough characters.",
                minutes_to_complete=45,
                user=user
            )

            db.session.add(recipe)
            db.session.commit()

            assert recipe.id is not None  # Ensure the recipe was created in the database
            assert recipe.user.username == "TestUser"  # Ensure the recipe is associated with the user
