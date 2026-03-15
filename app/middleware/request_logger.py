from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Proceed with the request first
        response = await call_next(request)

        # 2. Database logging logic
        db: Session = SessionLocal()
        try:
            # Check request.state for the user attached by oauth2.py
            user = getattr(request.state, "user", None)

            log = models.RequestLog(
                user_id=user.id if user else None,
                endpoint=request.url.path,
                method=request.method,
                status=response.status_code,
                # Use timezone-aware datetime for Python 3.13+
                timestamp=datetime.now(timezone.utc)
            )

            db.add(log)
            db.commit()
            # db.refresh(log) is optional unless you need the ID right now
        except Exception as e:
            
            print(f"Logging Error: {e}")
            db.rollback()
        finally:
            db.close()

        return response