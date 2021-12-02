from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT
from core.authentication import AuthHandler
from core.schema.model_operation import PurchaseOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.purchase import  PurchaseSchemaOut, PurchaseSchemaCreate

router = APIRouter(
    prefix="/purchase",
    tags=["Purchase"]
)

# Declaring auth handler for admin user.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring purchase repository for all crud methods.
purchase_repo: PurchaseOperation = PurchaseOperation()


@router.get("/", name="userlist:fetch_purchase_list")
# , current_user=Depends(auth_handler.authorize)):
async def Purchase_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of Purchase

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        users (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_user['Purchase_type'] == "super_admin":
    try:
        purchases = await purchase_repo.list(**commons)
        if commons["limit"] == 0:
            return purchases
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": purchases
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


@router.get("/{purchase_id}", name="Purchase detials:fetch_Purchase_by_id",response_model=PurchaseSchemaOut)
async def get_purchase_by_id(purchase_id: int): #,current_user=Depends(auth_handler.authorize)):
    """Fetch Purchase by ID

    Args:
        purchase_id (int): Purchase id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Purchase: Fetched Purchase object.
    """
    try:
        return await purchase_repo.fetch_by_id(purchase_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", name="create_Purchase",response_model=PurchaseSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_purchase(app: PurchaseSchemaCreate):#, current_user=Depends(auth_handler.authorize)):
    """Create new Purchase

    Args:
        app (PurchaseCreate): Payload for Purchase create
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Purchase: Created Purchase object
    """
    try:
        return await purchase_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{Purchase_id}", name="Purchase:update_Purchase_data_by_id",response_model=PurchaseSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_purchase(Purchase_id: int, app: PurchaseSchemaCreate): #, current_user=Depends(auth_handler.authorize)):
    """Update Purchase object

    Args:
        purchase_id (int): Purchase id
        app (PurchaseUpdate): Payload for Purchase update
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Purchase (PurchaseOut): Updated Purchase object
    """
    try:
        return await purchase_repo.update(Purchase_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{purchase_id}", name="Purchase:delete_Purchase_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_purchase_by_id(purchase_id: int): #, current_user=Depends(auth_handler.authorize)):
    """Delete Purchase

    Args:
        purchase_id (int): Purchase id
        current_user (User, optional): Request User object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await purchase_repo.delete_by_id(purchase_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")