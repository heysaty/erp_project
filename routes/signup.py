from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from hashing import Hasher
import schemas, models
import database
from middlewares import seeding
from oauth2 import get_current_user

router = APIRouter(
    tags=['Signup']
)

get_db = database.get_db


@router.post('/signup')
def signup(request: schemas.User, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")

    else:

        user = db.query(models.User).filter(models.User.id == token.user_id).first()

        if user.role == 'admin':

            if request.role == 'admin':
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Only employee role can be created")
            user = db.query(models.User).filter(models.User.email == request.email).first()

            if not user:

                new_user = models.User(first_name=request.first_name, last_name=request.last_name,
                                       email=request.email, role=request.role,
                                       password=Hasher.get_password_hash(request.password))

                db.add(new_user)
                db.commit()
                db.refresh(new_user)

                return new_user
            else:

                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="user already exists")

        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Only Admin can create user")


