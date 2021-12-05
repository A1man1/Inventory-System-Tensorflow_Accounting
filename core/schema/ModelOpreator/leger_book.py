import typing
from typing import Optional

from core.schema.BaseSchema import (BaseSchema, IDModelMixin,
                                    ModifiedTimeModelMixin)
from core.schema.ModelOpreator.company import CompanyDetailSchema


class LegerBookSchema(BaseSchema):
    name:Optional[str]
    company_id:Optional[int]
    year_declare:Optional[int]



class LegerBookSchemaCreate(LegerBookSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass

class LegerBookSchemaUpdate(LegerBookSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class LegerBookSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, LegerBookSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class LegerBookSchemaOut(LegerBookSchemaInDB):
    pass



