import datetime

from db.database import database, user_table

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# This OAuth2PasswordBearer tells FastAPI our app uses JWTs for auth, & 
# it also adds to doc w/c URL the token be generated from (in this case: /token).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "22&$T'Sk&?YFh.l9v#o4Smt[a2tEDe[S"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



#****** Hashes Password ****************
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ******** Create Access Token(JWT) **************
def create_access_token(id_: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    jwt_data = {"sub": id_, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#******* For Login *******************

async def get_user(username: str):
    query = user_table.select().where(user_table.c.username == username)
    result = await database.fetch_one(query)
    if result:
        return result

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# ********* Get Current User from Token(with Oauth2 Depends) ************
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

