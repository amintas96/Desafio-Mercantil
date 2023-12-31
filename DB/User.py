from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Utils import Constantes as ct
from API.DB_Consulta_API import cria_sessao
import streamlit as st
from Utils import Functions as fc


DATABASE_URL = ct.URL_CONECTION

Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))
    email = Column(String(50), unique=True)

class Comentario(Base):
    __tablename__ = 'comentarios'
    id_comentario = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    comentario = Column(Text)
    data_postagem = Column(TIMESTAMP, server_default='now()')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

def get_users():
    fc.info("INICIANDO")
    try:
        session = cria_sessao()
        return session.query(Usuario).order_by(Usuario.email).all()
    except Exception as e:
        fc.error(str(e))
    finally:
        session.close()

def create_user(nome, email):
    fc.info("INICIANDO")
    try:
        session = cria_sessao()
        user = Usuario(nome=nome, email=email)
        session.add(user)
        session.commit()
    except Exception as e:
        fc.error(str(e))
    finally:
        session.close()


def user_name_by_id(user_id):
    fc.info("INICIANDO: ")
    try:
        session = cria_sessao()
        usuario = session.query(Usuario).filter(Usuario.id_usuario == user_id).first()
        return usuario.nome
    except Exception as e:
        fc.error(str(e))
    finally:
        session.close()

def adicionar_usuario(nome, email):
    try:
        fc.info(ct.INICIA)
        session = sessionmaker(bind=engine)()
        usuario = Usuario(nome=nome, email=email)
        session.add(usuario)
        session.commit()
    except Exception as e:
        fc.error(str(e))
    finally:
        session.close()
def adicionar_comentario(nome, comentario):
    try:
        fc.info(ct.INICIA)
        session = sessionmaker(bind=engine)()
        nome = str(nome).title()
        usuario = session.query(Usuario).filter(Usuario.nome == nome).first()

        if usuario:
            comentario = Comentario(id_usuario=usuario.id_usuario, comentario=comentario)
            session.add(comentario)
            session.commit()
            return
        else:
            adicionar_usuario(nome=nome, email=None)
            adicionar_comentario(nome=nome, comentario=comentario)
    except Exception as e:
        fc.error(str(e))

    finally:
        session.close()

adicionar_comentario('junior', 'Olá rapaziada')
def obter_todos_comentarios():
    try:
        fc.info(ct.INICIA)
        session = cria_sessao()
        stmt = select(Comentario)
        resultados = session.execute(stmt).scalars().all()
        return resultados
    except Exception as e:
        fc.error(str(e))
    finally:
        session.close()

Base.metadata.create_all(bind=engine)


def update_user(id_usuario, novo_nome, novo_email):
    try:
        fc.info(ct.INICIA)
        sessao = cria_sessao()
        usuario = sessao.query(Usuario).filter_by(id_usuario=id_usuario).first()

        if usuario:
            usuario.nome = novo_nome
            usuario.email = novo_email
            sessao.commit()

    except Exception as e:
        fc.error(str(e))
    finally:
        sessao.close()

