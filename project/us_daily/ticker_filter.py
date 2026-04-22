import logging
import time
from typing import List

from project.us_daily.config import Config

logger = logging.getLogger("us_daily")

EXCHANGES = ["XNAS", "XNYS", "ARCX"]


def filter_top_tickers(client, config: Config) -> List[dict]:
    result = []
    for exchange in EXCHANGES:
        logger.info(f"Fetching tickers for exchange: {exchange}")
        try:
            tickers = client.list_tickers(
                market="stocks",
                exchange=exchange,
                active=True,
                limit=1000,
            )
        except Exception as e:
            logger.error(f"Failed to list tickers for {exchange}: {e}")
            continue

        time.sleep(config.request_interval)

        for ticker_obj in tickers:
            ticker_str = ticker_obj.ticker
            try:
                details = client.get_ticker_details(ticker_str)
                time.sleep(config.request_interval)
            except Exception as e:
                logger.warning(f"Failed to get details for {ticker_str}: {e}")
                continue

            if details.market_cap is None:
                logger.debug(f"{ticker_str}: no market_cap data, skipping")
                continue

            if details.market_cap >= config.market_cap_min:
                entry = {
                    "ticker": details.ticker,
                    "name": details.name,
                    "market_cap": details.market_cap,
                    "exchange": details.primary_exchange,
                }
                result.append(entry)
                logger.info(
                    f"  {details.ticker}: market_cap={details.market_cap:.0f} included"
                )
            else:
                logger.debug(
                    f"  {ticker_str}: market_cap={details.market_cap:.0f} < {config.market_cap_min:.0f}, skipping"
                )

    logger.info(f"Total top tickers found: {len(result)}")
    return result
