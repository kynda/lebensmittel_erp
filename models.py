from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Kunde(Base):
    __tablename__ = "kunden"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    adresse = Column(String)
    typ = Column(String)

class Produkt(Base):
    __tablename__ = "produkte"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    preis = Column(Float)

class Charge(Base):
    __tablename__ = "chargen"
    id = Column(Integer, primary_key=True, index=True)
    produkt_id = Column(Integer, ForeignKey("produkte.id"))
    datum = Column(Date)
    menge = Column(Float)
    produkt = relationship("Produkt")
