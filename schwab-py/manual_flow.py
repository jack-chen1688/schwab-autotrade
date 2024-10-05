from schwab import auth, client
import json
import httpx

api_key = '6SV6Bv1os4eOgpPUc24XdhnzGITHVWEZ'
app_secret = 'A619PMEkJu2XFf7z'
callback_url = 'https://127.0.0.1'
token_path = "/home/jack/.schwab/token.json"

USE_MANUAL_FLOW = True 
c = auth.client_from_token_file(token_path, api_key, app_secret)
if c is None:
    c = auth.client_from_manual_flow(api_key, app_secret, callback_url, token_path)

## using manual flow
#resp = c.get_price_history_every_day('AAPL')
#assert resp.status_code == httpx.codes.OK
#history = resp.json()
#print(history)

resp = c.get_account_numbers()
assert resp.status_code == httpx.codes.OK
print(resp.json())