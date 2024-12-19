from fastapi.security import  HTTPBearer
import uuid
from fastapi import HTTPException
from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
import jwt
from jose import JWTError, jwt
from App.read_env import env_data 
 
 
if __name__=="__main__":
    pwd_context = PasswordHasher(hash_len=env_data['hash_length'],
                                memory_cost=env_data['memorycost'],
                                parallelism=env_data['pararellism'],
                                salt_len=env_data['salt_length'],
                                time_cost=env_data['timecost']
                                )

    oauth2_scheme = HTTPBearer()



    async def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    async def get_password_hash(password):
        return pwd_context.hash(password)


    async def get_user(username: str,collection_name:str):
        try:
            
            user=await Mongoconnect.find_one_projection(collection_name=collection_name,query={"username":username},projection={username:1,"password":1,"id":1})
            return user
        except Exception as e:
            raise HTTPException(404, f"User not found {e}")


    async def authenticate_user(username: str, password: str):
        user = await get_user(username)

        if not user:
            return False
        if not await verify_password(password, user[1]):
            return False
        return user


    # async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    #     to_encode = data.copy()
    #     if expires_delta:
    #         expire = datetime.now(timezone.utc) + expires_delta
    #     else:
    #         try:
    #             expire_minutes = int(exptime)  # Ensure exptime is an integer
    #         except ValueError:
    #             expire_minutes = (
    #                 15  # Default to 15 minutes if exptime is not a valid integer
    #             )
    #         expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    #     to_encode.update({"exp": expire})
    #     encoded_jwt = jwt.encode(to_encode, key, algorithm=algo)
    #     return encoded_jwt


    # async def decode_jwt(token: str):
    #     try:
    #         payload = jwt.decode(token, key, algorithms=[algo])

    #         return payload
    #     except JWTError as e:
    #         return None


    # async def get_current_user(token: str = Depends(oauth2_scheme)):
    #     try:
    #         payload = await decode_jwt(token.credentials)
    #         if payload is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
    #             )

    #         expiration_time = payload.get("exp")
    #         if expiration_time is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 detail="Token has no expiration time",
    #             )

    #         expiration_datetime = datetime.fromtimestamp(expiration_time, timezone.utc)
    #         if expiration_datetime <= datetime.now(timezone.utc):
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
    #             )

    #         username: str = payload.get("sub")
    #         id: str = payload.get("user_id")
    #         if not username:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 detail="Username not found in token",
    #             )

    #         return {"username": username, "id": id}
    #     except JWTError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    #         )


    # async def authenticte_token(token):
    #     try:
    #         ueq = await RunQuery(
    #             q="""SELECT id, disabled FROM users WHERE id=?""", val=(token["id"],)
    #         )
    #         if not ueq:
    #             raise HTTPException(
    #                 status_code=404, detail="Invalid token: user does not exist"
    #             )

    #         user_id, disabled = ueq[0], ueq[1]

    #         if disabled:
    #             raise HTTPException(
    #                 status_code=403,
    #                 detail="Account is disabled: cannot perform any action ask admin ",
    #             )

    #         return token

    #     except HTTPException as http_exc:
    #         raise http_exc

    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Token validation error: {e}")
    

    # async def get_user_role(token: str | None = None):
    #     return await RunQuery(
    #         q=""" SELECT user_role FROM users WHERE id = ?""", val=(token["id"],)
    #     )
