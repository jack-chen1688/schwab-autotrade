import pprint
import os
import hydra

from schwab_ext import SchwabExt
from util import * 

home_directory = os.path.expanduser("~")
config_path = os.path.join(home_directory, "gdrive", "auth")

with hydra.initialize_config_dir(config_dir=config_path, version_base=None):
    cfg = hydra.compose(config_name="auth")

username = cfg.schwab.username
password = cfg.schwab.password
# Initialize our schwab instance
#browser = playwright.chromium.launch(headless=False)

api = SchwabExt(headless=True, session_cache="session.json")

# Login using playwright
print("Logging into Schwab")
logged_in = api.login(
    username=username,
    password=password,
    totp_secret="ASCCXLYYOV655SJ3WQZAULLTIIHW3BVH", # Get this by generating TOTP at https://itsjafer.com/#/schwab
    lazy = True,
)

# Get information about a few tickers
quotes = api.quote_v2(["PFE", "AAPL"])
pprint.pprint(quotes)

# Get information about all accounts holdings
# Note: api.get_account_info() (v1) is broken — it hits the legacy
# client.schwab.com/api/PositionV2/PositionsDataV2 endpoint, which no longer
# returns JSON. Use the v2 method instead.
print("Getting account holdings information v2")
account_info = api.get_account_info_v2()
pprint.pprint(account_info)

print("The following account numbers were found: " + str(account_info.keys()))

# Pick the first account that holds at least one position
account_id = next(a for a, info in account_info.items() if info["positions"])
pprint.pprint(account_info[account_id])

security_id = account_info[account_id]["positions"][0]["security_id"]
isSuccess, result = api.get_lot_info_v2(account_id, security_id)
print("isSuccess: ", isSuccess)
pprint.pprint(result)

csv_file_name = "realized_gain_loss.csv"
api.get_RGL(account_id=account_id, from_date="01/01/2023", to_date="07/02/2026", file_path=csv_file_name)

sort_csv_by_symbol(csv_file_name, "sorted_" + csv_file_name)
# sort the file 

total_gain_loss, gain_loss_dict  = calculate_consolidated_gain_loss(csv_file_name)

# Print the consolidated gain/loss for each underlying stock
for stock, gain_loss in sorted(gain_loss_dict.items()):
    print(f"{stock}: {'gain' if gain_loss >= 0 else 'loss'} {abs(gain_loss)}")

print(f"Total gain/loss: {total_gain_loss}")

"""
print("Placing a dry run trade for AAPL stock")

# Place a dry run trade for account 99999999
messages, success = api.trade_v2(
    ticker="AAPL", 
    side="Buy", #or Sell
    qty=1, 
    account_id=99999999, # Replace with your account number
    dry_run=True # If dry_run=True, we won't place the order, we'll just verify it.
)

print("The order verification was " + "successful" if success else "unsuccessful")
print("The order verification produced the following messages: ")
pprint.pprint(messages)
"""