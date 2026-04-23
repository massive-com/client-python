import json
import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    refresh_tickers: bool = False
    start_date: str = "2026-01"
    data_source_priority: List[str] = field(
        default_factory=lambda: ["massive", "akshare", "yfinance"]
    )
    market_cap_min: float = 1_000_000_000
    akshare_interval: float = 2.0
    yfinance_interval: float = 1.0
    massive_interval: float = 12.0
    list_data_dir: str = "data/us_list"
    daily_data_dir: str = "data/us_daily"
    max_retries: int = 3


def load_config(config_path: str = None) -> Config:
    config = Config()
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
    return config
