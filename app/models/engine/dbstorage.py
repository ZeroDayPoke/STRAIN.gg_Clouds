#!/usr/bin/python3
"""Our DB Storage Engine"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from models.strain import Strain

class DBStorage:
    __engine = None
    __session = None

    # Dictionary to map class names to their respective model classes
    class_dictionary = {
        'Strain': Strain,
    }

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Create a connection to the MySQL database using the environment variables
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                            .format(os.getenv('DB_USER'),
                                    os.getenv('DB_PASS'),
                                    os.getenv('DB_HOST'),
                                    os.getenv('DB_NAME')),
                                    pool_pre_ping=True)

    def reload(self):
        """Create all tables in the database and set up the session."""
        Base.metadata.create_all(self.__engine)
        the_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(the_session)
        self.__session = Session()

    def new(self, obj):
        """Add a new object to the session."""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session."""
        if obj is not None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """
        Query all objects in the database, optionally filtered by class.
        Returns a dictionary with object keys in the format "<classname>.<id>".
        """
        obj_dct = {}
        qry = []
        if cls is None:
            for cls_typ in DBStorage.class_dictionary.values():
                qry.extend(self.__session.query(cls_typ).all())
        else:
            if cls in self.class_dictionary.keys():
                cls = self.class_dictionary.get(cls)
            qry = self.__session.query(cls)
        for obj in qry:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dct[obj_key] = obj
        return obj_dct

    def close(self):
        """Close the session."""
        self.__session.close()

    def get(self, cls, id):
        """
        Retrieve an object by class and id.
        Returns the object if found, otherwise returns None.
        """
        if type(cls) is str:
            cls = self.class_dictionary.get(cls)
        if cls and id:
            fetch = "{}.{}".format(cls.__name__, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
        Count the number of objects in the database, optionally filtered by class.
        Returns the count of objects.
        """
        return (len(self.all(cls)))

    def delete_all(self, class_name):
        """
        Delete all objects of a specific class from the database.
        If the class_name is not in the class_dictionary, returns an error message.
        """
        if class_name not in self.class_dictionary:
            return f"Invalid object type. Supported types: {', '.join(self.class_dictionary.keys())}"
        
        class_obj = self.class_dictionary[class_name]

        try:
            self.__session.query(class_obj).delete()
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e
