from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import models
from .. import utils
from app.database import get_db
from app.schemas import UserBase,UserResponse,UserUpdate
from ..oauth2 import get_current_user
from ..services.rate_limit_service import get_rate_limit_rule,rate_limiter
from ..redis_limiter import check_rate_limit

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    dependencies=[Depends(rate_limiter)]
):

    rule = get_rate_limit_rule(db, current_user.role)

    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate limit rule not found"
        )

    check_rate_limit(
        user_id=current_user.id,
        limit=rule.requests_limit,
        window=rule.time_window
    )

    return {"message": "User profile"}

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user:UserBase,db:Session=Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=UserResponse)
def get_user(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user.id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not allowed')

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    return user

@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=UserResponse)
def update_user(id:int,user:UserUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == id)

    if db_user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    if db_user.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not allowed')
    db_user.update(user.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    return db_user.first()

@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    rule = get_rate_limit_rule(db, current_user.role)

    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate limit rule not found"
        )

    check_rate_limit(
        user_id=current_user.id,
        limit=rule.requests_limit,
        window=rule.time_window
    )

    return {"message": "User profile"}