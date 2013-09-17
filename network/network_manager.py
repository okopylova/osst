"""
To use script, add this lines to your /etc/sudoers file:
youruser ALL=NOPASSWD: /usr/bin/pkill
youruser ALL=NOPASSWD: /sbin/brctl
youruser ALL=NOPASSWD: /sbin/ip
youruser ALL=NOPASSWD: /sbin/iptables
youruser ALL=NOPASSWD: /sbin/ifconfig
where 'youruser' is user who run this script
"""

from subprocess import Popen, PIPE, call
import os
from osst.db import infokeeper
from osst.db.infokeeper import IPaddress

home = os.path.expanduser('~')
hostsfile = os.path.join(home,
                         'osst/network/config/dnsmasq_dhcp_hostsfile.conf')
conffile = os.path.join(home, 'osst/network/config/dnsmasq.conf')


def _del_file_line(fname, line_pattern):
    with open(fname, 'r') as fd:
        lines = fd.readlines()
        for ln in lines:
            if ln.rfind(line_pattern) != -1:
                lines.remove(ln)
                with open(fname, 'w') as wfd:
                    wfd.writelines(lines)
                break


def dnsmasq_hangup():
    cmd = "sudo pkill -HUP -o dnsmasq"
    (stdout, stderr) = Popen(cmd.split(), stdout=PIPE).communicate()
    print 'stdout %s\nstderr %s' % (stdout, stderr)


def bridge_settings():
    call([os.path.join(home, 'osst/network/bridge_settings.sh')])


def assign_ip(vmid, mac, ip=None):
    if ip:  # check if address is availiable
        if not infokeeper.get_ipaddress(ip):
            raise ValueError("IP address '%s' is not availiable" % ip)
    else:  # get free ip address
        ip_obj = infokeeper.get_free_ip()
        if ip_obj:
            ip = ip_obj.addr
        else:
            raise ValueError("No free IP addresses")
    infokeeper.assign_ip(vmid, ip)
    with open(hostsfile, 'a') as fd:
        fd.write('%s,%s\n' % (mac, ip))
    dnsmasq_hangup()


def exempt_ip(addr):
    _del_file_line(hostsfile, addr + '\n')
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
        lines = fd.readlines()
        print lines
        for addr in addresses:
            infokeeper.delete_ip(addr)
            for ln in lines:
                if ln.rfind(addr + '\n') != -1:
                    lines.remove(ln)
                    print addr
                    break
        print lines
        with open(hostsfile, 'w') as wfd:
            wfd.writelines(lines)
        _del_file_line(conffile, addr_start + ',' + addr_end)


bridge_settings()
