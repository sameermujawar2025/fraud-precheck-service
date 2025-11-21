# app/services/calculators/r4_impossible_travel.py
from datetime import timezone
from app.services.calculators.base import FeatureCalculator
from app.models.transaction_models import TransactionRequest
from app.models.feature_models import FeatureVector
from app.repositories.transaction_repository import TransactionRepository
from app.utils.geo import haversine_km, compute_speed_kmph


class ImpossibleTravelCalculator(FeatureCalculator):
    """
    R4 – distance_from_last_location_km, speed_kmph
    """

    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def calculate(
        self,
        txn: TransactionRequest,
        features: FeatureVector
    ) -> None:
        if txn.current_latitude is None or txn.current_longitude is None:
            return

        last = self.repo.get_last_successful_txn_for_user_card(
            user_id=txn.user_id,
            card_number=txn.card_number,
            before_time=txn.timestamp
        )
        if not last:
            return

        last_lat = last.get("current_latitude")
        last_lon = last.get("current_longitude")
        last_ts = last.get("timestamp")

        if last_lat is None or last_lon is None or last_ts is None:
            return

        if last_ts.tzinfo is None:
            last_ts = last_ts.replace(tzinfo=timezone.utc)
        if txn.timestamp.tzinfo is None:
            current_ts = txn.timestamp.replace(tzinfo=timezone.utc)
        else:
            current_ts = txn.timestamp

        dt = (current_ts - last_ts).total_seconds() / 3600.0
        if dt <= 0:
            return

        dist = haversine_km(
            lat1=last_lat,
            lon1=last_lon,
            lat2=txn.current_latitude,
            lon2=txn.current_longitude,
        )
        speed = compute_speed_kmph(dist, dt)

        features.distance_from_last_location_km = dist
        features.speed_kmph = speed
