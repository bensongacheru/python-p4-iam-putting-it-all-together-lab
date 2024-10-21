from flask import Flask
from models import db

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Example using SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Create the database and tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # Run the app in debug mode
