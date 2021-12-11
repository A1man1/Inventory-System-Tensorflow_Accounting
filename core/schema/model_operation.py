from typing import Type

import sqlalchemy
from core.models.tables import (CompanyDetail, Leger_page, LegerBook, Order,
                                Product, Purchase, Role, Suppilers, User)
from core.schema.BaseSchema import BaseRepository
from core.schema.ModelOpreator import (company, leger_book, leger_page, order,
                                       product, purchase, role, supplier, user)
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Date


class CompanyDetailOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return CompanyDetail

    @property
    def _schema_out(self) -> Type[company.CompanySchemaOut]:
        print(company.CompanySchemaOut)
        return company.CompanySchemaOut

    @property
    def _schema_create(self) -> Type[company.compnaySchemaCreate]:
        return company.compnaySchemaCreate

    @property
    def _schema_update(self) -> Type[company.CompanySchemaUpdate]:
        return company.CompanySchemaUpdate

    async def fetch_by_company_name(self, company_name: str):
        query = self._table.select().where(self._table.c.name.like(company_name+"%"))
        rows = await self._db.fetch_all(query=query)
        data=[self._schema_out(**dict(row.items())) for row in rows]
        return data
    

class ProductOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Product

    @property
    def _schema_out(self) -> Type[product.ProductSchemaOut]:
        return product.ProductSchemaOut

    @property
    def _schema_create(self) -> Type[product.ProductSchemaCreate]:
        return product.ProductSchemaCreate

    @property
    def _schema_update(self) -> Type[product.ProductSchemaUpdate]:
        return product.ProductSchemaUpdate

    async def fetch_by_company_id(self, company_id: int):
        query = self._table.select().where(self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]

    async def fetch_by_product_name(self, product_name: str , company_id:int):
        query = self._table.select().where(self._table.c.product_name == product_name)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]


class SuppilerOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Suppilers

    @property
    def _schema_out(self) -> Type[supplier.SuppilersSchemaOut]:
        return supplier.SuppilersSchemaOut

    @property
    def _schema_create(self) -> Type[supplier.SuppilersSchemaCreate]:
        return supplier.SuppilersSchemaCreate

    @property
    def _schema_update(self) -> Type[supplier.SuppilersSchemaUpdate]:
        return supplier.SuppilersSchemaUpdate
    
    async def fetch_by_supplier_name(self,suppiler_name:str):
        query=self._table.select().where(self._table.c.name == suppiler_name)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]

    async def fetch_by_company_id(self, company_id: int):
        query = self._table.select().where(self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
        
    async def fetch_by_company_tax_id(self, tax_id:str , company_id:int):
        query = self._table.select().where(self._table.c.company_tax_id == tax_id ,self._table.c.company_id == company_id) 
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]

    async def fetch_product_list_of_suppiler(self, suppiler_id:int, company_id:int):
        query = Product.select().where(Product.c.supplier_id == suppiler_id and Product.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [ProductOperation()._schema_out(**dict(row.items())) for row in rows]
    


class PurchaseOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Purchase

    @property
    def _schema_out(self) -> Type[purchase.PurchaseSchemaOut]:
        return purchase.PurchaseSchemaOut

    @property
    def _schema_create(self) -> Type[purchase.PurchaseSchemaCreate]:
        return purchase.PurchaseSchemaCreate

    @property
    def _schema_update(self) -> Type[purchase.PurchaseSchemaUpdate]:
        return purchase.PurchaseSchemaUpdate

    async def fetch_by_suppiler_id(self, suppiler_id: int , company_id:int):
        query = self._table.select().where(self._table.c.suppiler_id == suppiler_id 
        , self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_product_id(self, product_id: int):
        query = self._table.select().where(self._table.c.suppiler_id == product_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_purchase_date(self, purchsase_date: Date ,company_id:int):
        query = self._table.select().where(self._table.c.purchsase_date == purchsase_date 
        , self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_parchase_by_company_id(self,purchase_id:int,company_id:int):
        query= self._table.select().where(self._table.c.id == purchase_id , 
        self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]

class OrdersOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Order

    @property
    def _schema_out(self) -> Type[order.OrderSchemaOut]:
        return order.OrderSchemaOut

    @property
    def _schema_create(self) -> Type[order.OrderSchemaCreate]:
        return order.OrderSchemaCreate

    @property
    def _schema_update(self) -> Type[order.OrderSchemaUpdate]:
        return order.OrderSchemaUpdate

    async def fetch_by_product_id(self, product_id: int, company_id:int):
        query = self._table.select().where(self._table.c.product_id == product_id ,
        self._table.c.compnay_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_company_id(self, compnay_id: int):
        query = self._table.select().where(self._table.c.compnay_id == compnay_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_order_date(self, order_date:Date):
        query = self._table.select().where(self._table.c.order_date == order_date)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]


class LegerBookOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return LegerBook

    @property
    def _schema_out(self) -> Type[leger_book.LegerBookSchemaOut]:
        return leger_book.LegerBookSchemaOut

    @property
    def _schema_create(self) -> Type[leger_book.LegerBookSchemaCreate]:
        return leger_book.LegerBookSchemaCreate

    @property
    def _schema_update(self) -> Type[leger_book.LegerBookSchemaUpdate]:
        return leger_book.LegerBookSchemaUpdate

    async def fetch_by_name(self, name:str):
        query = self._table.select().where(self._table.c.name == name)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_year(self, year:int):
        query = self._table.select().where(self._table.c.year_declare == year)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
       


class LegerPageOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Leger_page

    @property
    def _schema_out(self) -> Type[leger_page.LegerPageSchemaOut]:
        return leger_page.LegerPageSchemaOut

    @property
    def _schema_create(self) -> Type[leger_page.LegerPageSchemaCreate]:
        return leger_page.LegerPageSchemaCreate

    @property
    def _schema_update(self) -> Type[leger_page.LegerPageSchemaUpdate]:
        return leger_page.LegerPageSchemaUpdate

    async def fetch_by_company_id(self, company_id: int):
        query = self._table.select().where(self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_leger_date(self, leger_date: Date,company_id:int):
        query = self._table.select().where(self._table.c.leger_date == leger_date 
        , self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_leger_title(self, title:str,company_id:int):
        query = self._table.select().where(self._table.c.title == title 
        , self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def fetch_by_issue_finised(self, issue_finished:bool,company_id:int):
        query = self._table.select().where(self._table.c.issue_finished == issue_finished 
        and self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]


class UserOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return User

    @property
    def _schema_out(self) -> Type[user.UserSchemaOut]:
        return user.UserSchemaOut

    @property
    def _schema_create(self) -> Type[user.UserSchemaCreate]:
        return user.UserSchemaCreate

    @property
    def _schema_update(self) -> Type[user.UserSchemaUpdate]:
        return user.UserSchemaUpdate

    async def fetch_by_user_by_company_id(self, company_id: int):
        query = self._table.select().where(self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
    
    async def assign_permission_to_user(self, user_id:int , permission:list=None):
        query = self._table.update().where(self._table.c.id == user_id).values(
            permission=permission)
        await self._db.execute(query=query)
        rows = await self.fetch_by_id(user_id)
        return rows
    
    async def active_to_account(self,user_id):
        query = self._table.update().where(self._table.c.id == user_id).values(is_active=True)
        await self._db.execute(query=query)
        rows = await self.fetch_by_id(user_id)
        return rows
    
    async def deactive_to_account(self,user_id):
        query = self._table.update().where(self._table.c.id == user_id).values(is_active=False)
        await self._db.execute(query=query)
        rows = await self.fetch_by_id(user_id)
        return rows
    
    async def assign_role_to_account(self,user_id:int, role_type : int):
        query = self._table.update().where(self._table.c.id == user_id).values(role_type=role_type)
        await self._db.execute(query=query)
        rows = await self.fetch_by_id(user_id)
        return rows

    async def authenticate(self,user:str,passwd:str):
        query = self._table.select().where(
            self._table.c.email == user , self._table.c.passwd == passwd)
            
        rows= await self._db.fetch_all(query=query)
        
        return [self._schema_out(**dict(row.items())) for row in rows]

class RoleOperation(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Role

    @property
    def _schema_out(self) -> Type[role.RoleSchemaOut]:
        return role.RoleSchemaOut

    @property
    def _schema_create(self) -> Type[role.RoleSchemaCreate]:
        return role.RoleSchemaCreate

    @property
    def _schema_update(self) -> Type[role.RoleSchemaUpdate]:
        return role.RoleSchemaUpdate

    async def fetch_by_role_id(self, role_id: int , company_id:int):
        query = self._table.select().where(self._table.c.id == role_id , self._table.c.company_id == company_id)
        rows = await self._db.fetch_all(query=query)
        return [self._schema_out(**dict(row.items())) for row in rows]
