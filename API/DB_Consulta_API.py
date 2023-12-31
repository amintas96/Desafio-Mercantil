import psycopg2
from Utils import Constantes, Functions as fc
from sqlalchemy import create_engine, Column, Float, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def cria_sessao():
    try:
        fc.info('INICIANDO')
        Session = sessionmaker(bind=create_engine(Constantes.URL_CONECTION))
        return Session()
    except Exception as e:
        fc.error(str(e))    
    
def cria_cursor():
    fc.info('INICIANDO')
    try:
        dbname = Constantes.DBNAME
        user = Constantes.USER
        password = Constantes.PASSWORD
        host = Constantes.HOST
        port = Constantes.PORT
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return conn.cursor()
    except Exception as e:
        fc.error(str(e))



engine = create_engine(Constantes.URL_CONECTION)
Base = declarative_base()

class TB_Time_Series(Base):
    __tablename__ = 'tb_time_series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consulta_date = Column(TIMESTAMP)
    open_value = Column(Float)
    high_value = Column(Float)
    low_value = Column(Float)
    close_value = Column(Float)
    amount_volume = Column(Integer)

Base.metadata.create_all(engine)

def create_record(session, consulta_date, open_value, high_value, low_value, close_value, amount_volume):
    new_record = TB_Time_Series(
        consulta_date=consulta_date,
        open_value=open_value,
        high_value=high_value,
        low_value=low_value,
        close_value=close_value,
        amount_volume=amount_volume
    )
    session.add(new_record)
    session.commit()

def read_all_records(session):
    return session.query(TB_Time_Series).all()

def update_record(session, record_id, new_values):
    record = session.query(TB_Time_Series).filter_by(id=record_id).first()
    if record:
        for key, value in new_values.items():
            setattr(record, key, value)
        session.commit()

def delete_record(session, record_id):
    record = session.query(TB_Time_Series).filter_by(id=record_id).first()
    if record:
        session.delete(record)
        session.commit()
        
        