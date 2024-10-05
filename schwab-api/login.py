from schwab_api import Schwab 
import pprint

# Initialize our schwab instance
#browser = playwright.chromium.launch(headless=False)
api = Schwab(headless=False, session_cache="session.json")

# Login using playwright
print("Logging into Schwab")
logged_in = api.login(
    username="chenxuehua",
    password="&&WbkgWTa2vT",
    totp_secret="ASCCXLYYOV655SJ3WQZAULLTIIHW3BVH", # Get this by generating TOTP at https://itsjafer.com/#/schwab
    lazy = True,
)

# Get information about a few tickers
quotes = api.quote_v2(["PFE", "AAPL"])
pprint.pprint(quotes)

# Get information about all accounts holdings
print("Getting account holdings information")
account_info = api.get_account_info()
pprint.pprint(account_info)

print("Getting account holdings informration v2")
account_info = api.get_account_info_v2()
pprint.pprint(account_info)

print("The following account numbers were found: " + str(account_info.keys()))

pprint.pprint(account_info[13492844])

isSuccess, result = api.get_lot_info_v2(13492844, 1737167066)
print("isSuccess: ", isSuccess)
pprint.pprint(result)
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