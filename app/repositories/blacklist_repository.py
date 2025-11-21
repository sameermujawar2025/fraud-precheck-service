# app/repositories/blacklist_repository.py
from typing import List, Dict
from pymongo.collection import Collection

from app.repositories.mongo_client import MongoClientFactory
from app.config.settings import settings


class BlacklistRepository:
    def __init__(self):
        db = MongoClientFactory.get_db()
        self.col: Collection = db[settings.blacklist_collection_name]

    def find_matches(
        self,
        user_id: str | None,
        card_number: str | None,
        ip_address: str | None
    ) -> List[Dict]:
        or_clauses = []
        if user_id:
            or_clauses.append({"user_id": user_id})
        if card_number:
            or_clauses.append({"card_number": card_number})
        if ip_address:
            or_clauses.append({"ip_address": ip_address})

        if not or_clauses:
            return []

        q = {"$or": or_clauses}
        return list(self.col.find(q))
