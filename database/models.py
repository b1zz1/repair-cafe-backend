from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    surname = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    birth_date = Column(Date, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class RepairPoint(Base):
    __tablename__ = 'repair_point'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    phone = Column(String(15), nullable=False)
    wa_link = Column(String(50))
    fc_link = Column(String(50))
    ig_link = Column(String(50))
    creation_date = Column(DateTime, server_default=func.now())
    last_validation = Column(Date)
    is_validated = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="repair_points")

class Expertise(Base):
    __tablename__ = 'expertise'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    description = Column(String(100))

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(50), nullable=False)
    house_number = Column(Integer, nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    state_code = Column(String(2))
    country = Column(String(50))
    cep = Column(String(8))
    repair_id = Column(Integer, ForeignKey('repair_point.id'))
    repair_point = relationship("RepairPoint", back_populates="address")

class RepairExpertise(Base):
    __tablename__ = 'repair_expertise'
    repair_id = Column(Integer, ForeignKey('repair_point.id'), primary_key=True)
    expertise_id = Column(Integer, ForeignKey('expertise.id'), primary_key=True)
    expertise = relationship("Expertise", back_populates="repair_points")
    repair_point = relationship("RepairPoint", back_populates="expertises")
