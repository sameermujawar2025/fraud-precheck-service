# app/services/calculators/r7_night_time_flag.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector


class NightTimeFlagCalculator(FeatureCalculator):
    """
    R7 – hour_of_day (rule-engine can decide risk)
    """

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        features.hour_of_day = txn.timestamp.hour
