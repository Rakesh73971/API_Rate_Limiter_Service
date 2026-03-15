from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas
from ..oauth2 import get_current_user,check_admin_role
from typing import List
from sqlalchemy import func,text
from ..services.rate_limit_service import rate_limiter

router = APIRouter(
    prefix='/request_logs',
    tags=['RequestLogs'],
    dependencies=[Depends(rate_limiter)]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.RequestLogResponse)
def create_requestlog(
    requestlog: schemas.RequestLogBase,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print("current user:",current_user)
    request_log = models.RequestLog(
        user_id=current_user.id,
        endpoint=requestlog.endpoint,
        status_code=requestlog.status_code
    )

    db.add(request_log)
    db.commit()
    db.refresh(request_log)

    return request_log

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.RequestLogResponse])
def get_request_logs(db:Session=Depends(get_db),current_user=Depends(check_admin_role)):
    request_logs = db.query(models.RequestLog).all()
    return request_logs

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.RequestLogBase)
def get_request_log(id:int,db:Session=Depends(get_db),current_user=Depends(check_admin_role)):
    request_log = db.query(models.RequestLog).filter(models.RequestLog.id == id).first()
    if request_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with request log not found')
    return request_log


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.RequestLogResponse)
def update_request_log(id: int, request_log: schemas.RequestLogBase, db: Session = Depends(get_db), current_user = Depends(check_admin_role)):
    query = db.query(models.RequestLog).filter(models.RequestLog.id == id)
    db_log = query.first()
    
    if db_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id with {id} request log not found')
    
    query.update(request_log.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(db_log) 
    return db_log

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_request_log(id:int,db:Session=Depends(get_db),current_user=Depends(check_admin_role)):
    db_request_log = db.query(models.RequestLog).filter(models.RequestLog.id == id).first()
    if db_request_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='request log not found')
    db.delete(db_request_log)
    db.commit()
    return None


@router.get('/stats/summary', status_code=status.HTTP_200_OK)
def get_rate_limit_summary(
    db: Session = Depends(get_db), 
    current_user = Depends(check_admin_role)
):
    # 1. Total Requests Blocked (429s)
    total_blocked = db.query(models.RequestLog).filter(
        models.RequestLog.status_code == 429
    ).count()

    # 2. Total Requests Allowed (200s, 201s, etc.)
    total_allowed = db.query(models.RequestLog).filter(
        models.RequestLog.status_code < 400
    ).count()

    # 3. Most Targeted Endpoint (Where do people hit the limit most?)
    most_targeted = db.query(
        models.RequestLog.endpoint, 
        func.count(models.RequestLog.id).label('count')
    ).filter(models.RequestLog.status_code == 429)\
     .group_by(models.RequestLog.endpoint)\
     .order_by(text('count DESC'))\
     .first()

    return {
        "summary": {
            "blocked": total_blocked,
            "allowed": total_allowed,
            "total_processed": total_blocked + total_allowed
        },
        "top_blocked_endpoint": most_targeted[0] if most_targeted else "None",
        "health_score": f"{(total_allowed / (total_blocked + total_allowed) * 100) if (total_blocked + total_allowed) > 0 else 0:.2f}%"
    }