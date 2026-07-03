from schwab_api import Schwab
from schwab_api.account_information import Position, Account
import requests

class SchwabExt(Schwab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_account_ids(self):
        """
        Returns the list of all brokerage account ids for the customer.
        """
        self.update_token(token_type='api')
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("schwab-client-ids", "schwab-client-account")}
        r = requests.get("https://ausgateway.schwab.com/api/is.TradeOrderManagementWeb/v1/TradeOrderManagementWebPort/customer/accounts", headers=headers)
        if r.status_code != 200:
            raise ValueError(f"customer/accounts request failed: status {r.status_code}: {r.text[:200]}")
        return [str(a["brokerageAccountId"]) for a in r.json()["brokerageAccounts"]]

    def get_account_info_v2(self):
        """
        Overrides the broken upstream method: Schwab moved the holdings endpoint
        to HoldingV2 with a new response format (~2025). Based on unmerged
        upstream PR itsjafer/schwab-api#77, extended to return ALL accounts:
        HoldingV2 only returns the accounts listed in the Schwab-Client-Ids
        header, so we look up every account id first and pass them all.
        """
        account_info = dict()
        account_ids = self.get_all_account_ids()
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("schwab-client-ids", "schwab-client-account")}
        headers["Schwab-Client-Ids"] = ",".join(account_ids)
        r = requests.get("https://ausgateway.schwab.com/api/is.Holdings/V1/Holdings/HoldingV2", headers=headers)
        if r.status_code != 200:
            raise ValueError(f"HoldingV2 request failed: status {r.status_code}: {r.text[:200]}")
        response = r.json()
        for account in response['accounts']:
            positions = list()
            valid_parse = True
            for security_group in account["groupedPositions"]:
                if security_group["groupName"] == "Cash":
                    continue
                for position in security_group["holdingsRows"]:
                    if "symbol" not in position:
                        valid_parse = False
                        break
                    positions.append(
                        Position(
                            position["symbol"]["symbol"],
                            position["description"],
                            float(position["qty"]["qty"]),
                            0 if "costBasis" not in position else float(position["costBasis"]["cstBasis"]),
                            0 if "marketValue" not in position else float(position["marketValue"]["val"]),
                            position["symbol"]["ssId"]
                        )._as_dict()
                    )
            if not valid_parse:
                continue
            account_info[int(account["accountId"])] = Account(
                account["accountId"],
                positions,
                account["totals"]["marketValue"],
                account["totals"]["cashInvestments"],
                account["totals"]["accountValue"],
                account["totals"].get("costBasis", 0)
            )._as_dict()

        return account_info

    def get_RGL(self, account_id, from_date, to_date, file_path):
        """
        Get the Realized Gain Loss for a specific account
        """
        url = f"https://ausgateway.schwab.com/api/is.RealizedGainLoss/V1/Rgl/export?selectedTimeFrame=Custom&IncludeLots=true&fromDate={from_date}&toDate={to_date}&sortBy=symbol&hasPresto=true"
        # Send a GET request to the URL
        self.headers["Schwab-Client-ids"] = str(account_id)
        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the file to a local directory (you can customize the file name and path)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"File successfully downloaded and saved to {file_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

