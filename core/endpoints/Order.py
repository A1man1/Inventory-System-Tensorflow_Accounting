from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT
from core.authentication import AuthHandler
from core.schema.model_operation import OrdersOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.order import  OrderSchemaOut, OrderSchemaCreate
from core.authentication import JWTBearer

router = APIRouter(
    prefix="/order",
    tags=["Orders"]
)

# Declaring auth handler for admin order.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring order repository for all crud methods.
order_repo: OrdersOperation = OrdersOperation()


@router.get("/",dependencies=[Depends(JWTBearer(100))], name="orderlist:fetch_order_list")

async def order_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of order

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        orders (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_order['order_type'] == "super_admin":
    try:
        orders = await order_repo.list(**commons)
        if commons["limit"] == 0:
            return orders
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": orders
            }

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/{order_id}", dependencies=[Depends(JWTBearer(100))],name="order detials:fetch_order_by_id",response_model=OrderSchemaOut)
async def get_order_by_id(order_id: int): 
    """Fetch order by ID

    Args:
        order_id (int): order id
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        order: Fetched order object.
    """
    try:
        return await order_repo.fetch_by_id(order_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/company/", dependencies=[Depends(JWTBearer(42))],name="order detials:fetch_order_by_id",response_model=OrderSchemaOut)
async def get_order_by_company_id(order_id: int,company_id:int):
    """Fetch order by ID and company ID

    Args:
        order_id (int): order id
        company_id (int): company id
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        order: Fetched order object.
    """
    try:
        return await order_repo.fetch_by_company_id(order_id,company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/product/", dependencies=[Depends(JWTBearer(42))],name="order detials:fetch_order_by_product_id",response_model=OrderSchemaOut)
async def get_order_by_product_id(product_id:int, company_id:int):
    """Fetch order by Product ID and company ID

    Args:
        product_id (int): Product id
        company_id (int): company id
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        order: Fetched order object.
    """
    try:
        return await order_repo.fetch_by_product_id(product_id,company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", dependencies=[Depends(JWTBearer(40))],name="create_order",response_model=OrderSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_order(app: OrderSchemaCreate):#, current_order=Depends(auth_handler.authorize)):
    """Create new order

    Args:
        app (orderCreate): Payload for order create
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        order: Created order object
    """
    try:
        print( await order_repo.create(app))
        return await order_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{order_id}", dependencies=[Depends(JWTBearer(46))], name="order:update_order_data_by_id",response_model=OrderSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: int, app: OrderSchemaCreate): #, current_order=Depends(auth_handler.authorize)):
    """Update order object

    Args:
        order_id (int): order id
        app (orderUpdate): Payload for order update
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        order (orderOut): Updated order object
    """
    try:
        return await order_repo.update(order_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{order_id}", dependencies=[Depends(JWTBearer(44))],name="order:delete_order_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(order_id: int): #, current_order=Depends(auth_handler.authorize)):
    """Delete order

    Args:
        order_id (int): order id
        current_order (order, optional): Request order object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await order_repo.delete_by_id(order_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
