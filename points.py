import csv
import sys
from datetime import datetime
from collections import defaultdict

def spend_points(spend, trans_csv):

    trans = [] # Creates a list to allow us to sort by time later and loop through transactions
    balances = {} # Creates an empty dictionary to keep track of individual payers balances

    with open(trans_csv) as file:
        for t in csv.DictReader(file):
            timestamp = datetime.strptime(t['timestamp'], "%Y-%m-%dT%H:%M:%SZ") # Grabs all of the attributes from each row and puts them into variables
            points = int(t['points'])
            payer = t['payer']
            
            trans.append((payer, points, timestamp)) # Creates a list to easily order transactions by time and loop through

            if payer not in balances:
                balances[payer] = 0
            balances[payer] += points # Keeps track of the balances for each payer

    trans.sort(key=lambda x: x[2]) # Sorts the transactions list based on the third element in each index which is time
    balance = sum(balances.values()) # Sums the total balance of the user

    if (spend > balance):
        print("Sorry, you do not have enough points in your balance for this transction.")
        quit()
    
    success = False

    for redeem in trans: # Loops through all of the transactions in the csv until you have spent all the points you wanted to
        if spend == 0: # Breaks and marks as success when spend == 0
            success = True
            break
        
        payer, points, timestamp = redeem # matches up each of the variables to their position in the list index

        if balances[payer] - points < 0: # Makes sure that taking points from this payer won't result in a negative balance
            continue

        payment = min(spend, points) # Takes the min of spend and points make sure we do not overuse points, and use the negative points properly
        spend -= payment # Updates spend to trans for the new points redeemed
        balances[payer] -= payment #Updates the payer's balance to trans for the user redeeming their points

    if success:
        return dict(balances)
    else:
        print("Sorry, went wrong during your payment, please try again.")

if __name__ == '__main__':
    input = sys.argv
    if len(input) < 3:
        print("Please use this format to spend points: 'points.py [amount of points] transactions.csv")
        quit()
    spend = int(sys.argv[1])
    trans_csv = sys.argv[2]
    print(spend_points(spend, trans_csv))