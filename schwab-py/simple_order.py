import json
import httpx
from datetime import datetime

from schwab import auth, client
from schwab.orders.equities import equity_buy_limit
from schwab.orders.common import Duration, Session
from schwab.client.base import BaseClient

api_key = '6SV6Bv1os4eOgpPUc24XdhnzGITHVWEZ'
app_secret = 'A619PMEkJu2XFf7z'
callback_url = 'https://127.0.0.1'
token_path = "/home/jack/.schwab/token.json"

c = auth.client_from_token_file(token_path, api_key, app_secret)
if c is None:
    c = auth.client_from_manual_flow(api_key, app_secret, callback_url, token_path)

resp = c.get_account_numbers()
assert resp.status_code == httpx.codes.OK

accounts = resp.json()
for account in accounts:
    if account['accountNumber'] == "13492844":
        account_hash = account['hashValue']

"""
c.place_order(
    account_hash,  # account_id
    equity_buy_limit('NVDA', 1, '121.0')
        .set_duration(Duration.GOOD_TILL_CANCEL)
        .set_session(Session.SEAMLESS)
        .build())
"""
print(dir(c))
from_date = datetime(2024, 9, 24)

resp = c.get_orders_for_account(account_hash, from_entered_datetime = from_date)
print(resp.json())

for order in resp.json():
    print(order['status'])
    if order['status'] == 'PENDING_ACTIVATION':
        print(order['orderId'])
        c.cancel_order(order['orderId'], account_hash)
    print("\n\n")

resp = c.get_market_hours(BaseClient.MarketHours.Market.EQUITY)
print(resp.json())

