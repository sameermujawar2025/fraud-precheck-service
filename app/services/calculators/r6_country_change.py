# app/services/calculators/r6_country_change.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.repositories.transaction_repository import TransactionRepository


class CountryChangeCalculator(FeatureCalculator):
    """
    R6 – country_change_flag
    """

    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        if not txn.current_country:
            return

        last = self.repo.get_last_successful_txn_for_user_card(
            user_id=txn.user_id,
            card_number=txn.card_number,
            before_time=txn.timestamp
        )
        if not last:
            return

        last_country = last.get("current_country")
        if not last_country:
            return

        features.country_change_flag = (last_country != txn.current_country)
