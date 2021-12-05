from typing import Optional

from core.authentication import AuthHandler, JWTBearer
from core.config import log
from core.schema import util
from core.schema.model_operation import SuppilerOperation
from core.schema.ModelOpreator.supplier import (SuppilersSchemaCreate,
                                                SuppilersSchemaOut)
from core.schema.trie import Trie
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter(
    prefix="/suppiler",
    tags=["suppilers"]
)

#Trie 
trie_ins = Trie()
# Declaring auth handler for admin suppiler.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring suppiler repository for all crud methods.
suppiler_repo: SuppilerOperation = SuppilerOperation()


@router.get("/",dependencies=[Depends(JWTBearer(100))], name="suppilerlist:fetch_suppiler_list")
# , current_suppiler=Depends(auth_handler.authorize)):
async def suppiler_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of suppiler

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppilers (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_suppiler['suppiler_type'] == "super_admin":
    try:
        suppilers = await suppiler_repo.list(**commons)
        if commons["limit"] == 0:
            return suppilers
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": suppilers
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


@router.get("/{suppiler_id}", dependencies=[Depends(JWTBearer(34))],name="suppiler detials:fetch_suppiler_by_id",response_model=SuppilersSchemaOut)
async def get_suppiler_by_id(suppiler_id: int): 
    """Fetch suppiler by ID

    Args:
        suppiler_id (int): suppiler id
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler: Fetched suppiler object.
    """
    try:
        return await suppiler_repo.fetch_by_id(suppiler_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/suppilers/", dependencies=[Depends(JWTBearer(34))],name="suppiler detials:company suppiler list and search name")
async def get_suppiler_by_company_and_search(company_id:int,suppiler_name:Optional[str] = None): 
    """Fetch suppiler by ID

    Args:
        suppiler_name (str): suppiler name
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler: Fetched suppiler object.
    """
    try:
        data= await suppiler_repo.fetch_by_company_id(company_id)
        if suppiler_name is None or suppiler_name.isspace():
            return  data
            
        [trie_ins.insert(items.name,items) for items in data]
        return trie_ins.search(suppiler_name)
           

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/name/", dependencies=[Depends(JWTBearer(34))],name="suppiler detials:fetch_suppiler_by_name")
async def get_suppiler_supper_by_name(suppiler_name:str): 
    """Fetch suppiler by NAME

    Args:
        suppiler_name (str): suppiler name
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler: Fetched suppiler object.
    """
    try:
        
        return await suppiler_repo.fetch_by_supplier_name(suppiler_name) 

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/products/", dependencies=[Depends(JWTBearer(34))],name="suppiler detials:fetch_suppiler_product_by_name")
async def get_suppiler_product_list(suppiler_id:int , company_id:int): 
    """Fetch suppiler by name

    Args:
        suppiler_name (str): suppiler name
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler: Fetched suppiler object.
    """
    try:
        return await suppiler_repo.fetch_product_list_of_suppiler(suppiler_id,company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")





@router.post("/", dependencies=[Depends(JWTBearer(32))], name="create_suppiler",response_model=SuppilersSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_suppiler(app: SuppilersSchemaCreate):
    """Create new suppiler

    Args:
        app (suppilerCreate): Payload for suppiler create
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler: Created suppiler object
    """
    try:
        return await suppiler_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{suppiler_id}", dependencies=[Depends(JWTBearer(38))] , name="suppiler:update_suppiler_data_by_id",response_model=SuppilersSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_suppiler(suppiler_id: int, app: SuppilersSchemaCreate): 
    """Update suppiler object

    Args:
        suppiler_id (int): suppiler id
        app (suppilerUpdate): Payload for suppiler update
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        suppiler (suppilerOut): Updated suppiler object
    """
    try:
        return await suppiler_repo.update(suppiler_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{suppiler_id}", dependencies=[Depends(JWTBearer(36))], name="suppiler:delete_suppiler_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_suppiler_by_id(suppiler_id: int): 
    """Delete suppiler

    Args:
        suppiler_id (int): suppiler id
        current_suppiler (suppiler, optional): Request suppiler object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await suppiler_repo.delete_by_id(suppiler_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
