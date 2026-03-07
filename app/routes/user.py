from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import models
from .. import utils
from app.database import get_db
from app.schemas import UserCreate,UserOut

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    return user
