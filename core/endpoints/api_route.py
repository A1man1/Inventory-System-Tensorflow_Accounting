from core.endpoints.company import router as companydetils
from core.endpoints.leger_book import router as Book
from core.endpoints.leger_page import router as Page
from core.endpoints.Order import router as Order
from core.endpoints.Product import router as Products
from core.endpoints.Purchase import router as Purchase
from core.endpoints.Role import router as Role
from core.endpoints.Suppilers import router as Supplier
from core.endpoints.User import router as User
from fastapi import APIRouter

router = APIRouter()

router.include_router(companydetils)
router.include_router(Products)
router.include_router(User)
router.include_router(Role)
router.include_router(Purchase)
router.include_router(Supplier)
router.include_router(Order)
router.include_router(Book)
router.include_router(Page)

