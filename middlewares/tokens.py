import models
from sqlalchemy.orm import Session


def tokendb(id: int, access_token: str, db: Session):
    print(id, access_token)
    token = models.Tokens(user_id=id,
                          token=access_token)
    db.add(token)
    db.commit()
    db.refresh(token)
