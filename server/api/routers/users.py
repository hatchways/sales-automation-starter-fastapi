# FastAPI
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm.session import Session

from api import schemas
from api.core import security
from api.crud import UserCrud
from api.dependencies.auth import get_current_user
from api.dependencies.db import get_db

router = APIRouter(prefix="/api", tags=["user"])


@router.get("/user", response_model=schemas.User)
def get_authenticated_user(
    current_user: schemas.User = Depends(get_current_user),
):
    """Get the currently logged in user if the token is valid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in"
        )
    return current_user


@router.post("/users", response_model=schemas.RegisterResponse)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user record in the database and send a registration confirmation email"""
    db_user = UserCrud.get_user_by_email(db, data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserCrud.create_user(db, data)

    token = security.create_access_token(data={"sub": new_user.email})

    return schemas.RegisterResponse(token=token, user=new_user)
