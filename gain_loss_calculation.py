import csv
from io import StringIO

# The file name of the CSV file
csv_file_name = 'gain_loss.csv'

# A dictionary to hold individual gain/loss for each stock or option
stock_gain_loss = {}

# Read the CSV file
with open(csv_file_name, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)

    # Read each row and store the gain/loss information
    for row in reader:
        try:
            # Extract the stock symbol and Gain/Loss value
            stock_symbol = row[0]
            gain_loss_value = float(row[9].replace('$', '').replace(',', '').replace('(', '-').replace(')', ''))
            
            # Add the gain/loss to the stock's total in the dictionary
            if stock_symbol in stock_gain_loss:
                stock_gain_loss[stock_symbol] += gain_loss_value
            else:
                stock_gain_loss[stock_symbol] = gain_loss_value
        except ValueError:
            # Skip rows with invalid data
            continue

# Initialize a dictionary to store the consolidated gain/loss for each underlying stock
consolidated_gains_losses = {}

# Iterate over the gain/loss records and consolidate them by underlying stock
for symbol, gain_loss in stock_gain_loss.items():
    # Extract the underlying stock symbol (assuming it's the first word in the symbol)
    underlying_symbol = symbol.split()[0]
    
    # Add the gain/loss to the underlying stock's total in the dictionary
    if underlying_symbol in consolidated_gains_losses:
        consolidated_gains_losses[underlying_symbol] += gain_loss
    else:
        consolidated_gains_losses[underlying_symbol] = gain_loss

# Print the consolidated gain/loss for each underlying stock
for stock, total_gain_loss in sorted(consolidated_gains_losses.items()):
    print(f"{stock}: {'gain' if total_gain_loss >= 0 else 'loss'} {abs(total_gain_loss)}")
