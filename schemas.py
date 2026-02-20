from pydantic import BaseModel
from typing import Optional

class Usuario_schema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class Pedido_schema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True

class Login_schema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True