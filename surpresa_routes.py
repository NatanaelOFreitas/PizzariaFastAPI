from fastapi import APIRouter

surpresa_router = APIRouter(prefix="/surpresa", tags=["surpresa"])

@surpresa_router.get("/")
async def order():
    return {"mensagem" : "Te amo papai"}