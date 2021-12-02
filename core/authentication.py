import time

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import log, settings
from core.schema.model_operation import UserOperation
from core.settings import Settings


class AuthHandler:
    security: HTTPBearer = HTTPBearer()

    def __init__(self):
         pass
        
    

    async def token_response(self,token: str):
        return {
            "access_token": token
        }

    async def login(self, email:str , passwd:str):
        """Encoder JWT token to check authentication
        Args:
            user_email (str): user Email
            passwd     (str): Password
        """
        user_repo: UserOperation = UserOperation()
        try:
            try:
                load = await user_repo.authenticate(email,passwd) 
                load= dict(load[0])
                load["expires"] =time.time() + 600
                
            except Exception as err:
                log.error(err)
                if hasattr(err, 'status_code'):
                    raise HTTPException(status_code=err.status_code, detail=err.detail)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
            
            
            token = jwt.encode(payload=load, key=Settings().secret_key, algorithm=Settings().algorithm, )
            return await self.token_response(token)
            
        except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=err.detail)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")

        


    async def verify(self, token: str):
        """Decode JWT token to check for permission.

        Args:
            token (str): Auth token for user.
        """

        try:
                user = jwt.decode(token, key=Settings().secret_key, algorithms=Settings().algorithm)
            
                if not user["is_active"] and user["role_type"] is not None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Deactivated User Account")

                else:
                    return user

        except jwt.ExpiredSignatureError as sign_err:
            log.warn(sign_err)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired")

        except jwt.InvalidTokenError as token_err:
            log.warn(token_err)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

        except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=err.detail)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
