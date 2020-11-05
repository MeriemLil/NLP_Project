from sqlalchemy import create_engine
from sqlalchemy import exc

def database_connect():
    try:
        engine = create_engine('sqlite:///../../data/project.db', echo=False)
        engine.connect()
    except exc.OperationalError:
        engine = create_engine('sqlite:///data/project.db', echo=False)
    return engine