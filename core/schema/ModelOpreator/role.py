import typing 
from typing import Optional
from core.schema.ModelOpreator.company import CompanyDetailSchema
from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema


class RoleSchema(BaseSchema):
    company_id: Optional[int]
    role_name: Optional[str]
    permission: Optional[typing.List[int]]

class RoleSchemaCreate(RoleSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class RoleSchemaUpdate(RoleSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class RoleSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, RoleSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class RoleSchemaOut(RoleSchemaInDB):
    pass



