import json
import concurrent.futures
from typing import Any, Dict
from massive import RESTClient

# Initialize Massive API client
client = RESTClient(
    trace=True
)  # Assuming you have MASSIVE_API_KEY environment variable set up

# Initialize the data structure to hold SIC code groups
sic_code_groups: Dict[str, Dict[str, Any]] = {}


# https://en.wikipedia.org/wiki/Standard_Industrial_Classification
# https://www.investopedia.com/terms/s/sic_code.asp
def sic_code_to_group(sic_code):
    """
    Maps a given SIC code to the industry group.
    """
    sic_code = int(sic_code)
    if 100 <= sic_code <= 999:
        return "Agriculture, Forestry and Fishing"
    elif 1000 <= sic_code <= 1499:
        return "Mining"
    elif 1500 <= sic_code <= 1799:
        return "Construction"
    # Note: 1800-1999 not used
    elif 2000 <= sic_code <= 3999:
        return "Manufacturing"
    elif 4000 <= sic_code <= 4999:
        return "Transportation and Public Utilities"
    elif 5000 <= sic_code <= 5199:
        return "Wholesale Trade"
    elif 5200 <= sic_code <= 5999:
        return "Retail Trade"
    elif 6000 <= sic_code <= 6799:
        return "Finance, Insurance and Real Estate"
    elif 7000 <= sic_code <= 8999:
        return "Services"
    elif 9100 <= sic_code <= 9729:
        return "Public Administration"
    elif 9900 <= sic_code <= 9999:
        return "Nonclassifiable"
    else:
        return None


def process_ticker(ticker_snapshot):
    ticker = ticker_snapshot.ticker

    try:
        details = client.get_ticker_details(ticker)

        # Check if the type is 'CS' (common stock), if not, return early without processing this ticker
        # if getattr(details, 'type', None) != 'CS' or getattr(details, 'market_cap', None) != None:
        if (
            getattr(details, "type", None) != "CS"
            or getattr(details, "market_cap", None) is None
        ):
            return

        sic_code = details.sic_code
        sic_description = getattr(
            details, "sic_description", None
        )  # Use getattr to avoid AttributeError if sic_description is not present
        market_cap = getattr(details, "market_cap", None)

        # if sic_code:
        #    sic_code = str(sic_code)[:1]  # Extract first 1 digits

        if sic_code:
            sic_group = sic_code_to_group(sic_code)
            if sic_group is None:
                return

            # Check if the sic_code is already in the groups, if not create a new entry with sic_description and empty companies list
            # if sic_code not in sic_code_groups:
            #    sic_code_groups[sic_code] = {"sic_description": sic_description, "companies": []}

            if sic_group not in sic_code_groups:
                sic_code_groups[sic_group] = {
                    "sic_description": sic_group,
                    "companies": [],
                }

            # Append the company details to the corresponding SIC code entry
            # sic_code_groups[sic_code]["companies"].append({
            #    "ticker": ticker,
            #    "market_cap": market_cap
            # })

            sic_code_groups[sic_group]["companies"].append(
                {"ticker": ticker, "market_cap": market_cap}
            )

    except Exception as e:
        print(f"Error processing ticker {ticker}: {e}")


# Get snapshot data
snapshot = client.get_snapshot_all("stocks")

# Execute the data processing in parallel, limited to 100 workers
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(process_ticker, snapshot)

# Modify the SIC Code Groups Dictionary to include the weights
for sic_code, group_data in sic_code_groups.items():
    companies = group_data["companies"]
    total_market_cap = sum(
        company["market_cap"] for company in companies if company["market_cap"]
    )

    # If total_market_cap is 0, we will skip weight calculation to avoid division by zero
    if total_market_cap == 0:
        continue

    for company in companies:
        if company[
            "market_cap"
        ]:  # Avoid dividing by zero if a company's market cap is None or 0
            company["weight"] = company["market_cap"] / total_market_cap
        else:
            company["weight"] = 0  # You can also set to a default value if preferred

# Save the enhanced data structure to a JSON file
with open("sic_code_groups.json", "w") as f:
    json.dump(sic_code_groups, f)

print("Data collection complete and saved to 'sic_code_groups.json'")
