from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router
from surpresa_routes import surpresa_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(surpresa_router)

#para rodar o código, basta rodar esse comando no terminal: uvicorn main:app --reload