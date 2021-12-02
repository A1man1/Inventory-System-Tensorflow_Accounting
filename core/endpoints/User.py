from typing import Optional
import typing
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT
from core.authentication import AuthHandler
from core.schema.model_operation import UserOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.user import  UserSchemaOut , UserSchemaCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Declaring auth handler for admin user.
auth_handler: AuthHandler = AuthHandler()

# Declaring user repository for all crud methods.
user_repo: UserOperation = UserOperation()


@router.get("/", name="userlist:fetch_user_list")
# , current_user=Depends(auth_handler.authorize)):
async def user_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of user

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        users (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_user['role_type'] == "super_admin":
    try:
        users = await user_repo.list(**commons)
        if commons["limit"] == 0:
            return users
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": users
            }

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
    # else:
    #    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"detial: {'You are not authorized this area!'}")


@router.get("/{user_id}", name="user detials:fetch_user_by_id",response_model=UserSchemaOut)
async def get_user_by_id(user_id: int): #,current_user=Depends(auth_handler.authorize)):
    """Fetch Users by ID

    Args:
        user_id (int): Users id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await user_repo.fetch_by_id(user_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/company/", name="user detials:fetch_user_by_company_id")
async def get_user_by_company_id(company_id: int): #,current_user=Depends(auth_handler.authorize)):
    """Fetch Users by company Name

    Args:
        company_id (int): Company id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await user_repo.fetch_by_user_by_company_id(company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/assgin/", name="update permission",response_model=UserSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def get_user_by_update_permission(user_id:int, permission:Optional[typing.List[int]]=None): #,current_user=Depends(auth_handler.authorize)):
    """
    Updating user permission
    
    Args:
        company_id (int): Company id
        user_id (int): User id
        permission (list): permission list in number

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await user_repo.assign_permission_to_user(user_id=user_id, permission=permission)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/activate/", name="activate user profile",response_model=UserSchemaOut, status_code=status.HTTP_202_ACCEPTED)
async def get_user_by_company_id(user_id:int): #,current_user=Depends(auth_handler.authorize)):
    """
    activate user 
    
    Args:
        user_id (int): User id

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await user_repo.active_to_account(user_id=user_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/assign_role/", name="assign role user",response_model=UserSchemaOut, status_code=status.HTTP_202_ACCEPTED)
async def get_user_by_company_id(user_id:int, role_id_type:int): #,current_user=Depends(auth_handler.authorize)):
    """
    activate user 
    
    Args:
        user_id (int): User id

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await user_repo.assign_role_to_account(user_id,role_id_type)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")



@router.post("/", name="register_user",response_model=UserSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_user(app: UserSchemaCreate):#, current_user=Depends(auth_handler.authorize)):
    """Create new Users

    Args:
        app (AppProviderCreate): Payload for Users create
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Created Users object
    """
    try:
        return await user_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{user_id}", name="user:update_user_data_by_id",response_model=UserSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, app: UserSchemaCreate): #, current_user=Depends(auth_handler.authorize)):
    """Update Users object

    Args:
        user_id (int): Users id
        app (AppProviderUpdate): Payload for Users update
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users (AppProviderOut): Updated Users object
    """
    try:
        return await user_repo.update(user_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{user_id}", name="user:delete_user_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int): #, current_user=Depends(auth_handler.authorize)):
    """Delete Users

    Args:
        user_id (int): Users id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await user_repo.delete_by_id(user_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/authenticate/", name="encrypted authorize", status_code=status.HTTP_200_OK)
async def authenticate(user:str, passwd:str):
    """
    activate user 
    
    Args:
        user_id (int): User id

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Users: Fetched Users object.
    """
    try:
        return await  auth_handler.login(user,passwd)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
