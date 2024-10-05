from schwab import auth, client
import json

api_key = '6SV6Bv1os4eOgpPUc24XdhnzGITHVWEZ'
app_secret = 'A619PMEkJu2XFf7z'
callback_url = 'https://127.0.0.1:8182/'
token_path = '/path/to/token.json'

c = auth.easy_client(api_key, app_secret, callback_url, token_path)

r = c.get_price_history_every_day('AAPL')
r.raise_for_status()
print(json.dumps(r.json(), indent=4))