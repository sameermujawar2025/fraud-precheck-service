# app/config/settings.py
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    app_name: str = "fraud-feature-service"
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME", "tao-fda-db")

    # Collections (aligned with your doc)
    txn_collection_name: str = os.getenv("TXN_COLLECTION_NAME", "transactions_90_days")
    blacklist_collection_name: str = os.getenv("BLACKLIST_COLLECTION_NAME", "blacklist")

    # Feature thresholds (can be tuned / moved to rule-engine later)
    velocity_window_minutes: int = int(os.getenv("VELOCITY_WINDOW_MINUTES", "10"))
    decline_window_minutes: int = int(os.getenv("DECLINE_WINDOW_MINUTES", "10"))
    high_value_threshold: float = float(os.getenv("HIGH_VALUE_THRESHOLD", "5000"))
    card_test_amount_max: float = float(os.getenv("CARD_TEST_AMOUNT_MAX", "10"))

    # For impossible travel
    max_speed_kmph: float = float(os.getenv("MAX_SPEED_KMPH", "900"))

    # Night time window (UTC hours)
    night_start_hour: int = int(os.getenv("NIGHT_START_HOUR", "0"))
    night_end_hour: int = int(os.getenv("NIGHT_END_HOUR", "4"))


settings = Settings()
