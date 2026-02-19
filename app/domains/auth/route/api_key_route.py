# app/domains/auth/api/api_key_route.py
 
from fastapi import APIRouter, Request, Depends
from app.domains.auth.schemas.api_key_schema import (
    BasicKeyRequest, BasicKeyResponse, ListKeyResponse,
    DeactKeyRequest, DeactKeyResponse,
)
from app.domains.auth.services.api_key_service import BasicKeyService
from app.application.guards.service_guard import service_guard

router = APIRouter(prefix="/security", tags=["Security"])

def get_service() -> BasicKeyService:
    return BasicKeyService()

@router.post("/create-api-key", response_model=BasicKeyResponse, 
    dependencies=[Depends(service_guard("create_api_key"))]
)
async def create_api_key(request: Request, 
        params: BasicKeyRequest, 
        service: BasicKeyService = Depends(get_service)
    ):

    request.state.payload = params.model_dump()
    res = service.create_key(params.user)
    return {
        "request_id": getattr(request.state, "request_id", "unknown"),
        **res,
        }

@router.get("/list-api-key", response_model=ListKeyResponse, 
            dependencies=[Depends(service_guard("list_api_key"))]
            )
async def list_api_keys(request: Request,
    params: BasicKeyRequest = Depends(), 
    service: BasicKeyService = Depends(get_service)
):
    
    result = service.list_key(params.user)

    return {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "result": result,
    }

@router.patch("/deact-api-key", response_model=DeactKeyResponse, 
              dependencies=[Depends(service_guard("deact_api_key"))]
              )
async def deactivate_key(request: Request, 
                         params: DeactKeyRequest, 
                         service: BasicKeyService = Depends(get_service)
                         ):
    
    msg = service.deactivate_key(params.ID)

    return {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "result": msg,
    }

@router.patch("/act-api-key", response_model=DeactKeyResponse, 
              dependencies=[Depends(service_guard("act_api_key"))]
              )
async def activate_key(request: Request, 
                       params: DeactKeyRequest, 
                       service: BasicKeyService = Depends(get_service)
                       ):

    msg = service.activate_key(params.ID)

    return {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "result": msg,
    }