from fastapi import APIRouter

from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.companies import router as companies_router
from app.api.v1.endpoints.drafts import router as drafts_router
from app.api.v1.endpoints.research import router as research_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(research_router, tags=["research"])
api_router.include_router(companies_router, tags=["companies"])
api_router.include_router(drafts_router, tags=["drafts"])
api_router.include_router(analytics_router, tags=["analytics"])