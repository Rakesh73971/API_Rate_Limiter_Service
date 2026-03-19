from fastapi import APIRouter,status,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import asc,desc
from ..database import get_db
from ..oauth2 import get_current_user,check_admin_role
from .. import schemas,models
from typing import List,Optional
from ..services.rate_limit_service import rate_limiter
import math




router = APIRouter(
    prefix='/rate_limit_rules',
    tags=['Rate_Limit_Rules'],
    dependencies=[Depends(rate_limiter),Depends(check_admin_role)]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.LimitRuleResponse)
def create_limit_rule(rule:schemas.LimitRuleBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    limit_rule = models.RateLimitRule(**rule.dict())
    db.add(limit_rule)
    db.commit()
    db.refresh(limit_rule)
    return limit_rule


@router.get('/',status_code=status.HTTP_200_OK,response_model=schemas.LimitRulePaginationResponse)
def get_rate_limites(db:Session=Depends(get_db),current_user=Depends(get_current_user),limit:int=Query(10,ge=1,le=10),page:int=Query(1,ge=1),search:Optional[str]="",sort_by:str=Query('id'),order:str=Query('asc')):
    sort_fields = {
        'id':models.RateLimitRule.id,
        'role':models.RateLimitRule.role,
        'requests_limit':models.RateLimitRule.requests_limit
    }
    query = db.query(models.RateLimitRule).filter(models.RateLimitRule.role.contains(search))

    total = query.count()
    total_pages = math.ceil(total/limit)
    offset = (page-1) * limit

    sort_column = sort_fields.get(sort_by,models.RateLimitRule.id)

    if order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    ratelimit_rule = query.limit(limit).offset(offset).all()

    return {
        'data':ratelimit_rule,
        'total':total,
        'page':page,
        'totalPages':total_pages
    }


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.LimitRuleResponse)
def get_rate_limit(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rate_limit = db.query(models.RateLimitRule).filter(models.RateLimitRule.id == id).first()
    if rate_limit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with rate limit not found')
    return rate_limit


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.LimitRuleBase)
def update_rate_limit(id:int,rate_limit:schemas.LimitRuleBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_rate_limit = db.query(models.RateLimitRule).filter(models.RateLimitRule.id == id)
    if db_rate_limit.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with rate limit not found')
    db_rate_limit.update(rate_limit.model_dump())
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
    