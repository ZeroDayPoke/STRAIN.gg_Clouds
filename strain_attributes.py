import os
import json
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up database connection
engine = create_engine('postgresql://<username>:<password>@localhost/<database>')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define Strain model
class Strain(Base):
    __tablename__ = 'strains'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    strain_type = Column(String)
    thc_concentration = Column(Float)
    cbd_concentration = Column(Float)
    cbn_concentration = Column(Float)
    overview = Column(String)
    medical_uses = Column(String)
    flavors_aromas = Column(String)

# Read contents of TXT file
with open('strains.txt', 'r') as file:
    data = file.read()

# Parse data into list of strain information
strains = []
for strain_data in data.split('\n\n'):
    strain = json.loads(strain_data)
    strains.append(strain)

# Insert each strain into database
session = Session()
for strain in strains:
    new_strain = Strain(
        name=strain['Strain Name'],
        strain_type=strain['Strain type'],
        thc_concentration=strain['THC concentration'],
        cbd_concentration=strain['CBD concentration'],
        cbn_concentration=strain['CBN concentration'],
        overview=strain['Overview'],
        medical_uses=strain['Medical Uses'],
        flavors_aromas=strain['Flavors/Aroma']
    )
    session.add(new_strain)

session.commit()
