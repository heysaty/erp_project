from fastapi import FastAPI
import models
from database import engine
from routes import login, signup, logout, leaves

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(login.router)
app.include_router(signup.router)
app.include_router(leaves.router)
app.include_router(logout.router)
