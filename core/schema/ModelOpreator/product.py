import re 
from typing import Optional
from fastapi.exceptions import HTTPException
from starlette import status

from core.schema.BaseSchema import (BaseSchema, IDModelMixin,
                                    ModifiedTimeModelMixin)
from pydantic import HttpUrl , validator


class ProductSchema(BaseSchema):
    company_id:Optional[int]
    product_name: Optional[str] 
    product_number: Optional[str]
    product_label: Optional[str]
    starting_inventory: Optional[int]
    inventory_received: Optional[int]
    inventory_shipped: Optional[int]
    inventory_onhand: Optional[int]
    price: Optional[float]
    minimum_required: Optional[int]
    product_image: Optional[HttpUrl]
    supplier_id: Optional[int]

    @validator("product_image", pre=True, always=True)
    def default_image_product(cls, value:HttpUrl) -> HttpUrl:
        if not re.match('',value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="needs image url of product")
        return  value 


class ProductSchemaCreate(ProductSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class ProductSchemaUpdate(ProductSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class ProductSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, ProductSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class ProductSchemaOut(ProductSchemaInDB):
    pass



