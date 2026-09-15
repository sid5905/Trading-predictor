import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Trading Predictor")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
MARKET_DATA_PROVIDER = os.getenv("MARKET_DATA_PROVIDER", "demo")
