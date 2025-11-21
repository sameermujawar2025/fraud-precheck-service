# app/models/blacklist_models.py
from pydantic import BaseModel
from typing import Optional, List, Dict


class BlacklistCheckRequest(BaseModel):
    user_id: Optional[str] = None
    card_number: Optional[str] = None
    ip_address: Optional[str] = None


class BlacklistMatch(BaseModel):
    user_id: Optional[str] = None
    card_number: Optional[str] = None
    ip_address: Optional[str] = None
    reason: str
    source: str


class BlacklistCheckResponse(BaseModel):
    is_blacklisted: bool
    matches: List[BlacklistMatch]
