"""
Include routers from other modules.

charityproject_router: for /charity_project endpoints
donation_router: for /donation endpoints
user_router: for /auth and /user endpoints
"""

from fastapi import APIRouter

from app.api.endpoints import referral_router, user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    referral_router,
    prefix="/referral",
    tags=["Referral links"],
)
