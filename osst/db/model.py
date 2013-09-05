from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Instance(Base):
    __tablename__ = 'instances'

    STATUS_POWER_OFF = 0
    STATUS_POWER_ON = 1

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    power_status = Column(Integer,
                          default=STATUS_POWER_OFF)

    __table_args__ = (UniqueConstraint('name', name='_unique_vm_name'),)

    def __init__(self, name, power_status=None):
        self.name = name
        self.power_status = power_status

    def __repr__(self):
        return "<Instance(name='%s', power_status='%d')>" % (self.name,
                                                             self.power_status)


class IPaddress(Base):
    __tablename__ = 'ipaddr'

    id = Column(Integer, primary_key=True)
    addr = Column(String(15))  # 15 is length of IPv4 adress representation
    assigned_vm_id = Column(Integer, ForeignKey('instances.id'), nullable=True)

    __table_args__ = (UniqueConstraint('addr', name='_unique_addr'),)

    @staticmethod
    def validate_addr(addr):
        '''Validate IPv4 address'''
        octets = addr.split('.')
        return (len(octets) == 4 and
                all(map(lambda o: o.isdigit() and 0 <= int(o) < 256, octets)))

    def __init__(self, addr, vm_id=None):
        if IPaddress.validate_addr(addr):
            self.addr = addr
        else:
            raise ValueError('Invalid IPv4 address format')
        self.assigned_vm_id = vm_id

    def __repr__(self):
        return ("<IPaddress(addr='%s', assigned_vm_id='%s')>" %
                (self.addr, self.assigned_vm_id))
