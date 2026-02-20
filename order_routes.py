from fastapi import APIRouter, Depends
from schemas import Pedido_schema
from sqlalchemy.orm import Session
from dependencies import pegar_session
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    return {"mensagem" : "Essa é a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: Pedido_schema, session: Session = Depends(pegar_session)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    Session.add(novo_pedido)
    Session.commit()
    return {"mensagem": f"Pedido feito com sucesso. Id do pedido: {novo_pedido.id}"}