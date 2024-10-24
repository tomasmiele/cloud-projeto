from fastapi import FastAPI, Depends, HTTPException, status, Request, Query
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from alpha_vantage.timeseries import TimeSeries

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

class CriarUsuario(BaseModel):
    nome: str
    email: str
    senha: str

class LogarUsuario(BaseModel):
    email: str
    senha: str

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(login_password: str, user_password) -> bool:
    return pwd_context.verify(login_password, user_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> bool:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido.",
            )

        usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido.",
            )
        return True

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido.",
        )

@app.post("/registrar")
def create_usuario(usuario: CriarUsuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já registrado."
        )
    
    hashed_password = hash_password(usuario.senha)
    novo_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=hashed_password)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    token_data = {"sub": novo_usuario.email}
    jwt_token = create_access_token(token_data)
    
    return {"jwt": jwt_token}

@app.post("/login")
def login_usuario(usuario: LogarUsuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email não registrado."
        )

    if verify_password(usuario.senha, usuario_existente.senha) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta."
        )

    token_data = {"sub": usuario.email}
    jwt_token = create_access_token(token_data)
    
    return {"jwt": jwt_token}

@app.get("/consultar")
def consultar(acao: str = Query("AAPL", description="Símbolo da ação a ser consultada"), usuario_valido: bool = Depends(verify_user_from_token)):
    ts = TimeSeries(key=os.getenv('API_KEY'), output_format='pandas')
    try:
        data, _ = ts.get_daily(acao)
    except:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Não existe essa ação."
        )
    data_last_5_days = data.head(5)
    data_dict = data_last_5_days.to_dict()
    return {f"Informações dos últimos 5 dias da Ação: {acao}": data_dict}
