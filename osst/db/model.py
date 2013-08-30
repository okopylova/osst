from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Instance(Base):
    __tablename__ = 'instances'

    STATUS_POWER_OFF = 0
    STATUS_POWER_ON = 1

    id = Column(Integer, primary_key=True)
    name = Column(String)
    power_status = Column(Integer,
                          default=STATUS_POWER_OFF)

    def __init__(self, name, power_status=None):
        self.name = name
        self.power_status = power_status

    def __repr__(self):
        return "<Instance(name='%s', power_status='%d')>" % (self.name,
                                                             self.power_status)


from sqlalchemy import create_engine
Base.metadata.create_all(create_engine('postgresql://postgres:zaq123@localhost:5432/vm_manager'))
