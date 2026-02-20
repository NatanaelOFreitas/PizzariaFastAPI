from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    return {"mensagem": "Essa é a rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first
    if usuario:
        #caso já exista um usuário
        return {"mensagem": "Usuário já existente"}
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso"}