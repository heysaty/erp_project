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
    tags=['Leaves']
)

get_db = database.get_db


@router.post('/leaves', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Leaves, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'employee':
            print(request.leave_date)
            new_leave = models.Leaves(date=str(request.leave_date),
                                      leave_type=request.leave_type,
                                      leave_status="Pending",
                                      user_id=user.id)
            db.add(new_leave)
            db.commit()
            db.refresh(new_leave)
            return new_leave
        if user.role == 'admin':
            new_leave = models.Leaves(date=str(request.leave_date),
                                      leave_type=request.leave_type,
                                      leave_status="Pending",
                                      user_id=user.id)
            db.add(new_leave)
            db.commit()
            db.refresh(new_leave)
            return new_leave


@router.get('/leaves', status_code=status.HTTP_201_CREATED)
def all(db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'employee':
            employee_leaves = db.query(models.Leaves).filter(models.Leaves.user_id == user.id).all()
            return employee_leaves

        if user.role == 'admin':
            all_leaves = db.query(models.Leaves).all()
            return all_leaves


@router.post('/leaves/approve/{id}', status_code=status.HTTP_201_CREATED)
def approve(id: int, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'admin':
            employee = db.query(models.Leaves).filter(models.Leaves.user_id == id).all()
            # print(employee)

            for user in employee:
                user.leave_status = 'Approved'

            db.commit()
            db.close()

            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail="leave approved")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Only Admin can approve")


@router.post('/leaves/reject/{id}', status_code=status.HTTP_201_CREATED)
def reject(id: int, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'admin':
            employee = db.query(models.Leaves).filter(models.Leaves.user_id == id).all()
            # print(employee)

            for user in employee:
                user.leave_status = 'Rejected'

            db.commit()
            db.close()

            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail="leave Rejected")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Only Admin can approve")

