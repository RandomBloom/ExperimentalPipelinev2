from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

import pandas

import datetime

Base = declarative_base()

class ExperimentDBException(Exception):
    pass

class Experiment(Base):
    __tablename__ = 'experiment'
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.now())
    organism = Column(String)
    variable = Column(String)
    temperature = Column(Integer)
    light = Column(Integer)
    target_N = Column(Integer)
    target_P = Column(Integer)
    target_Si = Column(Integer)
    replicate = Column(Integer)

    olc_results = relationship("OLCResults", back_populates="experiment")

    def __str__(self):
        return (
            f"Experiment(id={self.id}, "
            f"created_date={self.created_date}, "
            f"organism={self.organism}, "
            f"temperature={self.temperature}, "
            f"target_N={self.target_N}, "
            f"target_P={self.target_P}, "
            f"target_Si={self.target_Si}, "
            f"replicate={self.replicate})"
        )

class OLCResults(Base):
    __tablename__ = 'olcresults'

    id = Column(Integer, primary_key=True)
    time = Column(Float)
    oxygen = Column(Float)
    auxiliary_1 = Column(Float)
    label = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete="CASCADE"), nullable=False)

    experiment = relationship('Experiment', back_populates="olc_results")

class ExperimentDB():
    def __init__(self, db_file: str):
        self.engine = create_engine(f"sqlite:///{db_file}")
        self.Session = sessionmaker(bind=self.engine)

    def create(self):
        Base.metadata.create_all(self.engine)

    def add_experiment(self, created_date, organism, variable, temperature, light, N, P, Si, rep):
        if not created_date:
            created_date = datetime.datetime.now()
        with self.Session() as session:
            exp = Experiment(
                created_date=created_date,
                organism=organism,
                temperature=temperature,
                light=light,
                target_N=N,
                target_P=P,
                target_Si=Si,
                replicate=rep
            )
            session.add(exp)
            session.commit()
            session.refresh(exp)
            return exp.id

    def add_results(self, df, exp_id):
        # prepare the dataframe for upload
        df["experiment_id"] = exp_id
        db_columns = OLCResults.__table__.columns.keys()[1:]
        df.columns = db_columns
        with self.engine.connect() as con:
            df.to_sql(
                'olcresults',
                con=con,
                if_exists='append',
                index=False
            )

    def get_all_column_values(self, column):
        if not hasattr(Experiment, column):
            raise ExperimentDBException(f"experiment table has no column {column}")
        with self.Session() as session:
            return [item[0] for item in session.query(getattr(Experiment, column)).distinct()]

    def get_experiments_by_conditions(self, conditions):
        with self.Session() as session:
            query = session.query(Experiment)
            for column_name in conditions:
                value = conditions[column_name]
                query = query.filter(getattr(Experiment, column_name) == value)
            return [x for x in query]

    def get_results_by_conditions(self, conditions):
        """
        conditions is a map from column name to value for selection

        does a join between Experiment and OLCResults to return all the data together

        returns a dataframe
        """
        with self.Session() as session:
            # I feel like I should be able to do the join using the ORM relationships,
            # but this works so whatever
            query = session.query(Experiment, OLCResults).filter(Experiment.id == OLCResults.experiment_id)
            for column_name in conditions:
                value = conditions[column_name]
                query = query.filter(getattr(Experiment, column_name) == value)
            df = pandas.read_sql(sql=query.statement, con=self.engine)
            return df

if __name__ == "__main__":
    DB_FILE = "exp_data.db"
    test_conditions = {
        "organism": "3R6",
        "temperature": 26,
        "target_P": 36,
        "target_N": 50,
        "target_Si": 106
    }

    edb = ExperimentDB(DB_FILE)
    experiments = edb.get_experiments_by_conditions(test_conditions)
    print(experiments)
    import pdb;

    pdb.set_trace()