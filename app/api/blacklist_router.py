# app/api/blacklist_router.py
from fastapi import APIRouter, Depends
from app.models.blacklist_models import (
    BlacklistCheckRequest,
    BlacklistCheckResponse,
)
from app.services.blacklist_service import BlacklistService
from app.repositories.blacklist_repository import BlacklistRepository


router = APIRouter(
    prefix="/blacklist",
    tags=["blacklist"]
)


def get_blacklist_service() -> BlacklistService:
    repo = BlacklistRepository()
    return BlacklistService(repo)


@router.post("/check", response_model=BlacklistCheckResponse)
def check_blacklist(
    request: BlacklistCheckRequest,
    service: BlacklistService = Depends(get_blacklist_service)
) -> BlacklistCheckResponse:
    """
    Direct blacklist lookup for a user/card/IP.

    Request:
    {
      "user_id": "U0999",
      "card_number": "4555666677778888",
      "ip_address": "192.168.1.200"
    }

    Response:
    {
      "is_blacklisted": true,
      "matches": [
        {
          "user_id": "U0999",
          "card_number": null,
          "ip_address": null,
          "reason": "Confirmed Fraud",
          "source": "csv"
        }
      ]
    }
    """
    return service.check(request)
