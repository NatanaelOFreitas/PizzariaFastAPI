from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import Usuario_schema, Login_schema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc + duracao_token)
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = Session.query(Usuario).filter(Usuario.email==email)
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def auth():
    return {
        "mensagem": "Essa é a rota de autenticação",
        "autenticado": False
        }

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
        return {
            "mensagem": f"Usuário cadastrado com sucesso, novo usuário: {Usario_schema.email}"
            }
    
@auth_router.post("/login")
async def login(login_schema: Login_schema, session: Session = Depends(pegar_session)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha errada")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
                "acess_token": acess_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"                
                }
    
@auth_router.get("/refresh")
async def use_refresh_token():
    return 