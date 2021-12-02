from datetime import date
from uuid import uuid4
from typing import Optional
from core.schema.BaseSchema import IDModelMixin, ModifiedTimeModelMixin, BaseSchema



class PurchaseSchema(BaseSchema):
    name: Optional[str]
    suppiler_id: Optional[int]
    product_id: Optional[int]
    company_id: Optional[int]
    number_of_recevied: Optional[int]
    purchsase_date: Optional[date]
    

class PurchaseSchemaCreate(PurchaseSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    Billno: Optional[str] = uuid4()


class PurchaseSchemaUpdate(PurchaseSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class PurchaseSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, PurchaseSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class PurchaseSchemaOut(PurchaseSchemaInDB):
    Billno: Optional[str]
