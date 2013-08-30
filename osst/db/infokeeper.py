from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from osst.db.model import Instance, Base
from osst.config.db import dbconfig

engine = create_engine('{engine}://{user}:{passw}@{host}:{port}/{dbname}'
                       .format(**dbconfig), echo=True)
session = sessionmaker(bind=engine)()
Base.metadata.create_all(bind=engine)


def add_vm(vmname):
    session.add(Instance(vmname))


def remove_vm(vmname):
    pass


def status_vm(vmname=None):
    return session.query(Instance).filter_by(name=vmname)
