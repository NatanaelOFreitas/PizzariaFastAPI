from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def pegar_session():
    try:
        session = sessionmaker(bind=db)
        session = session()
        yield session
    finally:
        session.close()
        
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        raise HTTPException(status_code=401, detail="Acesso negado")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")
    return usuario