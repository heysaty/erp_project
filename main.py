from fastapi import FastAPI
import models
from database import engine
from routes import login, signup, logout, leaves

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(signup.router)
app.include_router(leaves.router)
app.include_router(logout.router)
