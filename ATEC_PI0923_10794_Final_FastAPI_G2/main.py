from typing import List

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modelos import *


engine = create_engine('sqlite:///chronetravel.db')
Base.metadata.create_all(engine)

session = Session(engine)

app = FastAPI()

# Viajantes

@app.post("/viajantes", status_code=status.HTTP_201_CREATED)
def create_viajante(create_viajante: CreateViajante) -> Viajante:
    viajante_bd = ViajanteBD(**create_viajante.model_dump())

    session.add(viajante_bd)
    session.commit()
    session.refresh(viajante_bd)
    return Viajante.model_validate(viajante_bd)

@app.get("/viajantes")
def get_viajantes() -> List[Viajante]:
    stmt = select(ViajanteBD)
    result = session.execute(stmt)
    viajantes = result.scalars().all()
    return [Viajante.model_validate(viajante) for viajante in viajantes]
@app.get("/viajantes/{id}")
def get_viajante(id: int) -> Viajante:
    stmt = select(ViajanteBD).where(ViajanteBD.id == id)
    result = session.execute(stmt)
    viajante =  result.scalars().first()
    if viajante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajante não encontrado")
    return Viajante.model_validate(viajante)
@app.put("/viajantes/{id}")
def put_viajante(id: int, create_viajante: CreateViajante) -> Viajante:
    stmt = select(ViajanteBD).where(ViajanteBD.id == id)
    result = session.execute(stmt)
    viajante =  result.scalars().first()
    if viajante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajante não encontrado")
    viajante.nome = create_viajante.nome # pyright: ignore[reportAttributeAccessIssue]
    viajante.email = create_viajante.email # pyright: ignore[reportAttributeAccessIssue]
    viajante.data_nasc = create_viajante.data_nasc # pyright: ignore[reportAttributeAccessIssue]
    session.commit()
    session.refresh(viajante)
    return Viajante.model_validate(viajante)
@app.patch("/viajantes/{id}")
def patch_viajante(id: int, patch_viajante: PatchViajante) -> Viajante:
    stmt = select(ViajanteBD).where(ViajanteBD.id == id)
    result = session.execute(stmt)
    viajante =  result.scalars().first()
    if viajante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajante não encontrado")
    if patch_viajante.nome != None:
        viajante.nome = patch_viajante.nome # pyright: ignore[reportAttributeAccessIssue]
    if patch_viajante.email != None:
        viajante.email = patch_viajante.email # pyright: ignore[reportAttributeAccessIssue]
    if patch_viajante.data_nasc != None:
        viajante.data_nasc = patch_viajante.data_nasc # pyright: ignore[reportAttributeAccessIssue] 
    session.commit()
    session.refresh(viajante)
    return Viajante.model_validate(viajante)
@app.delete("/viajantes/{id}")
def delete_viajante(id: int):
    stmt = select(ViajanteBD).where(ViajanteBD.id == id)
    result = session.execute(stmt)
    viajante =  result.scalars().first()
    if viajante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajante não encontrado")
    session.delete(viajante)
    session.commit()
    return {"message": "Viajante eliminado com sucesso"}


# Viagens

@app.post("/viagens", status_code=status.HTTP_201_CREATED)
def create_viagem(create_viagem: CreateViagem) -> Viagem:
    viagem_bd = ViagemBD(**create_viagem.model_dump())

    session.add(viagem_bd)
    session.commit()
    session.refresh(viagem_bd)
    return Viagem.model_validate(viagem_bd)

@app.get("/viagens")
def get_viagens() -> List[Viagem]:
    stmt = select(ViagemBD)
    result = session.execute(stmt)
    viagens = result.scalars().all()
    return [Viagem.model_validate(viagem) for viagem in viagens]

@app.get("/viagens/{id}")
def get_viagem(id: int) -> Viagem:
    stmt = select(ViagemBD).where(ViagemBD.id == id)
    result = session.execute(stmt)
    viagem =  result.scalars().first()
    if viagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")
    return Viagem.model_validate(viagem)

