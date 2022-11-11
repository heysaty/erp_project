from sqlalchemy.orm import Session
import models
from hashing import Hasher

#
# get_db = database.get_db


def seeding(db: Session):
    admin = db.query(models.User).all()

    if not admin:
        new_admin = models.User(
            first_name="bruce",
            last_name="wayne",
            email="bruce@wayne.com",
            password=Hasher.get_password_hash("batman"),
            role="admin")
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    else:
        pass

