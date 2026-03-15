from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        
        db: Session = SessionLocal()
        try:
            user = getattr(request.state, "user", None)

            log = models.RequestLog(
                user_id=user.id if user else None,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                timestamp=datetime.now(timezone.utc)
            )

            db.add(log)
            db.commit()
        except Exception as e:
            
            print(f"Logging Error: {e}")
            db.rollback()
        finally:
            db.close()

        return response