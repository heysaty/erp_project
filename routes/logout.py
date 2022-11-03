from fastapi import APIRouter, status, Depends, HTTPException, Response
import  database
import models
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Logout']
)


# db: Session = Depends(database.get_db)


@router.post('/logout')
def logout(db: Session = Depends(database.get_db),
           ):

    tokens= db.query(models.Tokens)
    tokens.delete(synchronize_session=False)
    db.commit()

    return "logout successfully"

