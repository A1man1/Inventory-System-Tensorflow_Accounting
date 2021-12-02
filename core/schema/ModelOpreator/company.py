import enum
import typing 
from typing import Optional 
from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema


class CompanyDetailSchema(BaseSchema):
    name: Optional[str]
    tax_type: Optional[str]
    company_tax_id: Optional[str]
    address: Optional[str]
    areacode: Optional[str]
    country: Optional[str]
    city: Optional[str]
    email: Optional[str]
    contact_number: Optional[typing.List[str]]

class compnaySchemaCreate(CompanyDetailSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class CompanySchemaUpdate(CompanyDetailSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class CompanySchemaInDB(IDModelMixin, ModifiedTimeModelMixin, CompanyDetailSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class CompanySchemaOut(CompanySchemaInDB):
    pass



