import pytest
from sqlalchemy.exc import IntegrityError
from app import create_app  # Change here to import create_app
from models import db, User, Recipe

@pytest.fixture
def app():
    """Create a Flask application instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests
    with app.app_context():
        db.create_all()  # Create the database tables
        yield app
        db.drop_all()  # Clean up after tests

class TestUser:
    """User model tests."""

    def test_has_attributes(self, app):
        """Test that the User model has the correct attributes."""
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" +
                    """ - March 23, 2011) was a British-American actress. """ +
                    """She began her career as a child actress in the early""" +
                    """ 1940s and was one of the most popular stars of """ +
                    """classical Hollywood cinema in the 1950s. She then""" +
                    """ became the world's highest paid movie star in the """ +
                    """1960s, remaining a well-known public figure for the """ +
                    """rest of her life. In 1999, the American Film Institute""" +
                    """ named her the seventh-greatest female screen legend """ +
                    """of Classic Hollywood cinema."""
            )
            user.set_password("whosafraidofvirginiawoolf")  # Use the method to hash the password
            
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter(User.username == "Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio == \
                """Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" + \
                """ - March 23, 2011) was a British-American actress. """ + \
                """She began her career as a child actress in the early""" + \
                """ 1940s and was one of the most popular stars of """ + \
                """classical Hollywood cinema in the 1950s. She then""" + \
                """ became the world's highest paid movie star in the """ + \
                """1960s, remaining a well-known public figure for the """ + \
                """rest of her life. In 1999, the American Film Institute""" + \
                """ named her the seventh-greatest female screen legend """ + \
                """of Classic Hollywood cinema."""
            
            with pytest.raises(AttributeError):
                created_user.password_hash  # Ensure this raises an error as intended

    # (Include other test methods similarly)

