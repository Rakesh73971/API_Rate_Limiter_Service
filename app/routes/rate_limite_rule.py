from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import schemas,models
from typing import List




router = APIRouter(
    prefix='/rate_limit_rules',
    tags=['Rate_Limit_Rules']
)

@router.put('/',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.LimitRuleOut)
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
