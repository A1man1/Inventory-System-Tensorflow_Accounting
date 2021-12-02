import typing 
from datetime import date
from typing import Optional
from uuid import uuid4
from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema



class OrderSchema(BaseSchema):
    title: Optional[str]
    first_name:Optional[str]
    middle_name:Optional[str]
    last_name:Optional[str]
    number_shipped:Optional[str]
    order_date:Optional[date]
    product_id:Optional[int]    
    company_id:Optional[int]


class OrderSchemaCreate(OrderSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    Order_number:Optional[str] = str(uuid4())


class OrderSchemaUpdate(OrderSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class OrderSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, OrderSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class OrderSchemaOut(OrderSchemaInDB):
    Order_number:Optional[str]



