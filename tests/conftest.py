import pytest
from app.models.engine.dbstorage import DBStorage

@pytest.fixture(scope='module')
def db():
    """Set up and tear down the DBStorage instance."""
    db_storage = DBStorage()
    yield db_storage
    db_storage.close()
