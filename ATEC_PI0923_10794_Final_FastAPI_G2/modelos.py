from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, ConfigDict
import datetime

# Base de dados
class Base(DeclarativeBase):
    pass
class ViajanteBD(Base):
    __tablename__ = "viajantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    data_nasc = Column(Date, nullable=False)
class ViagemBD(Base):
    __tablename__ = "viagens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino_temporal = Column(String, nullable=False)
    data_partida = Column(Date, nullable=False)
    duracao_dias = Column(Integer, nullable=False)
    max_viajantes = Column(Integer, nullable=False)
class MarcacaoBD(Base):
    __tablename__ = "marcacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viajante = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    id_viagem = Column(Integer, ForeignKey("viagens.id"), nullable=False)
    data_marcacao = Column(Date, nullable=False)
class PedidoBD(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viajante = Column(Integer, ForeignKey("viajantes.id"), nullable=False)
    data_pedido = Column(Date, nullable=False)
    destino_temporal = Column(String, nullable=False)
class RestricoesViagemBD(Base):
    __tablename__ = "restricoes_viagem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viagem = Column(Integer, ForeignKey("viagens.id"), unique=True, nullable=False)
    idade_minima = Column(Integer, nullable=True)
    idade_maxima = Column(Integer, nullable=True)
    proibicao_interac_eventos = Column(Boolean, nullable=False, default=False)
    requisitos = Column(String, nullable=True)
# Pydantic
class Viajante(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    data_nasc: datetime.date
class CreateViajante(BaseModel):
    nome: str
    email: str
    data_nasc: datetime.date
class PatchViajante(BaseModel):
    nome: str | None = None
    email: str | None = None
    data_nasc: datetime.date | None = None


class Viagem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    destino_temporal: str
    data_partida: datetime.date
    duracao_dias: int
    max_viajantes: int
class CreateViagem(BaseModel):
    destino_temporal: str
    data_partida: datetime.date
    duracao_dias: int
    max_viajantes: int
class PatchViagem(BaseModel):
    destino_temporal: str | None = None
    data_partida: datetime.date | None = None
    duracao_dias: int | None = None
    max_viajantes: int | None = None

class RestricoesViagem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_viagem: int
    idade_minima: int | None = None
    idade_maxima: int | None = None
    proibicao_interac_eventos: bool = False
    requisitos: str | None = None

class CreateRestricoesViagem(BaseModel):
    idade_minima: int | None = None
    idade_maxima: int | None = None
    proibicao_interac_eventos: bool = False
    requisitos: str | None = None

class Marcacao(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_viajante: int
    id_viagem: int
    data_marcacao: datetime.date
class CreateMarcacao(BaseModel):
    id_viajante: int
    id_viagem: int
    data_marcacao: datetime.date
class PatchMarcacao(BaseModel):
    id_viajante: int | None = None
    id_viagem: int | None = None
    data_marcacao: datetime.date | None = None

class PedidoViagem(BaseModel):
    id: int
    id_viajante: int
    data_pedido: datetime.date
    destino_temporal: str
class CreatePedidoViagem(BaseModel):
    id_viajante: int
    destino_temporal: str
class PatchPedidoViagem(BaseModel):
    id_viajante: int | None = None
    destino_temporal: str | None = None