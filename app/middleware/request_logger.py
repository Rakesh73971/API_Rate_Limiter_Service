from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models


class RequestLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        db: Session = SessionLocal()

        response = await call_next(request)

        try:
            user = request.state.user if hasattr(request.state, "user") else None

            log = models.RequestLog(
                user_id=user.id if user else None,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                created_at=datetime.utcnow()
            )

            db.add(log)
            db.commit()

        finally:
            db.close()

        return response