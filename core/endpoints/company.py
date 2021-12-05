import sys
import pathlib
from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, status, Security
from starlette.status import HTTP_204_NO_CONTENT, HTTP_406_NOT_ACCEPTABLE

from core.authentication import AuthHandler , JWTBearer
from core.schema.model_operation import CompanyDetailOperation, RoleOperation
from core.config import log
from core.schema import util
from core.schema.ModelOpreator.company import compnaySchemaCreate, CompanySchemaOut

router = APIRouter(
    prefix="/company",
    tags=["Company"]
)

# Declaring auth handler
token_auth_scheme = HTTPBearer()
auth_handler: AuthHandler = AuthHandler()
role_gardian:RoleOperation = RoleOperation()

# Declaring company repository for all crud methods.
company_repo: CompanyDetailOperation = CompanyDetailOperation()


@router.get("/items/", dependencies=[Depends(JWTBearer(100))],name="companylist:fetch_companies_list") 
async def company_list(commons: dict = Depends(util.common_parameters)):
    """Fetch list of company

    Args:
        commons (dict, optional): Contains optional query params. Defaults to Depends(common_parameters).
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        compnay (List): Fetch paginated list except if limit is 0 returns list of objects.
    """
    try:
            companys = await company_repo.list(**commons)
            if commons["limit"] == 0:
                return companys
            else:
                return {
                    "offset": commons["skip"],
                    "limit": commons["limit"],
                    "results": companys
                }

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
        #else:
        #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"detial: {'You are not authorized this area!'}")


@router.get("/{company_id}",dependencies=[Depends(JWTBearer(100))],name="company detials:fetch_company_by_id",response_model=CompanySchemaOut)
async def get_company_by_id(company_id: int ):
    """Fetch CompanyDetail by ID

    Args:
        company_id (int): CompanyDetail id
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        CompanyDetail: Fetched CompanyDetail object.
    """
    try:
        return await company_repo.fetch_by_id(company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.get("", dependencies=[Depends(JWTBearer(100))] ,name="company detials:fetch_company_by_name")
async def get_company_by_name(company_name: str):
    """Fetch CompanyDetail by ID

    Args:
        company_id (int): CompanyDetail id
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        CompanyDetail: Fetched CompanyDetail object.
    """
    try:
        if company_name is None:
            raise HTTPException(status_code=HTTP_204_NO_CONTENT,detail="no query!")
        elif len(company_name) < 3:
            raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE, detail="needs more than 10 keys for search")
        list_data = await company_repo.fetch_by_company_name(company_name)
        return [list_data]

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/",name="create_register_company",response_model=CompanySchemaOut,status_code=status.HTTP_201_CREATED)
async def create_company(app: compnaySchemaCreate):
    """Create new CompanyDetail

    Args:
        app (CompanyDetailCreate): Payload for CompanyDetail create
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        CompanyDetail: Created CompanyDetail object
    """
    try:
        return await company_repo.create(app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.put("/{company_id}", dependencies=[Depends(JWTBearer(55))], name="company:update_company_data_by_id",response_model=CompanySchemaOut,status_code=status.HTTP_202_ACCEPTED)
async def update_company(company_id: int, app: compnaySchemaCreate):
    """Update CompanyDetail object

    Args:
        company_id (int): CompanyDetail id
        app (CompanyDetailUpdate): Payload for CompanyDetail update
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        CompanyDetail (CompanyDetailOut): Updated CompanyDetail object
    """
    try:
        return await company_repo.update(company_id, app)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.delete("/{company_id}", dependencies=[Depends(JWTBearer(100))],name="company:delete_company_info_by_id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_by_id(company_id: int):
    """Delete CompanyDetail

    Args:
        company_id (int): CompanyDetail id
        current_user (User, optional): Request User object. Defaults to Depends().

    Raises:
        HTTPException: Exception if some error occurred with proper status code

    Returns:
        None: No content with 204 status code
    """
    try:
        return await company_repo.delete_by_id(company_id)

    except Exception as err:
        log.error(err)
        if hasattr(err, 'status_code'):
            raise HTTPException(status_code=err.status_code, detail=err.detail)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
