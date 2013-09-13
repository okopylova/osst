from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from osst.db.model import Instance, IPaddress
from osst.config.db import dbconfig

url = '{engine}://{user}:{passw}@{host}:{port}/{dbname}'.format(**dbconfig)
engine = create_engine(url)
session = sessionmaker(bind=engine)()


def get_instance(vmname):
    return session.query(Instance).filter_by(name=vmname)


def add_vm(vmname, mac):
    """Insert information about VM state into table "instances"
    """
    session.add(Instance(vmname, mac))
    session.commit()


def status_vm(vmname):
    return get_instance(vmname).first()


def status_all_vm():
    return session.query(Instance).all()


def delete_vm(vmname):
    vm = get_instance(vmname).first()
    session.delete(vm)
    session.commit()


def update_status_vm(vmname, status):
    get_instance(vmname).update({'power_status': status})
    session.commit()


def add_ip_addr(addr, assigned_vm_id=None):
    session.add(IPaddress(addr, assigned_vm_id))
    session.commit()


def delite_ip(addr):
    session.query(IPaddress).filter_by(addr=addr)


def get_free_ip():
    return session.query(IPaddress).filter_by(assigned_vm_id=None).first()


def exempt_ip(addr):
    session.query(IPaddress).filter_by(addr=addr). \
        update({'assigned_vm_id': None})
    session.commit()


def assign_ip(vmname, addr=None):
    vm = get_instance(vmname).first()
    if vm is None:
        raise ValueError("No VM with name '%s'" % vmname)
    if addr:  # check if address is availiable
        ip_obj = session.query(IPaddress). \
            filter_by(addr=addr, assigned_vm_id=None).first()
        if not ip_obj:
            raise ValueError("IP address '%s' is not availiable" % addr)
    else:  # get free ip address
        ip_obj = session.query(IPaddress).filter_by(assigned_vm_id=None). \
            first()
        if not ip_obj:
            raise ValueError("No free IP addresses")
    session.query(IPaddress).filter_by(id=ip_obj.id). \
        update({'assigned_vm_id': vm.id})
    session.commit()
    return vm.mac, ip_obj.addr


#def ip_bind_vm(addr, vm_id):
