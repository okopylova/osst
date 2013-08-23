"""This module contains variables for vm_manager path configurations"""

from os.path import expanduser, join

driver = 'qemu:///system'
home = expanduser('~')
base_disk_path = join(home, 'vm_disks')
base_vm_img = join(home, 'osst/vm_manager/data/base_vm_disk.img')
vm_conf_templ_path = join(home, 'osst/vm_manager/src/config/vm_conf_templ.xml')
