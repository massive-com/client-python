import json
import os
from dataclasses import dataclass


@dataclass
class Config:
    refresh_tickers: bool = False
    market_cap_min: float = 5e9
    start_date: str = "2020-01"
    request_interval: int = 20
    data_dir: str = "data/us_daily"
    max_retries: int = 3


def load_config(config_path: str = "project/us_daily/config.json") -> Config:
    config = Config()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
    return config
