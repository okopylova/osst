"""Manage VMs with CirrOS OS, based on existing VM disk image
see config.pathconf.py for path configuration"""

import os
import shutil
import libvirt
from config.pathconf import driver, base_disk_path
from config.pathconf import base_vm_img, vm_conf_templ_path

_conn = libvirt.open(driver)
_vm_conf_template = open(vm_conf_templ_path).read()


def list_all():
    """Returns list of all defined VM names"""

    return (_conn.listDefinedDomains() +
            [_conn.lookupByID(id).name() for id in _conn.listDomainsID()])


def create(vmname):
    """Create VM with specified name

    Keyword arguments:
    vmname -- name of the created VM

    Raise libvirt.libvirtError if VM with this name already exists

    Returns libvirt.virDomain instance"""

    imgpath = os.path.join(base_disk_path, vmname + '.img')
    shutil.copyfile(base_vm_img, imgpath)
    config = _vm_conf_template.format(**locals())
    return _conn.defineXML(config)


def delete(vmname, deldisk=True):
    """Delete VM with specified name

    Keyword arguments:
    vmname -- name of the created VM
    deldisk -- specifies whether to perform deletion of VM disk image
    (default: True)

    Raise libvirt.libvirtError if VM with this name doesn't exist"""

    dom = _conn.lookupByName(vmname)
    if dom.isActive():
        dom.destroy()
    dom.undefine()
    if deldisk:
        os.remove(os.path.join(base_disk_path, dom.name() + '.img'))


def power_on(vmname):
    """Start VM with specified name
    Raise libvirt.libvirtError if VM with this name doesn't exist
    or it is already running"""

    _conn.lookupByName(vmname).create()


def power_off(vmname):
    """Stop VM with specified name
    Throws libvirt.libvirtError if VM with this name doesn't exist
    or it is not running"""

    _conn.lookupByName(vmname).destroy()  # cirros don't know shutdown command


def reboot(vmname):
    """Reboot VM with specified name
    Throws libvirt.libvirtError if VM with this name doesn't exist
    or it is not running"""

    dom = _conn.lookupByName(vmname)
    # cirros also don't know reboot command
    dom.destroy()
    dom.create()
