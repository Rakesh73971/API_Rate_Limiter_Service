from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from ..redis_limiter import check_rate_limit
from .. import models


def rate_limiter(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    rule = db.query(models.RateLimitRule).filter(
        models.RateLimitRule.role == current_user.role
    ).first()

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

def get_rate_limit_rule(db: Session, role: str):
    return db.query(models.RateLimitRule).filter(
        models.RateLimitRule.role == role
    ).first()