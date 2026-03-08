from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import schemas,models
from typing import List




router = APIRouter(
    prefix='/rate_limit_rules',
    tags=['Rate_Limit_Rules']
)

@router.post('/',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.LimitRuleOut)
def create_limit_rule(rule:schemas.LimitRuleCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    limit_rule = models.RateLimitRule(**rule.dict())
    db.add(limit_rule)
    db.commit()
    db.refresh(limit_rule)
    return limit_rule


@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.LimitRuleOut])
def get_rate_limites(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rate_limits=db.query(models.RateLimitRule).all()
    return rate_limits


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.LimitRuleOut)
def get_rate_limit(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rate_limit = db.query(models.RateLimitRule).filter(models.RateLimitRule.id == id).first()
    if rate_limit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with rate limit not found')
    return rate_limit


@router.put('/{id}',status_code=status.HTTP_404_NOT_FOUND,response_model=schemas.LimitRuleOut)
def update_rate_limit(id:int,rate_limit:schemas.LimitRuleCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_rate_limit = db.query(models.RateLimitRule).filter(models.RateLimitRule.id == id)
    if db_rate_limit.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with rate limit not found')
    db_rate_limit.update(rate_limit)
    db.commit()
    return db_rate_limit.first()


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_rate_limit(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rate_limit = db.query(models.RateLimitRule).filter(models.RateLimitRule.id == id).first()
    if rate_limit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id with rate limit is not found')
    db.delete(rate_limit)
    db.commit()
    return None
    