from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema
from datetime import date
from typing import Optional
import typing 
from pydantic import ValidationError, validator

class UserSchema(BaseSchema):
    company_id: Optional[int] 
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    


class UserSchemaCreate(UserSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    role_type: Optional[int] = 0
    permission:Optional[typing.List[int]] = []
    is_active:Optional[bool] = True
    passwd: Optional[str]


class UserSchemaUpdate(UserSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    
    is_active:Optional[bool]
    permission:Optional[typing.List[int]]


class UserSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, UserSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class UserSchemaOut(UserSchemaInDB):
    role_type: Optional[int]
    registered_date: Optional[date]
    is_active:Optional[bool]
    permission:Optional[typing.List[int]]


