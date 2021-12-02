from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT, HTTP_406_NOT_ACCEPTABLE
from core.authentication import AuthHandler
from core.schema.model_operation import ProductOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.product import  ProductSchemaOut, ProductSchemaCreate
from core.schema.trie import Trie


router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

trie_ins = Trie()
# Declaring auth handler for admin product.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring product repository for all crud methods.
product_repo: ProductOperation = ProductOperation()


@router.get("/", name="productlist:fetch_product_list")
# , current_product=Depends(auth_handler.authorize)):
async def product_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of product

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Product (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_product['role_type'] == "super_admin":
    try:
        products = await product_repo.list(**commons)
        if commons["limit"] == 0:
            return products
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": products
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


@router.get("/{product_id}", name="product detials:fetch_product_by_id",response_model=ProductSchemaOut)
async def get_product_by_id(product_id: int): #,current_product=Depends(auth_handler.authorize)):
    """Fetch App provider by ID

    Args:
        product_id (int): App provider id
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        App provider: Fetched app provider object.
    """
    try:
        return await product_repo.fetch_by_id(product_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/company/", name="product detials:fetch_product_by_company_id_search_product")
async def get_product_by_company_id_search_product(company_id: int, product_name:Optional[str]=None): #,current_product=Depends(auth_handler.authorize)):
    """Fetch App provider by Name

    Args:
        company_id (int): company id
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        Product : Fetched product object.
    """
    try:
        if company_id is None:
            raise HTTPException(status_code=HTTP_204_NO_CONTENT,detail="no query!")
        
        list_data = await product_repo.fetch_by_company_id(company_id)
        
        if  product_name is None or product_name.isspace():    
            return list_data
        else:
            for data in list_data:
                trie_ins.insert(data.product_name,data)
            return trie_ins.search(product_name)


    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")



@router.get("/name/", name="product detials:fetch_product_by_name")
async def get_product_by_name(product_name: str, company_id:int): #,current_product=Depends(auth_handler.authorize)):
    """Fetch App provider by Name

    Args:
        product_name (str): Name of Product
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        App provider: Fetched app provider object.
    """
    try:
        if product_name is None or product_name.isspace():
            raise HTTPException(status_code=HTTP_204_NO_CONTENT,detail="no query!")
        list_data = await product_repo.fetch_by_product_name(product_name,company_id)
        return list_data

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", name="create_register_product",response_model=ProductSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_product(app: ProductSchemaCreate):#, current_product=Depends(auth_handler.authorize)):
    """Create new App provider

    Args:
        app (AppProviderCreate): Payload for app provider create
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        App provider: Created app provider object
    """
    try:
        return await product_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{product_id}", name="product:update_product_data_by_id",response_model=ProductSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_product(product_id: int, app: ProductSchemaCreate): #, current_product=Depends(auth_handler.authorize)):
    """Update App provider object

    Args:
        product_id (int): App provider id
        app (AppProviderUpdate): Payload for app provider update
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        App provider (AppProviderOut): Updated app provider object
    """
    try:
        return await product_repo.update(product_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{product_id}", name="product:delete_product_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(product_id: int): #, current_product=Depends(auth_handler.authorize)):
    """Delete app provider

    Args:
        product_id (int): App provider id
        current_product (product, optional): Request product object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await product_repo.delete_by_id(product_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
