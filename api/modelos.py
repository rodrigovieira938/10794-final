from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
class Viajante(Base):
    __tablename__ = "viajantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    data_nasc = Column(Date, nullable=False)
class Viagem(Base):
    __tablename__ = "viagens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino_temporal = Column(String, nullable=False)
    data_partida = Column(Date, nullable=False)
    duracao_dias = Column(Integer, nullable=False)
    max_viajantes = Column(Integer, nullable=False)
class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viajante = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    id_viagem = Column(Integer, ForeignKey("viagens.id"), nullable=False)
    data_marcacao = Column(Date, nullable=False)
class RestricoesViagem(Base):
    __tablename__ = "restricoes_viagem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viagem = Column(Integer, ForeignKey("viagens.id"), unique=True, nullable=False)
    idade_minima = Column(Integer, nullable=True)
    idade_maxima = Column(Integer, nullable=True)
    proibicao_interac_eventos = Column(Boolean, nullable=True)
    requisitos = Column(String, nullable=True)