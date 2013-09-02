from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from osst.db.model import Instance, Base
from osst.config.db import dbconfig

engine = create_engine('{engine}://{user}:{passw}@{host}:{port}/{dbname}'
                       .format(**dbconfig))
session = sessionmaker(bind=engine)()
Base.metadata.create_all(bind=engine)


def _get_instance(vmname):
    return session.query(Instance).filter_by(name=vmname)


def add_vm(vmname):
    """Insert information about VM state into table "instances"
    """
    session.add(Instance(vmname))
    session.commit()


def status_vm(vmname):
    return _get_instance(vmname).first()


def status_all_vm():
    return session.query(Instance).all()


def delete_vm(vmname):
    session.delete(_get_instance(vmname).first())
    session.commit()


def update_status_vm(vmname, status):
    _get_instance(vmname).update({'power_status': status})
    session.commit()
