from datetime import date
from sqlalchemy import create_engine
from modelos import Base, Viajante, Viagem, Reserva, RestricoesViagem

viajantes = [
    Viajante(nome="Ana Silva", email="ana@example.com", data_nasc=date(1990, 5, 14)),
    Viajante(nome="Bruno Costa", email="bruno@example.com", data_nasc=date(1985, 8, 22)),
    Viajante(nome="Carla Mendes", email="carla@example.com", data_nasc=date(2000, 1, 10)),
    Viajante(nome="Diogo Rocha", email="diogo@example.com", data_nasc=date(1978, 12, 3)),
]

viagens = [
    Viagem(destino_temporal="Roma Antiga - 50 a.C.", data_partida=date(2026, 6, 1), duracao_dias=7, max_viajantes=10),
    Viagem(destino_temporal="Egito - Construção das Pirâmides", data_partida=date(2026, 7, 15), duracao_dias=10, max_viajantes=8),
    Viagem(destino_temporal="Futuro - Marte 2150", data_partida=date(2026, 9, 10), duracao_dias=5, max_viajantes=5),
]

reservas = [
    Reserva(id_viajante=1, id_viagem=1, data_marcacao=date(2026, 1, 10)),
    Reserva(id_viajante=2, id_viagem=1, data_marcacao=date(2026, 1, 12)),
    Reserva(id_viajante=3, id_viagem=2, data_marcacao=date(2026, 2, 5)),
    Reserva(id_viajante=1, id_viagem=3, data_marcacao=date(2026, 3, 1)),
]

restricoes = [
    RestricoesViagem(id_viagem=1, idade_minima=18, idade_maxima=60, proibicao_interac_eventos=True, requisitos="Não alterar eventos históricos"),
    RestricoesViagem(id_viagem=2, idade_minima=21, idade_maxima=None, proibicao_interac_eventos=True, requisitos="Uso obrigatório de traje adequado"),
    RestricoesViagem(id_viagem=3, idade_minima=25, idade_maxima=55, proibicao_interac_eventos=False, requisitos="Treino físico obrigatório"),
]

from sqlalchemy.orm import Session
engine = create_engine('sqlite:///alunos.db')
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all(viajantes)
    session.commit()

    session.add_all(viagens)
    session.commit()

    session.add_all(reservas)
    session.commit()

    session.add_all(restricoes)
    session.commit()