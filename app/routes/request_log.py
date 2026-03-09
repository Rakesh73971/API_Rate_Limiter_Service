from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas
from ..oauth2 import get_current_user
from typing import List
from ..services.rate_limit_service import rate_limiter

router = APIRouter(
    prefix='/request_logs',
    tags=['RequestLogs'],
    dependencies=[Depends(rate_limiter)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_requestlog(
    requestlog: schemas.RequestLogCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print("current user:",current_user)
    request_log = models.RequestLog(
        user_id=current_user.id,
        endpoint=requestlog.endpoint,
        status=requestlog.status
    )

    db.add(request_log)
    db.commit()
    db.refresh(request_log)

    return request_log

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.RequestLogOut])
def get_request_logs(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    request_logs = db.query(models.RequestLog).all()
    return request_logs

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.RequestLogOut)
def get_request_log(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    request_log = db.query(models.RequestLog).filter(models.RequestLog.id == id).first()
    if request_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='id with request log not found')
    return request_log


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.RequestLogOut)
def update_request_log(id:int,request_log:schemas.RequestLogCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_request_log = db.query(models.RequestLog).filter(models.RequestLog.id == id)
    if db_request_log.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id with {id} requrest log not found')
    db_request_log.update(request_log)
    db.commit()
    db.refresh(db_request_log)
    return db_request_log.first()

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_request_log(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_request_log = db.query(models.RequestLog).filter(models.RequestLog.id == id).first()
    if db_request_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='request log not found')
    db.delete(db_request_log)
    db.commit()
    return None