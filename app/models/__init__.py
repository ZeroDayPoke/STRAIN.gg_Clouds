from .engine.dbstorage import DBStorage

storage = DBStorage()
class_dictionary = storage.class_dictionary
storage.reload()
