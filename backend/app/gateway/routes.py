from fastapi import APIRouter

from app.gateway.policies import ACCESS_POLICIES


router = APIRouter(
    prefix="/gateway",
    tags=["API Gateway"]
)


@router.get("/status")
def gateway_status():
    return {
        "gateway": "Fresh Bowl API Gateway",
        "status": "active",
        "policy_count": len(ACCESS_POLICIES)
    }


@router.get("/policies")
def gateway_policies():
    return {
        "policies": ACCESS_POLICIES
    }