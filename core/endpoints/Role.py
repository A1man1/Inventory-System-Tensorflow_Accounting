from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT
from core.authentication import AuthHandler
from core.schema.model_operation import RoleOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.role import  RoleSchemaOut, RoleSchemaCreate
from core.authentication import JWTBearer
router = APIRouter(
    prefix="/role",
    tags=["Role"]
)

# Declaring auth handler for admin user.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring app_provider repository for all crud methods.
role_repo: RoleOperation = RoleOperation()


@router.get("/", dependencies=[Depends(JWTBearer('Admin'))],name="userlist:fetch_user_list")
# , current_user=Depends(auth_handler.authorize)):
async def role_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of role

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        role (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_user['role_type'] == "super_admin":
    try:
        app_providers = await role_repo.list(**commons)
        if commons["limit"] == 0:
            return app_providers
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": app_providers
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


@router.get("/{role_id}",dependencies=[Depends(JWTBearer('Admin'))], name="role detials:fetch_role_by_id",response_model=RoleSchemaOut)
async def get_app_provider_by_id(role_id: int): #,current_user=Depends(auth_handler.authorize)):
    """Fetch Role by ID

    Args:
        app_provider_id (int): Role id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Role: Fetched Role object.
    """
    try:
        return await role_repo.fetch_by_id(role_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", name="create_register_role",dependencies=[Depends(JWTBearer('Admin'))],response_model=RoleSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_app_provider(app: RoleSchemaCreate):#, current_user=Depends(auth_handler.authorize)):
    """Create new Role

    Args:
        app (RoleCreate): Payload for Role create
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Role: Created Role object
    """
    try:
        print( await role_repo.create(app))
        return await role_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{role_id}", dependencies=[Depends(JWTBearer('Admin'))],name="role:update_role_data_by_id",response_model=RoleSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_app_provider(role_id: int, app: RoleSchemaCreate): #, current_user=Depends(auth_handler.authorize)):
    """Update Role object

    Args:
        app_provider_id (int): Role id
        app (RoleUpdate): Payload for Role update
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Role (RoleOut): Updated Role object
    """
    try:
        return await role_repo.update(role_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{role_id}", dependencies=[Depends(JWTBearer('Admin'))], name="role:delete_role_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_app_provider_by_id(app_provider_id: int): #, current_user=Depends(auth_handler.authorize)):
    """Delete Role

    Args:
        app_provider_id (int): Role id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await role_repo.delete_by_id(app_provider_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
