from fastapi import status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from jose import jwt,JWTError
from datetime import datetime,timedelta
from . import models,database
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    to_encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return to_encode_jwt

def verify_access_token(token:str,credential_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id:int=payload.get('user_id')
        if user_id is None:
            raise credentail_exceptions
        token_data = TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credential_exceptions

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credential_exceptions=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )

    token_data = verify_access_token(token,credential_exceptions)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        credential_exceptions
    return user

    

