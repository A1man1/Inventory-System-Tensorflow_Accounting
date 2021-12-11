import time

import jwt
from fastapi import  HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import log
from core.Permission.permissin import _Schema_Admin
from core.schema.model_operation import RoleOperation, UserOperation
from core.schema.ModelOpreator.user import UserLoginSchema
from core.settings import Settings


class AuthHandler:

    
    def __init__(self):
         pass
        
    
    async def token_response(self,token: str):
        return {
            "access_token": token
        }

    async def check_user(self, payload:UserLoginSchema):
        user_repo: UserOperation = UserOperation()
        load = None 
        try:
            load = await user_repo.authenticate(*dict(payload).values()) 
            print(load)
            load= dict(load[0])
            load["expires"] = time.time() + 200000
            print(load)
            return load
        except Exception as err:
                log.error(err)
                if hasattr(err, 'status_code'):
                    raise HTTPException(status_code=err.status_code, detail=err.detail)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
        finally:
            return load

    async def login(self, payload:UserLoginSchema):
        """Encoder JWT token to check authentication
        Args:
            user_email (str): user Email
            passwd     (str): Password
        """
        try:
            data = await self.check_user(payload)
            if data:
                token = jwt.encode(payload=data, key=Settings().secret_key, algorithm=Settings().algorithm)
                return await self.token_response(token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User and password not matched")
        except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=err.detail)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")

        
    async def verify(self, token:str)->dict:
        """Decode JWT token to check for permission.

        Args:
            token (str): Auth token for user.
        """

        try:
                user = jwt.decode(token, key=Settings().secret_key, algorithms=Settings().algorithm)
                
                if  not user["is_active"] and user["role_type"] is not None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Deactivated User Account")
                if user['expires'] < time.time():
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="token Invaild") 
                
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


class JWTBearer(HTTPBearer, AuthHandler,_Schema_Admin):
    def __init__(self, permission_type:int ,auto_error: bool = True):
        self.permission = permission_type
        self.super_admin= ord(self.admin_permit())
        super(AuthHandler,self).__init__()
        super(JWTBearer, self).__init__(auto_error=auto_error,scheme_name='Authorization')

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            verify = await self.verify_jwt(credentials.credentials)
            if not verify:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")    
            user_permissions = verify['permission']
            role_id = verify['role_type']
            company_id = verify['company_id']
            role_permit = await RoleOperation().fetch_by_role_id(role_id,company_id)
            role_permit = dict(role_permit[0]).get('permission')
            user_permissions.append(role_permit)
            name , email , company_id =  None , verify['email'] ,company_id 
            try:
                first = verify['first_name']
                middle= verify['middle_name']
                last =  verify['last_name']
                name = first+" "+middle+' '+last
            except:
                first = verify['first_name']
                middle= ""
                last =  verify['last_name']
                name = first+" "+last
            data={'name':name,'email':email,'company_id':company_id }

            if not self.permission in user_permissions or\
              not int(self.super_admin) in user_permissions and\
                   self.permission == int(self.super_admin):
                raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="contact to admin to access this action!")
            return data
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> dict:
        return await self.verify(jwtoken)
