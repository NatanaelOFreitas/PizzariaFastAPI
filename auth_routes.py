from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_session
from main import bcrypt_context
from schemas import Usuario_schema, Login_schema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"asdassffgdh{id_usuario}"
    return token

@auth_router.get("/")
async def auth():
    return {"mensagem": "Essa é a rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(Usario_schema: Usuario_schema, session: Session = Depends(pegar_session)):
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
    
@auth_router.post("/login")
async def login(login_schema: Login_schema, session: Session = Depends(pegar_session)):
    usuario = Session.query(Usuario).filter(Usuario.email==login_schema.email)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        acess_token = criar_token(usuario.id)
        return {"acess_token": acess_token, "token_type": "Bearer"}