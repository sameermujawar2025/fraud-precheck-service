# app/services/blacklist_service.py
from app.models.blacklist_models import (
    BlacklistCheckRequest,
    BlacklistCheckResponse,
    BlacklistMatch,
)
from app.repositories.blacklist_repository import BlacklistRepository


class BlacklistService:
    def __init__(self, repo: BlacklistRepository):
        self.repo = repo

    def check(
        self,
        req: BlacklistCheckRequest
    ) -> BlacklistCheckResponse:
        matches_raw = self.repo.find_matches(
            user_id=req.user_id,
            card_number=req.card_number,
            ip_address=req.ip_address
        )
        matches = [
            BlacklistMatch(
                user_id=m.get("user_id"),
                card_number=str(m.get("card_number")) if m.get("card_number") else None,
                ip_address=m.get("ip_address"),
                reason=m.get("reason", ""),
                source=m.get("source", "")
            )
            for m in matches_raw
        ]
        return BlacklistCheckResponse(
            is_blacklisted=bool(matches),
            matches=matches
        )
