from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_session
from main import bcrypt_context
from schemas import Usuario_schema
from sqlalchemy.orm import session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    return {"mensagem": "Essa é a rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(Usario_schema: Usuario_schema, session: session = Depends(pegar_session)):
    usuario = session.query(Usuario).filter(Usuario.email==Usario_schema.email).first
    if usuario:
        #caso já exista um usuário
        raise HTTPException(status_code=400, detail= "Email já existente")
    else:
        senha_criptografada = bcrypt_context.hash(Usuario_schema.senha)
        novo_usuario = Usuario(Usario_schema.nome, Usario_schema.email, senha_criptografada, Usario_schema.ativo, Usario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso, novo usuário: {Usario_schema.email}"}