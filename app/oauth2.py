from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, schemas, utils, database
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, creditals_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
             raise creditals_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise creditals_exceptions

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    creditals_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, creditals_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    