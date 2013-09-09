from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from osst.db.model import Instance, IPaddress
from osst.config.db import dbconfig

url = '{engine}://{user}:{passw}@{host}:{port}/{dbname}'.format(**dbconfig)
engine = create_engine(url)
session = sessionmaker(bind=engine)()


def _get_instance(vmname):
    return session.query(Instance).filter_by(name=vmname)


def add_vm(vmname, mac):
    """Insert information about VM state into table "instances"
    """
    session.add(Instance(vmname, mac))
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


def add_ip_addr(addr, assigned_vm_id=None):
    session.add(IPaddress(addr, assigned_vm_id))
    session.commit()
