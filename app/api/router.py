
from fastapi import APIRouter
from app.api.employee_route.routes import router as employee_router
from app.api.attendanc_route.routes import router as attendant_router
from app.api.admin.routes import router as admin_router


router = APIRouter(prefix="/api/v1")

router.include_router(employee_router)
router.include_router(attendant_router)
router.include_router(admin_router)

