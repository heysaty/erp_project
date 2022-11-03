from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

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
        return 'signup'

