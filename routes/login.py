from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import database
import models
import schemas
from middlewares import seeding
from middlewares import tokens
from jwttoken import create_access_token

router = APIRouter(
    tags=['Login']
)

get_db = database.get_db


@router.post('/login')
def login(request: schemas.ShowUser, db: Session = Depends(get_db)):
    seeding.seeding(db)

    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    # if not Hasher.verify_password(request.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="Incorrect Password")

    access_token = create_access_token(data={"sub": user.email})

    print(access_token)

    tokens.tokendb(user.id, access_token, db)

    check = seeding.check_admin(request, db)

    if check:

        return {"access_token": access_token, "token_type": "bearer"}

    else:

        return "not admin"