@app.put("/viagens/{id}")
def put_viagem(id: int, create_viagem: CreateViagem) -> Viagem:
    stmt = select(ViagemBD).where(ViagemBD.id == id)
    result = session.execute(stmt)
    viagem =  result.scalars().first()
    if viagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")
    
    viagem.destino_temporal = create_viagem.destino_temporal # pyright: ignore[reportAttributeAccessIssue]
    viagem.data_partida = create_viagem.data_partida # pyright: ignore[reportAttributeAccessIssue]
    viagem.duracao_dias = create_viagem.duracao_dias # pyright: ignore[reportAttributeAccessIssue]
    viagem.max_viajantes = create_viagem.max_viajantes # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(viagem)
    return Viagem.model_validate(viagem)
@app.patch("/viagens/{id}")
def patch_viagem(id: int, patch_viagem: PatchViagem) -> Viagem:
    stmt = select(ViagemBD).where(ViagemBD.id == id)
    result = session.execute(stmt)
    viagem =  result.scalars().first()
    if viagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")
    
    if patch_viagem.destino_temporal != None:
        viagem.destino_temporal = patch_viagem.destino_temporal # pyright: ignore[reportAttributeAccessIssue]
    if patch_viagem.data_partida != None:
        viagem.data_partida = patch_viagem.data_partida # pyright: ignore[reportAttributeAccessIssue]
    if patch_viagem.duracao_dias != None:
        viagem.duracao_dias = patch_viagem.duracao_dias # pyright: ignore[reportAttributeAccessIssue]
    if patch_viagem.max_viajantes != None:
        viagem.max_viajantes = patch_viagem.max_viajantes # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(viagem)
    return Viagem.model_validate(viagem)
@app.delete("/viagens/{id}")
def delete_viagem(id: int):
    stmt = select(ViagemBD).where(ViagemBD.id == id)
    result = session.execute(stmt)
    viagem =  result.scalars().first()
    if viagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")
    session.delete(viagem)
    session.commit()
    return {"message": "Viagem eliminada com sucesso"}

# Restrições

@app.get("/viagens/{id}/restricoes")
def get_restricoes(id: int) -> RestricoesViagem:
    if session.get(ViagemBD, id) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")
    stmt = select(RestricoesViagemBD).where(RestricoesViagemBD.id_viagem == id)
    result = session.execute(stmt)
    restricoes =  result.scalars().first()
    if restricoes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restrições não encontrada")
    return RestricoesViagem.model_validate(restricoes)


@app.post("/viagens/{id}/restricoes", status_code=status.HTTP_201_CREATED)
def create_restricao(id: int, create_restricao: CreateRestricoesViagem) -> RestricoesViagem:
    if session.get(ViagemBD, id) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")
    
    restricao_bd = RestricoesViagemBD(**create_restricao.model_dump())
    restricao_bd.id_viagem = id # type: ignore

    session.add(restricao_bd)
    session.commit()
    session.refresh(restricao_bd)
    return RestricoesViagem.model_validate(restricao_bd)
@app.patch("/viagens/{id}/restricoes")
def patch_restricao(id: int, create_restricao: CreateRestricoesViagem) -> RestricoesViagem:
    if session.get(ViagemBD, id) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")
    
    stmt = select(RestricoesViagemBD).where(RestricoesViagemBD.id == id)
    result = session.execute(stmt)
    restricao =  result.scalars().first()
    if restricao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restrição não encontrada")
    
    
    restricao.idade_maxima = create_restricao.idade_maxima # pyright: ignore[reportAttributeAccessIssue]
    restricao.idade_minima = create_restricao.idade_minima # pyright: ignore[reportAttributeAccessIssue]
    restricao.proibicao_interac_eventos = create_restricao.proibicao_interac_eventos # pyright: ignore[reportAttributeAccessIssue]
    restricao.requisitos = create_restricao.requisitos # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(restricao)
    return RestricoesViagem.model_validate(restricao)
