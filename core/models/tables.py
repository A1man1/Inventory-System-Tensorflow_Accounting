from datetime import date, datetime
from uuid import uuid1, uuid3, uuid4

from core.dbconfig.db_engin import metadata
from sqlalchemy import (Boolean, Column, Date, DateTime, Integer, String,
                        Table, Text)
from sqlalchemy.sql.functions import current_date, current_time, now
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY, Enum, Float
#from sqlalchemy_imageattach.entity import Image ,  image_attachment
from sqlalchemy_utils import URLType

CompanyDetail= Table(
    "company_detail",metadata
    ,Column("id", Integer, primary_key=True, index=True)
    ,Column("name",String, unique=True,nullable=False)
    ,Column("tax_type",Enum("VAT","GST",name="tax_category"),default='GST')
    ,Column("company_tax_id",String,unique=True,nullable=False)
    ,Column("address",String,nullable=False) 
    ,Column("areacode",String,nullable=False) 
    ,Column("country",String,nullable=False)
    ,Column("city",String,nullable=False)
    ,Column("email",String, unique=True,nullable=False)
    ,Column ("contact_number",ARRAY(String),nullable=False)
    ,Column("last_modified_at", DateTime(timezone=True),onupdate=now(),server_default=now(),nullable=False))


Product=Table(
    "product",metadata
    ,Column("id", Integer, primary_key=True, index=True)
    ,Column("company_id",ForeignKey('company_detail.id',ondelete="CASCADE"),nullable=True)
    ,Column("supplier_id",ForeignKey('suppiler.id',ondelete="CASCADE"))
    ,Column("product_name",String)
    ,Column("product_number",String,unique=True)
    ,Column("product_label",String,nullable=True)
    ,Column("price",Float,nullable=True)
    ,Column("starting_inventory",Integer,nullable=True)
    ,Column("inventory_received",Integer,nullable=True)
    ,Column("inventory_shipped",Integer,nullable=True)
    ,Column("inventory_onhand",Integer,nullable=True)
    ,Column("minimum_required",Integer,nullable=True)
    ,Column("modified_date",Date,default=datetime.today(),nullable=True)
    ,Column('product_image',URLType)
    ,Column("last_modified_at", DateTime(timezone=True),onupdate=now(), server_default=now(), nullable=False))
 

Suppilers=Table(
    "suppiler",metadata
    ,Column("id", Integer, primary_key=True, index=True)
    ,Column("name",String, unique=True)
    ,Column("tax_type",Enum("VAT","GST",name="tax_category"),nullable=False)
    ,Column("company_tax_id",String,unique=True)
    ,Column("address",String) 
    ,Column("areacode",String) 
    ,Column("country",String)
    ,Column("city",String)
    ,Column("email",String, unique=True)
    ,Column ("contact_number",ARRAY(String))
    ,Column("company_id",ForeignKey('company_detail.id',ondelete="CASCADE"))
    ,Column("last_modified_at", DateTime(timezone=True),onupdate=now(), server_default=now(), nullable=False))

Purchase=Table(
    "purchase",metadata
    ,Column("id",Integer,primary_key=True, index=True)
    ,Column("company_id",Integer, ForeignKey('company_detail.id',ondelete="CASCADE"))
    ,Column("suppiler_id",Integer,ForeignKey('suppiler.id',ondelete="CASCADE"))
    ,Column("product_id",Integer,ForeignKey('product.id',ondelete="CASCADE"))
    ,Column("Number_of_recived",Integer,nullable=True)
    ,Column("Billno",String,nullable=False,server_default=str(uuid1().hex[:5])+str(date.year))
    ,Column ("purchsase_date",Date,nullable=True, index=True))

Order=Table(
    "order",metadata
    ,Column("id",Integer,primary_key=True,index=True)
    ,Column("title",String,unique=True)
    ,Column("first_name",String,nullable=True)
    ,Column("middle_name",String,nullable=True)
    ,Column("last_name",String,nullable=True)
    ,Column("company_id",Integer,ForeignKey('company_detail.id',ondelete="CASCADE"))
    ,Column("product_id",Integer,ForeignKey('product.id',ondelete="CASCADE"))
    ,Column("number_shipped",String,server_default=str(uuid4))
    ,Column("Order_number",String, server_default=str(uuid3))
    ,Column("order_date",Date,default=current_time,nullable=True))


LegerBook=Table(
    "leger_book",metadata
    ,Column("id",Integer,primary_key=True, index=True)
    ,Column("name",String, unique=True, nullable=False) 
    ,Column("company_id",Integer,ForeignKey('company_detail.id',ondelete="CASCADE"))
    ,Column("year_declare",Integer,default=datetime.today().year))


Leger_page=Table(
    "leger_page" ,metadata
    ,Column("id",Integer,primary_key=True, index=True)
    ,Column("leger_id",Integer,ForeignKey('leger_book.id',ondelete="CASCADE")) 
    ,Column("date",Date, default=current_date)
    ,Column("title",String,unique=True)
    ,Column("descrption",Text , nullable=True)
    ,Column("billno",String, nullable=True)
    ,Column("total_amount",Integer, nullable=True)
    ,Column("balance_amount",Integer, nullable=True)
    ,Column("issue_finised",Boolean, nullable=True))

Role=Table(
    "role",metadata
    ,Column('company_id',ForeignKey('company_detail.id',))
    ,Column('id',Integer,unique=True,primary_key=True, index=True)
    ,Column("role_name",String,unique=True)
    ,Column("permission",ARRAY(Integer),nullable=True))


User=Table(
    "users",metadata
    ,Column('id',Integer,primary_key=True, index=True)
    ,Column("company_id",ForeignKey('company_detail.id'))
    ,Column("role_type",ForeignKey("role.id"),nullable=True)
    ,Column("first_name",String)
    ,Column("last_name",String)
    ,Column("middle_name",String, nullable=True)
    ,Column("email",String, nullable=False,unique=True)
    ,Column("phone",String, nullable=False,unique=True)
    ,Column("registered_date",Date,default=current_date)
    ,Column("permission",ARRAY(Integer,as_tuple=True),nullable=True)
    ,Column("passwd",String, nullable=False,server_default='abc@123')
    ,Column("is_active", Boolean, nullable=False, server_default="False"))
