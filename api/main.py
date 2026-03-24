from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modelos import Base

engine = create_engine('sqlite:///alunos.db')
Base.metadata.create_all(engine)

session = Session(engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "a minha 1a api fastAPI"}