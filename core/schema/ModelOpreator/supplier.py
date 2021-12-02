from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema
import typing 
from typing import Optional
from core.schema.ModelOpreator.company import CompanyDetailSchema
from core.schema.ModelOpreator.product import ProductSchema

class SuppilersSchema(BaseSchema):
    name: Optional[str]
    tax_type:Optional[str]
    company_tax_id:Optional[str]
    address: Optional[str]
    areacode: Optional[str]
    country: Optional[str]
    city: Optional[str]
    email: Optional[str]
    contact_number: Optional[typing.List[str]]
    company_id: Optional[int]


class SuppilersSchemaCreate(SuppilersSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class SuppilersSchemaUpdate(SuppilersSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class SuppilersSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, SuppilersSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class SuppilersSchemaOut(SuppilersSchemaInDB):
    pass



