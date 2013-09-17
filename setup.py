from setuptools import setup
import os

setup(
    name="OSST",
    version="0.0.2",
    author="Olga Kopylova",
    description=("Manage VMs with CirrOS OS"),
    packages=['osst', 'network']
)

netconfdir = 'network/config'
dnsmasqconf = os.path.join(netconfdir, 'dnsmasq.conf')
if not os.path.exists(netconfdir):
    os.makedirs(netconfdir)
    with open(dnsmasqconf, 'w') as fd:
        fd.write('interface=br0\n'
                 'dhcp-hostsfile=%s'
                 % os.path.join(os.path.abspath(netconfdir),
                                'dnsmasq_dhcp_hostsfile.conf'))
    mode = int('777', 8)
    os.chmod(dnsmasqconf, mode)
    os.chmod(netconfdir, mode)
link = '/etc/dnsmasq.d/vm_network_manager.conf'
if not os.path.lexists(link):
    os.symlink(os.path.abspath(dnsmasqconf), link)
