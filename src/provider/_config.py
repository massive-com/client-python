# -*- coding: utf-8 -*-
"""
Slim configuration singleton for provider module.

Reads configuration from environment variables. Only includes attributes
actually used by provider fetchers.
"""

import os
from dataclasses import dataclass
from threading import Lock
from typing import Optional


# ---------------------------------------------------------------------------
# normalize_report_language  (extracted from src/report_language.py)
# ---------------------------------------------------------------------------

SUPPORTED_REPORT_LANGUAGES = ("zh", "en")

_REPORT_LANGUAGE_ALIASES = {
    "zh-cn": "zh", "zh_cn": "zh", "zh-hans": "zh", "zh_hans": "zh",
    "zh-tw": "zh", "zh_tw": "zh", "cn": "zh", "chinese": "zh",
    "english": "en", "en-us": "en", "en_us": "en", "en-gb": "en", "en_gb": "en",
}


def normalize_report_language(value: Optional[str], default: str = "zh") -> str:
    """Normalize report language to a supported short code."""
    candidate = (value or default).strip().lower().replace(" ", "_")
    candidate = _REPORT_LANGUAGE_ALIASES.get(candidate, candidate)
    return candidate if candidate in SUPPORTED_REPORT_LANGUAGES else default


# ---------------------------------------------------------------------------
# Config singleton
# ---------------------------------------------------------------------------

@dataclass
class Config:
    # Tushare
    tushare_token: str = ""
    # Longbridge
    longbridge_app_key: str = ""
    longbridge_app_secret: str = ""
    longbridge_access_token: str = ""
    # TickFlow
    tickflow_api_key: str = ""
    # Feature toggles
    enable_eastmoney_patch: bool = True
    enable_realtime_quote: bool = True
    enable_chip_distribution: bool = True
    enable_fundamental_pipeline: bool = True
    prefetch_realtime_quotes: bool = True
    # Realtime source priority
    realtime_source_priority: str = "tencent,akshare,efinance"
    # Fundamental pipeline
    fundamental_fetch_timeout_seconds: float = 30.0
    fundamental_stage_timeout_seconds: float = 60.0
    fundamental_cache_ttl_seconds: int = 3600
    fundamental_cache_max_entries: int = 256
    fundamental_retry_max: int = 2


_instance: Optional[Config] = None
_lock = Lock()


def _env_bool(key: str, default: str = "true") -> bool:
    return os.environ.get(key, default).lower() != "false"


def get_config() -> Config:
    """Return the global Config singleton, creating it on first call."""
    global _instance
    if _instance is not None:
        return _instance
    with _lock:
        if _instance is not None:
            return _instance
        _instance = Config(
            tushare_token=os.environ.get("TUSHARE_TOKEN", ""),
            longbridge_app_key=os.environ.get("LONGBRIDGE_APP_KEY", ""),
            longbridge_app_secret=os.environ.get("LONGBRIDGE_APP_SECRET", ""),
            longbridge_access_token=os.environ.get("LONGBRIDGE_ACCESS_TOKEN", ""),
            tickflow_api_key=os.environ.get("TICKFLOW_API_KEY", ""),
            enable_eastmoney_patch=_env_bool("ENABLE_EASTMONEY_PATCH"),
            enable_realtime_quote=_env_bool("ENABLE_REALTIME_QUOTE"),
            enable_chip_distribution=_env_bool("ENABLE_CHIP_DISTRIBUTION"),
            enable_fundamental_pipeline=_env_bool("ENABLE_FUNDAMENTAL_PIPELINE"),
            prefetch_realtime_quotes=_env_bool("PREFETCH_REALTIME_QUOTES"),
            realtime_source_priority=os.environ.get(
                "REALTIME_SOURCE_PRIORITY", "tencent,akshare,efinance"
            ),
            fundamental_fetch_timeout_seconds=float(
                os.environ.get("FUNDAMENTAL_FETCH_TIMEOUT_SECONDS", "30")
            ),
            fundamental_stage_timeout_seconds=float(
                os.environ.get("FUNDAMENTAL_STAGE_TIMEOUT_SECONDS", "60")
            ),
            fundamental_cache_ttl_seconds=int(
                os.environ.get("FUNDAMENTAL_CACHE_TTL_SECONDS", "3600")
            ),
            fundamental_cache_max_entries=int(
                os.environ.get("FUNDAMENTAL_CACHE_MAX_ENTRIES", "256")
            ),
            fundamental_retry_max=int(
                os.environ.get("FUNDAMENTAL_RETRY_MAX", "2")
            ),
        )
        return _instance
