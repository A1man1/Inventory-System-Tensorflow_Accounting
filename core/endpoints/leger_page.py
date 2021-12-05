from datetime import date, datetime
from typing import Optional

from core.authentication import AuthHandler, JWTBearer
from core.config import log
from core.schema import util
from core.schema.model_operation import LegerPageOperation
from core.schema.ModelOpreator.leger_page import (LegerPageSchemaCreate,
                                                  LegerPageSchemaOut)
from core.schema.trie import Trie
from core.schema.util import try_parsing_date
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/leger_page",
    tags=["leger_pages"]
)
trie_ins_title = Trie()


# Declaring auth handler for admin leger_page.
#auth_handler: AuthHandler = AuthHandler("admin")

# Declaring leger_page repository for all crud methods.
legerpage: LegerPageOperation = LegerPageOperation()


@router.get("/", dependencies=[Depends(JWTBearer(100))] , name="leger_pagelist:fetch_leger_page_list")
# , current_leger_page=Depends(auth_handler.authorize)):
async def leger_page_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of leger_page

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_pages (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    # if current_leger_page['leger_page_type'] == "super_admin":
    try:
        leger_pages = await legerpage.list(**commons)
        if commons["limit"] == 0:
            return leger_pages
        else:
            return {
                "offset": commons["skip"],
                "limit": commons["limit"],
                "results": leger_pages
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


@router.get("/{leger_page_id}", dependencies=[Depends(JWTBearer(16))], name="leger_page detials:fetch_leger_page_by_id",response_model=LegerPageSchemaOut)
async def get_leger_page_by_id(leger_page_id: int): #,current_leger_page=Depends(auth_handler.authorize)):
    """Fetch leger_page by ID

    Args:
        leger_page_id (int): leger_page id
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_page: Fetched leger_page object.
    """
    try:
        return await legerpage.fetch_by_id(leger_page_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("/company", dependencies=[Depends(JWTBearer(16))],name="leger_page detials:fetch_leger_page_by_company_id")
async def get_leger_page_by_company_id(company_id: int, title:Optional[str]=None, issue_finished:Optional[bool]=None, date:Optional[date]=None): #,current_leger_page=Depends(auth_handler.authorize)):
    """Fetch leger_page by ID

    Args:
        leger_page_id (int): leger_page id
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_page: Fetched leger_page object.
    """
    try:
        list_data = await legerpage.fetch_by_company_id(company_id)
        dict_data = {}
        list_add=[]
        if title is not None:
            for data in list_data:
                trie_ins_title.insert(data.title,data)
    
            dict_data['by_title']=list_add
            list_add.clear()
        
        if issue_finished is not None:
            for data in list_data:
                if data.issue_finised == issue_finished:
                    list_add.append(data)

            dict_data['by_issued']=list_add
            list_add.clear()

        if date is not None:
            check_date = try_parsing_date(date)
            check_date = datetime(data.date,check_date).strptime('%d/%m/%Y')
            for data in list_data:
               compare_date = try_parsing_date(data.date)
               compare_date = datetime(data.date,compare_date).strptime('%d/%m/%Y')
               if check_date == compare_date:
                   list_add.append(data)

            dict_data['by_date']=list_add

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/", dependencies=[Depends(JWTBearer(4))],name="create_leger_page",response_model=LegerPageSchemaOut,status_code=status.HTTP_201_CREATED)
async def create_leger_page(app: LegerPageSchemaCreate):#, current_leger_page=Depends(auth_handler.authorize)):
    """Create new leger_page

    Args:
        app (leger_pageCreate): Payload for leger_page create
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_page: Created leger_page object
    """
    try:
        return await legerpage.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{leger_page_id}", dependencies=[Depends(JWTBearer(8))],  name="leger_page:update_leger_page_data_by_id",response_model=LegerPageSchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_leger_page(leger_page_id: int, app: LegerPageSchemaCreate): #, current_leger_page=Depends(auth_handler.authorize)):
    """Update leger_page object

    Args:
        leger_page_id (int): leger_page id
        app (leger_pageUpdate): Payload for leger_page update
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        leger_page (leger_pageOut): Updated leger_page object
    """
    try:
        return await legerpage.update(leger_page_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{leger_page_id}", dependencies=[Depends(JWTBearer(10))], name="leger_page:delete_leger_page_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_leger_page_by_id(leger_page_id: int): #, current_leger_page=Depends(auth_handler.authorize)):
    """Delete leger_page

    Args:
        leger_page_id (int): leger_page id
        current_leger_page (leger_page, optional): Request leger_page object. Defaults to Depends(auth_handler.authorize).

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await legerpage.delete_by_id(leger_page_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
