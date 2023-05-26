from flask_sqlalchemy import SQLAlchemy
from app.models.base import Base, BaseModel
from app.models.strain import Strain
from app.models.store import Store
from app.models.user import User

db = SQLAlchemy()

class DBStorage:
    """A class representing the database storage.

    This class provides functionality for interacting with the database, including creating and deleting objects,
    querying the database for objects, and committing changes to the database.

    """
    class_dictionary = {
        'Strain': Strain,
        'Store': Store,
        'User': User
    }

    def __init__(self, app):
        """
        Initializes the DBStorage instance.

        Args:
            app: The Flask application instance.
        """
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def new(self, obj):
        """Add a new object to the database.

        Args:
            obj: The object to add.

        """
        db.session.add(obj)

    def save(self):
        """Commit changes to the database."""
        try:
            db.session.commit()
        except Exception as e:
            print("Error committing changes:", e)
            db.session.rollback()

    def delete(self, obj=None):
        """Delete an object from the database.

        Args:
            obj: The object to delete.

        """
        if obj is not None:
            db.session.delete(obj)
