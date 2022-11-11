from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import models
import schemas
import emailsender

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
                                      user_id=user.id,
                                      leave_user=user)
            db.add(new_leave)
            db.commit()
            db.refresh(new_leave)

            return new_leave
        if user.role == 'admin':
            new_leave = models.Leaves(date=str(request.leave_date),
                                      leave_type=request.leave_type,
                                      leave_status="Pending",
                                      user_id=user.id,
                                      leave_user=user)
            db.add(new_leave)
            db.commit()
            db.refresh(new_leave)
            return new_leave


@router.get('/leaves', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'employee':
            employee_leaves = db.query(models.Leaves).filter(models.Leaves.user_id == user.id).all()
            # all_users = db.query(models.User).all()
            # employee_leaves= dict(employee_leaves)
            # for leaves in employee_leaves:
            #     for users in all_users:
            #         if leaves.user_id == users.id:
            #             leaves['name'] = str(users.first_name) + str(users.last_name)
            user_name = []
            for leaves in employee_leaves:
                name = {}
                name["name"] = leaves.leave_user
                name['leave_type']= leaves.leave_type
                name['leave_status']= leaves.leave_status
                name['date']= leaves.date
                user_name.append(name)

            return user_name

        if user.role == 'admin':
            all_leaves = db.query(models.Leaves).all()

            user_name = []
            for leaves in all_leaves:
                name = {}
                name["name"] = leaves.leave_user
                name['leave_type'] = leaves.leave_type
                name['leave_status'] = leaves.leave_status
                name['date'] = leaves.date
                user_name.append(name)

            return user_name


@router.put('/leaves/approve/{id}', status_code=status.HTTP_201_CREATED)
def approve(id: int, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'admin':
            employee = db.query(models.Leaves).filter(models.Leaves.id == id).first()
            approved_user = db.query(models.User).filter(models.User.id == employee.user_id).first()

            # emailsender.send_the_mail(approved_user.email,"approved")

            employee.leave_status = 'Approved'

            db.commit()
            db.close()

            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail="leave approved")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Only Admin can approve")


@router.put('/leaves/reject/{id}', status_code=status.HTTP_201_CREATED)
def reject(id: int, db: Session = Depends(get_db)):
    token = db.query(models.Tokens).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login First")
    else:
        user = db.query(models.User).filter(models.User.id == token.user_id).first()
        if user.role == 'admin':
            employee = db.query(models.Leaves).filter(models.Leaves.id == id).first()

            rejected_user = db.query(models.User).filter(models.User.id == employee.user_id).first()

            # emailsender.send_the_mail(rejected_user.email, "rejected")
            # print(employee)

            employee.leave_status = 'Rejected'

            db.commit()
            db.close()

            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail="leave Rejected")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Only Admin can approve")
