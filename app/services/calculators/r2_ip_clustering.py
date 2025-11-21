# app/services/calculators/r2_ip_clustering.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.repositories.transaction_repository import TransactionRepository
from app.config.settings import settings


class IpClusteringCalculator(FeatureCalculator):
    """
    R2 – unique_cards_on_ip
    """

    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        if not txn.ip_address:
            return

        features.unique_cards_on_ip = self.repo.count_unique_cards_on_ip_last_minutes(
            ip_address=txn.ip_address,
            window_minutes=settings.velocity_window_minutes,
            now=txn.timestamp
        )
