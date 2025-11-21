# app/services/calculators/r5_last_amount_spike.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.repositories.transaction_repository import TransactionRepository


class LastAmountSpikeCalculator(FeatureCalculator):
    """
    R5 – amount_zscore (simplified: (current - last_amount) / last_amount)
    """

    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        last = self.repo.get_last_successful_txn_for_user_card(
            user_id=txn.user_id,
            card_number=txn.card_number,
            before_time=txn.timestamp
        )
        if not last:
            return

        last_amount = last.get("amount")
        if not last_amount or last_amount <= 0:
            return

        # crude Z-score-like ratio
        features.amount_zscore = (txn.amount - last_amount) / last_amount
