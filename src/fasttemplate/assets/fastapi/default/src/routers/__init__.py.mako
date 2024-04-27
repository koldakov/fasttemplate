from fastapi import APIRouter

from .root import router as router_root

router: APIRouter = APIRouter()
router.include_router(router_root)
