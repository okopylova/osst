"""
To use script, add this lines to your /etc/sudoers file:
youruser ALL=NOPASSWD: /usr/bin/pkill
youruser ALL=NOPASSWD: /sbin/brctl
youruser ALL=NOPASSWD: /sbin/ip
youruser ALL=NOPASSWD: /sbin/iptables
youruser ALL=NOPASSWD: /sbin/ifconfig
where 'youruser' is user who run this script

Also make a symlink from config/dnsmasq.conf to /etc/dnsmasq.d
"""

from subprocess import Popen, PIPE, call
from osst.db import infokeeper
from osst.db.infokeeper import IPaddress

hostsfile = 'config/dnsmasq_dhcp_hostsfile.conf'
conffile = 'config/dnsmasq.conf'


def dnsmasq_hangup():
    cmd = "sudo pkill -HUP -o dnsmasq"
    (stdout, stderr) = Popen(cmd.split(), stdout=PIPE).communicate()
    print 'stdout %s\nstderr %s' % (stdout, stderr)


def bridge_settings():
    call(['./bridge_settings.sh'])


def assign_ip(vmname, addr=None):
    mac, ip = infokeeper.assign_ip(vmname, addr)
    with open(hostsfile, 'a') as fd:
        fd.write('%s,%s\n' % (mac, ip))
    dnsmasq_hangup()


def exempt_ip(addr):
    with open(hostsfile, 'r') as fd:
        lines = fd.readlines()
    for ln in lines:
        if ln.rfind(addr) != -1:
            lines.remove(ln)
            with open(hostsfile, 'w') as wfd:
                wfd.writelines(lines)
            break
    infokeeper.exempt_ip(addr)


def add_ip_range(addr_start, addr_end):
    "Add allocated IP range in database. For last two octets only"
    for addr in IPaddress.range(addr_start, addr_end):
        infokeeper.add_ip_addr(addr)
    with open(conffile, 'a') as fd:
        fd.write('dhcp-range=set:br0,%s,%s,static\n' % (addr_start, addr_end))
    dnsmasq_hangup()


def del_ip_range(addr_start, addr_end):
    addresses = IPaddress.range(addr_start, addr_end)
    with open(hostsfile, 'r') as fd:
        lines = fd.reedlines()
        for addr in addresses:
            infokeeper.delete_ip_addr(addr)
            for ln in lines:
                if ln.rfind(addr) != -1:
                    lines.remove(ln)
                    break
        with open(hostsfile, 'w') as wfd:
            wfd.writelines(lines)
    #TODO: remove range from conffile


bridge_settings()
