# app/services/calculators/r8_high_value_flag.py
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.config.settings import settings


class HighValueFlagCalculator(FeatureCalculator):
    """
    R8 – high_value_flag
    """

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        features.high_value_flag = txn.amount >= settings.high_value_threshold