@app.delete("/viagens/{id}/restricoes")
def delete_restricao(id: int):
    if session.get(ViagemBD, id) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")

    stmt = select(RestricoesViagemBD).where(RestricoesViagemBD.id == id)
    result = session.execute(stmt)
    restrição =  result.scalars().first()
    if restrição is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restrição não encontrada")
    session.delete(restrição)
    session.commit()
    return {"message": "Restrição eliminadas com sucesso"}


# Marcações
@app.post("/marcacoes", status_code=status.HTTP_201_CREATED)
def create_marcacao(create_marcacao: CreateMarcacao):
    marcacao_bd = MarcacaoBD(**create_marcacao.model_dump())

    if session.get(ViajanteBD, create_marcacao.id_viajante) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")
    viagem = session.get(ViagemBD, create_marcacao.id_viagem) 
    if viagem == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")

    marcacoes = session.execute(select(MarcacaoBD).where(MarcacaoBD.id_viagem ==create_marcacao.id_viagem)).scalars().all()

    if len(marcacoes) >= viagem.max_viajantes: # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem já atingiu o número máximo de viajantes")

    session.add(marcacao_bd)
    session.commit()
    session.refresh(marcacao_bd)
    return Marcacao.model_validate(marcacao_bd)
@app.get("/marcacoes")
def get_marcacoes(viajante_id: int = 0) -> List[Marcacao]:
    stmt = None
    if(viajante_id == 0):
        stmt = select(MarcacaoBD)
    else:
        stmt = select(MarcacaoBD).where(MarcacaoBD.id_viajante == viajante_id)
    result = session.execute(stmt)
    marcacoes = result.scalars().all()
    return [Marcacao.model_validate(marcacao) for marcacao in marcacoes]
@app.get("/marcacoes")
def get_marcacoes_viagem(viagem_id: int) -> List[Marcacao]:
    stmt = select(MarcacaoBD).where(MarcacaoBD.id_viagem == viagem_id)
    result = session.execute(stmt)
    marcacoes = result.scalars().all()
    return [Marcacao.model_validate(marcacao) for marcacao in marcacoes]
@app.get("/marcacoes/{id}")
def get_marcacao(id: int) -> Marcacao:
    stmt = select(MarcacaoBD).where(MarcacaoBD.id == id)
    result = session.execute(stmt)
    marcacao =  result.scalars().first()
    if marcacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcação não encontrada")
    return Marcacao.model_validate(marcacao)
@app.put("/marcacoes/{id}")
def put_marcacao(id: int, create_marcacao: CreateMarcacao) -> Marcacao:
    stmt = select(MarcacaoBD).where(MarcacaoBD.id == id)
    result = session.execute(stmt)
    marcacao =  result.scalars().first()
    if marcacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcação não encontrada")
    
    if session.get(ViajanteBD, create_marcacao.id_viajante) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")
    if session.get(ViagemBD, create_marcacao.id_viagem) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrada")

    marcacao.id_viajante = create_marcacao.id_viajante # pyright: ignore[reportAttributeAccessIssue]
    marcacao.id_viagem = create_marcacao.id_viagem # pyright: ignore[reportAttributeAccessIssue]
    marcacao.data_marcacao = create_marcacao.data_marcacao # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(marcacao)
    return Marcacao.model_validate(marcacao)
