from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import database
import models
import schemas
from middlewares import seeding
from middlewares import tokens
from jwttoken import create_access_token
from hashing import Hasher

router = APIRouter(
    tags=['Login']
)

get_db = database.get_db


@router.post('/login')
def login(request: schemas.ShowUser, db: Session = Depends(get_db)):
    seeding.seeding(db)

    token = db.query(models.Tokens).first()
    if token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Logout first")

    else:
        user = db.query(models.User).filter(models.User.email == request.email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Invalid Credentials")


        if not Hasher.verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Password")

        if not user.role == request.role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Invalid Role")

        access_token = create_access_token(data={"sub": user.email})

        tokens.tokendb(user.id, access_token, db)

        return {"access_token": access_token, "token_type": "bearer"}
