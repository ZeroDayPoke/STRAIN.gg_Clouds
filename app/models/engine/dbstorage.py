#!/usr/bin/python3
"""
    DBStorage
    A class representing the database storage.

    This class provides functionality for interacting with the database, including creating and deleting objects, querying the database for objects, and committing changes to the database.

    Attributes
    session (scoped_session): The current database session.
    class_dictionary (dict): A dictionary mapping class names to class objects.
    Methods
    __init__()
    Create a new database engine and session.

    Initializes a new database engine and a new session object.

    reload()
    Reload the session and create all tables in the database.

    This method creates all tables in the database and sets up a new session object.

    new(obj: Base) -> None
    Adds a new object to the database.

    obj: The object to add.
    save() -> None
    Commits changes to the database.

    delete(obj: Base = None) -> None
    Deletes an object from the database.

    obj: The object to delete.
    all(cls: type = None, order_by: str = None, limit: int = None, offset: int = None, relationships: list[str] = None) -> dict[str, Base]
    Returns all objects of the specified class.

    cls: The class of object to retrieve.
    order_by: The attribute to order by.
    limit: The maximum number of objects to return.
    offset: The offset to start returning objects from.
    relationships: A list of relationships to join.
    Returns a dictionary mapping object IDs to objects.

    Raises:

    AttributeError: If the class of object to retrieve is not recognized.
    get(cls: Union[str, type], id: str) -> Union[Base, None]
    Retrieves an object by class and ID.

    cls: The class of object to retrieve.
    id: The ID of the object to retrieve.
    Returns the retrieved object, or None if no object was found.

    Raises:

    AttributeError: If the class of object to retrieve is not recognized.
    count(cls: type = None) -> int
    Counts the number of objects in the database, optionally filtered by class.

    cls: The class of object to count, or None to count all objects.
    Returns the number of objects in the database.

    Raises:

    AttributeError: If the class of object to retrieve is not recognized.
    delete_all(class_name: str) -> Union[str, None]
    Deletes all objects of a specific class from the database.

    class_name: The name of the class to delete objects from.
    Returns an error message if the class is not recognized, or None if the deletion was successful.

    with_session decorator
    A decorator that provides a session object to a function that interacts with the database.

    Arguments
    func: The function that will use the session object.
    Returns
    A wrapped function that has a session object passed as its first argument.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload, Mapped
from app.models.base import Base, BaseModel
from app.models.strain import Strain
from app.models.store import Store
from app.models.user import User


class DBStorage:
    """A class representing the database storage.

    This class provides functionality for interacting with the database, including creating and deleting objects,
    querying the database for objects, and committing changes to the database.

    Attributes:
        session (scoped_session): The current database session.
        class_dictionary (dict): A dictionary mapping class names to class objects.

    Methods:
        new(obj: Base) -> None: Adds a new object to the database.
        save() -> None: Commits changes to the database.
        delete(obj: Base = None) -> None: Deletes an object from the database.
        all(cls: type = None, order_by: str = None, limit: int = None, offset: int = None,
            relationships: list[str] = None) -> dict[str, Base]: Returns all objects of the specified class.
        get(cls: Union[str, type], id: str) -> Union[Base, None]: Retrieves an object by class and ID.
        count(cls: type = None) -> int: Counts the number of objects in the database, optionally filtered by class.
        delete_all(class_name: str) -> Union[str, None]: Deletes all objects of a specific class from the database.
            If the class_name is not in the class_dictionary, returns an error message.

    """
    __engine = None
    session = None
    class_dictionary = {
        'Strain': Strain,
        'Store': Store,
        'User': User
    }

    def create_session(self):
        """
        Create a new session object for interacting with the database.

        Returns:
            Session: A new session object.
        """
        Session = sessionmaker(bind=self.__engine)
        return Session()

    def __init__(self, session=None):
        """
        Create a new database engine and session.

        Initializes a new database engine and a new session object.
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                            .format(getenv('DB_USER'),
                                    getenv('DB_PASS'),
                                    getenv('DB_HOST'),
                                    getenv('DB_NAME')),
                                    pool_pre_ping=True)

        self.session = session if session else self.create_session()
        self.reload()

    def reload(self):
        """
        Reload the session and create all tables in the database.

        This method creates all tables in the database and sets up a new session object.
        """
        Base.metadata.create_all(self.__engine)
        the_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.Session = scoped_session(the_session)
        self.session = self.Session()

    def new(self, obj):
        """Add a new object to the database.

        Args:
            obj: The object to add.

        """
        self.session.add(obj)


    def save(self):
        """Commit changes to the database."""
        try:
            self.session.commit()
        except Exception as e:
            print("Error committing changes:", e)
            self.session.rollback()


    def delete(self, obj=None):
        """Delete an object from the database.

        Args:
            obj: The object to delete.

        """
        if obj is not None:
            self.session.delete(obj)


    def all(self, cls=None, order_by=None, limit=None, offset=None, relationships=None):
        """
        Return all objects of the specified class.

        Args:
            cls: The class of object to retrieve.
            order_by: The attribute to order by.
            limit: The maximum number of objects to return.
            offset: The offset to start returning objects from.
            relationships: A list of relationships to join.

        Returns:
            A list of objects of the specified class.

        Raises:
            ValueError: If the class of object to retrieve is not recognized.
        """
        session = self.Session()
        query = session.query(cls) if cls else session.query(*self.class_dictionary.values())
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if relationships:
            for relationship in relationships:
                query = query.options(joinedload(relationship))
        result = query.all()
        session.close()
        return result



    def get(self, cls, id):
        """
        Retrieve an object by class and ID.

        Args:
            cls: The class of object to retrieve.
            id: The ID of the object to retrieve.

        Returns:
            The retrieved object, or None if no object was found.

        Raises:
            ValueError: If the class of object to retrieve is not recognized.
        """
        if cls not in self.class_dictionary.values():
            raise ValueError(f"Unrecognized class: {cls}")
        obj = self.session.query(cls).get(id)
        self.session.expunge_all()  # Remove all objects from the session cache
        return obj



    def count(self, cls=None):
        """
        Count the number of objects in the database, optionally filtered by class.

        Args:
            cls: The class of object to count, or None to count all objects.

        Returns:
            The number of objects in the database.

        Raises:
            ValueError: If the class of object to retrieve is not recognized.
        """
        query = self.session.query(cls) if cls else self.session.query(*self.class_dictionary.values())
        count = query.count()
        self.session.expunge_all()  # Remove all objects from the session cache
        return count

    def __enter__(self):
        """
        Enter the runtime context for the DBStorage instance.

        Returns:
            self: The current instance of DBStorage.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context for the DBStorage instance.

        Args:
            exc_type: The type of the exception, if any.
            exc_value: The instance of the exception, if any.
            traceback: A traceback object encapsulating the call stack at the point where the exception was raised, if any.

        Returns:
            False: To propagate any exceptions that occurred during the context.
        """
        self.session.close()
        return False


    def delete_all(self, class_name):
        """
        Delete all objects of a specific class from the database.

        Args:
            class_name: The name of the class to delete objects from.

        Returns:
            An error message if the class is not recognized, or None if the deletion was successful.
        """
        if class_name not in self.class_dictionary:
            return f"Invalid object type. Supported types: {', '.join(self.class_dictionary.keys())}"
        
        class_obj = self.class_dictionary[class_name]

        try:
            self.session.query(class_obj).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
