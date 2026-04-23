import json
import os


def get_tickers_file_path(data_dir: str) -> str:
    return os.path.join(data_dir, "top_tickers.json")


def get_month_file_path(data_dir: str, ticker: str, month: str) -> str:
    return os.path.join(data_dir, ticker, f"{month}.json")


def get_year_file_path(data_dir: str, ticker: str, year: int) -> str:
    return os.path.join(data_dir, ticker, f"{year}.json")


def save_json(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def file_exists(path: str) -> bool:
    return os.path.isfile(path)
