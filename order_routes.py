from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def order():
    return {"mensagem" : "Essa é a rota de pedidos"}