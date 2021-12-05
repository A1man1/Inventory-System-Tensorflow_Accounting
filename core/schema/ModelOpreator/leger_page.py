import typing
from datetime import date
from typing import Optional

from core.schema.BaseSchema import (BaseSchema, IDModelMixin,
                                    ModifiedTimeModelMixin)
from core.schema.ModelOpreator.leger_book import LegerBookSchema


class LegerPageSchema(BaseSchema):
    leger_book:Optional[int]
    date:Optional[date]
    title:Optional[str]
    description:Optional[str]
    billno:Optional[str]
    total_amount:Optional[int]
    balance_amount:Optional[int]
    issue_finised:Optional[bool]


class LegerPageSchemaCreate(LegerPageSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass

class LegerPageSchemaUpdate(LegerPageSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class LegerPageSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, LegerPageSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class LegerPageSchemaOut(LegerPageSchemaInDB):
    pass



