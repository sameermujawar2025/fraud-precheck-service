# app/services/calculators/base.py
from abc import ABC, abstractmethod
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector


class FeatureCalculator(ABC):
    """
    Each calculator updates ONLY its own feature(s) in FeatureVector.
    """

    @abstractmethod
    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        ...