@app.patch("/marcacoes/{id}")
def patch_marcacao(id: int, patch_marcacao: PatchMarcacao) -> Marcacao:
    stmt = select(MarcacaoBD).where(MarcacaoBD.id == id)
    result = session.execute(stmt)
    marcacao =  result.scalars().first()
    if marcacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcação não encontrada")


    if patch_marcacao.id_viajante != None:
        if session.get(ViajanteBD, patch_marcacao.id_viajante) == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")
        marcacao.id_viajante = patch_marcacao.id_viajante # pyright: ignore[reportAttributeAccessIssue]
    if patch_marcacao.id_viagem != None:
        if session.get(ViagemBD, patch_marcacao.id_viagem) == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viagem não encontrado")
        marcacao.id_viagem = patch_marcacao.id_viagem # pyright: ignore[reportAttributeAccessIssue]
    if patch_marcacao.data_marcacao != None:
        marcacao.data_marcacao = patch_marcacao.data_marcacao # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(marcacao)
    return Marcacao.model_validate(marcacao)
@app.delete("/marcacoes/{id}")
def delete_marcacao(id: int):
    stmt = select(MarcacaoBD).where(MarcacaoBD.id == id)
    result = session.execute(stmt)
    marcacao =  result.scalars().first()
    if marcacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcação não encontrada")
    session.delete(marcacao)
    session.commit()
    return {"message": "Marcação eliminada com sucesso"}




@app.post("/pedidos", status_code=status.HTTP_201_CREATED)
def create_pedido(create_pedido: CreatePedidoViagem) -> PedidoViagem:
    pedido_bd = PedidoBD(**create_pedido.model_dump())

    if session.get(ViajanteBD, create_pedido.id_viajante) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")
    
    pedido_bd.data_pedido = datetime.datetime.now().date() # type: ignore

    session.add(pedido_bd)
    session.commit()
    session.refresh(pedido_bd)
    return PedidoViagem.model_validate(pedido_bd.__dict__)
@app.get("/pedidos")
def get_pedidos() -> List[PedidoViagem]:
    stmt = select(PedidoBD)
    result = session.execute(stmt)
    pedidos = result.scalars().all()
    return [PedidoViagem.model_validate(pedido.__dict__) for pedido in pedidos]
@app.get("/pedidos/{id}")
def get_pedido(id: int) -> PedidoViagem:
    stmt = select(PedidoBD).where(PedidoBD.id == id)
    result = session.execute(stmt)
    pedido =  result.scalars().first()
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrada")
    return PedidoViagem.model_validate(pedido.__dict__)
@app.put("/pedidos/{id}")
def put_pedido(id: int, create_pedido: CreatePedidoViagem) -> PedidoViagem:
    stmt = select(PedidoBD).where(PedidoBD.id == id)
    result = session.execute(stmt)
    pedido =  result.scalars().first()
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    
    if session.get(ViajanteBD, create_pedido.id_viajante) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")

    pedido.id_viajante = create_pedido.id_viajante # pyright: ignore[reportAttributeAccessIssue]
    pedido.destino_temporal = create_pedido.destino_temporal # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(pedido)
    return PedidoViagem.model_validate(pedido.__dict__)
@app.patch("/pedidos/{id}")
def patch_pedido(id: int, patch_pedido: PatchPedidoViagem) -> PedidoViagem:
    stmt = select(PedidoBD).where(PedidoBD.id == id)
    result = session.execute(stmt)
    pedido =  result.scalars().first()
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")


    if patch_pedido.id_viajante != None:
        if session.get(ViajanteBD, patch_pedido.id_viajante) == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Viajante não encontrado")
        pedido.id_viajante = patch_pedido.id_viajante # pyright: ignore[reportAttributeAccessIssue]
    if patch_pedido.destino_temporal != None:
        pedido.destino_temporal = patch_pedido.destino_temporal # pyright: ignore[reportAttributeAccessIssue]

    session.commit()
    session.refresh(pedido)
    return PedidoViagem.model_validate(pedido.__dict__)
@app.delete("/pedidos/{id}")
def delete_pedido(id: int):
    stmt = select(PedidoBD).where(PedidoBD.id == id)
    result = session.execute(stmt)
    pedido =  result.scalars().first()
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    session.delete(pedido)
    session.commit()
    return {"message": "Pedido eliminada com sucesso"}
