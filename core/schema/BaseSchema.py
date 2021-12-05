import abc
from datetime import datetime
from typing import Dict, List, Mapping, Optional, Union

import sqlalchemy
from sqlalchemy.sql.functions import current_date , current_timestamp
from sqlalchemy.sql.sqltypes import TIMESTAMP
from core.config import log
from core.dbconfig.db_engin import db
from core.schema.util import utc_now
from databases import Database
from fastapi import HTTPException, status
from pydantic import BaseConfig, BaseModel, validator


class IDModelMixin(BaseModel):
    """
    Schema to return Id field for all model schemas.
    """
    id: Optional[int]


class ModifiedTimeModelMixin(BaseModel):
    """
    Model Mixin for created and updated timestamp information tables.
    """
    last_modified_at: Optional[datetime] = current_timestamp

        
class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True


class BaseRepository(abc.ABC):
    """Base repository for all database tables.

    Args:
        abc.ABC (Class): Abstract base class.
    """

    def __init__(self, db: Database = db, *args, **kwargs) -> None:
        self._db = db
        super()

    @property
    @abc.abstractmethod
    def _schema_create(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_update(self):
        pass

    @property
    @abc.abstractmethod
    def _table(self) -> sqlalchemy.Table:
        pass

    @property
    @abc.abstractmethod
    def _schema_out(self):
        pass

    def _preprocess_create(self, values: Union[BaseSchema, Dict]) -> Dict:
        if isinstance(values, dict):
            values = self._schema_create(**values)
        return dict(values)

    def _preprocess_update(self, values: Union[BaseSchema, Dict]) -> Dict:
        if isinstance(values, dict):
            values = self._schema_update(**values)
        return dict(values)

    async def _list(self) -> List[Mapping]:
        query = self._table.select()
        return await self._db.fetch_all(query=query)

    async def _paginated_list(self, limit: int, skip: int) -> List[Mapping]:
        query = self._table.select().limit(limit).offset(skip)
        return await self._db.fetch_all(query=query)

    async def _fetch_by_id(self, id: int) -> Mapping:
        query = self._table.select().where(self._table.c.id == id)
        rec = await self._db.fetch_one(query=query)
        if not rec:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Not Found: { self._table.name.capitalize() } Object with ID { id }")
        return rec

    async def _delete_by_id(self, id: int):
        query = self._table.delete().where(self._table.c.id == id)
        return await self._db.execute(query=query)

    async def count_records(self) -> int:
        query = self._table.count()
        return await self._db.execute(query=query)

    async def list(self, **kwargs):
        if "limit" in kwargs.keys() and kwargs["limit"] == 0:
            rows = await self._list()
        else:
            rows = await self._paginated_list(kwargs["limit"], kwargs["skip"])
        return [self._schema_out(**dict(row.items())) for row in rows]

    async def fetch_by_id(self, id: int) -> BaseSchema:
        record = await self._fetch_by_id(id)
        return self._schema_out(**dict(record.items()))

    async def create(self, values: Union[BaseSchema, Dict]) -> BaseSchema:
        dict_values = self._preprocess_create(values)
        print(dict_values)
        query = self._table.insert()
        record_id = await self._db.execute(query=query, values=dict_values)
        return await self.fetch_by_id(record_id)

    async def update(self, id: int, values: Union[BaseSchema, Dict]) -> BaseSchema:
        await self._fetch_by_id(id)
        dict_values = self._preprocess_update(values)
        values = {k: v for k, v in dict_values.items() if v is not None}

        if len(values) >= 1:
            query = self._table.update().where(self._table.c.id == id)
            await self._db.execute(query=query, values=values)

        return await self.fetch_by_id(id)

    async def delete_by_id(self, id: int) -> Dict:
        await self._fetch_by_id(id)
        await self._delete_by_id(id)
        return {"msg": f"Object ID { id } deleted successfully"}

