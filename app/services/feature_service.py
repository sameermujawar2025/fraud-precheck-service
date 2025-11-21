# app/services/feature_service.py
from typing import List
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector, FeatureResponse
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.blacklist_repository import BlacklistRepository

from app.services.calculators.base import FeatureCalculator
from app.services.calculators.r1_card_testing_velocity import CardTestingVelocityCalculator
from app.services.calculators.r2_ip_clustering import IpClusteringCalculator
from app.services.calculators.r3_decline_spikes import DeclineSpikesCalculator
from app.services.calculators.r4_impossible_travel import ImpossibleTravelCalculator
from app.services.calculators.r5_last_amount_spike import LastAmountSpikeCalculator
from app.services.calculators.r6_country_change import CountryChangeCalculator
from app.services.calculators.r7_night_time_flag import NightTimeFlagCalculator
from app.services.calculators.r8_high_value_flag import HighValueFlagCalculator
from app.services.calculators.r9_blacklist_flag import BlacklistFlagCalculator


class FeatureService:
    """
    Orchestrates all feature calculators.
    SRP: knows HOW to build FeatureVector for a transaction.
    """

    def __init__(
        self,
        txn_repo: TransactionRepository,
        bl_repo: BlacklistRepository
    ):
        self.txn_repo = txn_repo
        self.bl_repo = bl_repo

        # Dependency injection of calculators (Open/Closed)
        self.calculators: List[FeatureCalculator] = [
            CardTestingVelocityCalculator(self.txn_repo),
            IpClusteringCalculator(self.txn_repo),
            DeclineSpikesCalculator(self.txn_repo),
            ImpossibleTravelCalculator(self.txn_repo),
            LastAmountSpikeCalculator(self.txn_repo),
            CountryChangeCalculator(self.txn_repo),
            NightTimeFlagCalculator(),
            HighValueFlagCalculator(),
            BlacklistFlagCalculator(self.bl_repo),
        ]

    def compute_features(
        self,
        txn: TransactionRequest
    ) -> FeatureResponse:
        features = FeatureVector()

        for calc in self.calculators:
            calc.calculate(txn, features)

        return FeatureResponse(features=features)
