from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from sqlalchemy.orm.session import Session

from api.core import security
from api.schemas.auth import LoginRequestBody, LoginResponse
from api.dependencies.db import get_db

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(form_data: LoginRequestBody, db: Session = Depends(get_db)):
    """User will attempt to authenticate with a email/password flow"""

    user = await security.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        # Wrong email or password provided
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = security.create_access_token(data={"sub": user.email})

    return LoginResponse(token=token, user=user)
