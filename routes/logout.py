from fastapi import APIRouter, status, Depends, HTTPException, Response
import  database
import models
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Logout']
)


# db: Session = Depends(database.get_db)

### logout hone k bad logout krne pad login first return karega
@router.delete('/logout')
def logout(db: Session = Depends(database.get_db),):
    tokens= db.query(models.Tokens)

    if tokens.all():
        tokens.delete(synchronize_session=False)
        db.commit()

        return "logout successfully"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Login First")

