# app/services/calculators/r9_blacklist_flag.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.repositories.blacklist_repository import BlacklistRepository


class BlacklistFlagCalculator(FeatureCalculator):
    """
    R9 – blacklist_flag + blacklist_matches
    """

    def __init__(self, repo: BlacklistRepository):
        self.repo = repo

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        matches = self.repo.find_matches(
            user_id=txn.user_id,
            card_number=txn.card_number,
            ip_address=txn.ip_address
        )

        if matches:
            features.blacklist_flag = True
            # Keep only safe fields for response
            features.blacklist_matches = [
                {
                    "user_id": m.get("user_id"),
                    "card_number": str(m.get("card_number")) if m.get("card_number") else None,
                    "ip_address": m.get("ip_address"),
                    "reason": m.get("reason"),
                    "source": m.get("source")
                }
                for m in matches
            ]
        else:
            features.blacklist_flag = False
            features.blacklist_matches = []
