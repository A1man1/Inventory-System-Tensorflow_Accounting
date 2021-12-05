from core.authentication import JWTBearer
from core.config import log
from core.schema import util
from core.schema.model_operation import LegerBookOperation
from core.schema.ModelOpreator.leger_book import (LegerBookSchemaCreate,
                                                  LegerBookSchemaOut)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/leger_books",
    tags=["leger_bookss"]
)

# Declaring leger_books repository for all crud methods.
legerbook: LegerBookOperation = LegerBookOperation()


@router.get("/", dependencies=[Depends(JWTBearer(100))],name="leger_bookslist:fetch_leger_books_list")
async def leger_books_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of leger_books

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_leger_books (leger_books, optional): Request leger_books object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_bookss (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_leger_books['leger_books_type'] == "super_admin":
    try:
        leger_bookss = await legerbook.list(**commons)
        if commons["limit"] == 0:
            return leger_bookss
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": leger_bookss
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


@router.get("/{leger_books_id}", dependencies=[Depends(JWTBearer(16))], name="leger_books detials:fetch_leger_books_by_id",response_model=LegerBookSchemaOut)
async def get_leger_books_by_id(leger_books_id: int): 
    """Fetch leger_books by ID

    Args:
        leger_books_id (int): leger_books id
        current_leger_books (leger_books, optional): Request leger_books object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_books: Fetched leger_books object.
    """
    try:
        return await legerbook.fetch_by_id(leger_books_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", dependencies=[Depends(JWTBearer(2))],name="create_leger_books",response_model=LegerBookSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_leger_books(app: LegerBookSchemaCreate):
    """Create new leger_books

    Args:
        app (leger_booksCreate): Payload for leger_books create
        current_leger_books (leger_books, optional): Request leger_books object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_books: Created leger_books object
    """
    try:
        return await legerbook.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{leger_books_id}", dependencies=[Depends(JWTBearer(6))],name="leger_books:update_leger_books_data_by_id",response_model=LegerBookSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_leger_books(leger_books_id: int, app: LegerBookSchemaCreate): 
    """Update leger_books object

    Args:
        leger_books_id (int): leger_books id
        app (leger_booksUpdate): Payload for leger_books update
        current_leger_books (leger_books, optional): Request leger_books object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_books (leger_booksOut): Updated leger_books object
    """
    try:
        return await legerbook.update(leger_books_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{leger_books_id}", dependencies=[Depends(JWTBearer(12))],name="leger_books:delete_leger_books_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_leger_books_by_id(leger_books_id: int): 
    """Delete leger_books

    Args:
        leger_books_id (int): leger_books id
        current_leger_books (leger_books, optional): Request leger_books object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await legerbook.delete_by_id(leger_books_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
