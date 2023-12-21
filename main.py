from fastapi import FastAPI, HTTPException, status, Depends
from api import main as api_main
from db.database import database, user_table
from security import get_password_hash, create_access_token, authenticate_user, get_current_user
from models.user import UserIn, User


app = FastAPI()

# ******** Include Route from other module ******************
app.include_router(api_main.router)

# ******** Route in here ******************
@app.get("/")
def root():
    return {"message": "Welcome to social media api!"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/register")
async def register(user: UserIn):
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(username=user.username, password=hashed_password)
    await database.execute(query)
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}




# startup and shutdown event handlers
async def startup_event():
    await database.connect()

async def shutdown_event():
    await database.disconnect()

# event handlers addition
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)
