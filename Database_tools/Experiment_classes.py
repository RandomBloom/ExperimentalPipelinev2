from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

class NikonResults(Base):
    __tablename__ = 'nikonresults'

    date = Column(DateTime)
    circularity = Column(Float)
    eq_diameter = Column(Float)
    min_feret = Column(Float)
    max_feret = Column(Float)
    mean_obj_intensity = Column(Float)
    object_area = Column(Float)
    perimeter = Column(Float)
    volume_eq_sphere = Column(Float)


class OLCResults(Base):
    __tablename__ = 'olcresults'

    id = Column(Integer, primary_key=True)
    time = Column(Float)
    oxygen = Column(Float)
    auxiliary_1 = Column(Float)
    label = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete="CASCADE"), nullable=False)

    experiment = relationship('Experiment', back_populates="olc_results")
