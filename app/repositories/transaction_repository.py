# app/repositories/transaction_repository.py
from datetime import datetime, timedelta
from typing import List
from pymongo.collection import Collection

from app.repositories.mongo_client import MongoClientFactory
from app.config.settings import settings


class TransactionRepository:
    """
    Read-only repository over fraud_transactions_90_days
    used for velocity, behaviour, geo features.
    """

    def __init__(self):
        db = MongoClientFactory.get_db()
        self.col: Collection = db[settings.txn_collection_name]

    def _window_query(self, field_filter: dict, window_minutes: int, now: datetime):
        start = now - timedelta(minutes=window_minutes)
        q = {
            "timestamp": {"$gte": start, "$lte": now},
            **field_filter
        }
        return q

    def count_txns_last_minutes_for_card(
        self,
        card_number: str,
        window_minutes: int,
        now: datetime
    ) -> int:
        q = self._window_query({"card_number": card_number}, window_minutes, now)
        return self.col.count_documents(q)

    def count_unique_cards_on_ip_last_minutes(
        self,
        ip_address: str,
        window_minutes: int,
        now: datetime
    ) -> int:
        q = self._window_query({"ip_address": ip_address}, window_minutes, now)
        return len(self.col.distinct("card_number", q))

    def get_txn_stats_last_minutes(
        self,
        user_id: str | None,
        card_number: str | None,
        window_minutes: int,
        now: datetime
    ) -> tuple[int, int]:
        """
        Returns: (total_count, decline_count) in the window.
        """
        filt = {}
        if user_id:
            filt["user_id"] = user_id
        if card_number:
            filt["card_number"] = card_number

        q = self._window_query(filt, window_minutes, now)
        total = self.col.count_documents(q)
        decline = self.col.count_documents({**q, "txn_status": "DECLINED"})
        return total, decline

    def get_last_successful_txn_for_user_card(
        self,
        user_id: str | None,
        card_number: str | None,
        before_time: datetime
    ):
        filt = {"txn_status": "APPROVED", "timestamp": {"$lt": before_time}}
        if user_id:
            filt["user_id"] = user_id
        if card_number:
            filt["card_number"] = card_number

        return self.col.find_one(
            filt,
            sort=[("timestamp", -1)]
        )
