from schwab_api import Schwab
import requests

class SchwabExt(Schwab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_RGL(self, account_id, file_path):
        """
        Get the Realized Gain Loss for a specific account
        """
        url = "https://ausgateway.schwab.com/api/is.RealizedGainLoss/V1/Rgl/export?selectedTimeFrame=Custom&IncludeLots=true&fromDate=01/01/2022&toDate=10/05/2024&sortBy=symbol&hasPresto=true"
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

