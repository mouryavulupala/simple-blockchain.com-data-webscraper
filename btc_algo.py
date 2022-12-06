# python -u "PATH/TO/btc_algo.py" epoch_timestamp
import urllib
from urllib.request import urlopen  # import urllib library
import csv
import json  # json library
import time  # used for the epoch time
import sys  # used for system arguments

# int(time.time()/10000)*10000  # this is current day in milliseconds --> adjust
start_day = int(sys.argv[1])
# how many days (before and including the starting day) you would like to include
dayRangeOfQuery = 2

# output dictionary to be converted to JSON
result_dict = {}
outputFile = open("addresses.txt", "a")

# FETCH ALL ADDRESSES ON "currentDay_epoch" (and dayRangeOfQuery-1 days before) THAT SENT ANYTHING
for x in range(dayRangeOfQuery):
    # the epoch of the "x" day before current (i.e. 0 day before current TO 30 days before current)
    day = start_day - (x*86400000)
    print("Date:\t" + time.strftime("%m/%d/%Y", time.localtime(day/1000)))

    allBlockData_URL = ("https://blockchain.info/blocks/" +
                        str(day) + "?format=json")
    allBlockData_response = urlopen(allBlockData_URL)
    allBlockData_JSON = json.loads(allBlockData_response.read())

    for block in allBlockData_JSON:
        # hash of an individual block in ALL of the block data
        blockHash = block['hash']

        blockData_URL = "https://blockchain.info/rawblock/" + blockHash
        blockData_response = urlopen(blockData_URL)
        blockData_JSON = json.loads(blockData_response.read())

        print("PROCESSING BLOCK [" + str(allBlockData_JSON.index(block)+1) + "/" + str(len(allBlockData_JSON)) +
              "] of " + time.strftime("%m/%d/%Y", time.localtime(day/1000)) + " .. containing " + str(len(blockData_JSON['tx'])) + " transactions")

        for transaction in blockData_JSON['tx']:
            print("progress:\t[" + str(blockData_JSON['tx'].index(transaction)
                                       ) + "/" + str(len(blockData_JSON['tx'])) + "]", end='\r')

            # hash of an individual transaction in blockData
            transactionHash = transaction['hash']

            txData_URL = "https://blockchain.info/rawtx/" + transactionHash
            txData_response = urlopen(txData_URL)
            txData_JSON = json.loads(txData_response.read())

            sender_addresses = []
            sender_purchase_amt = []
            for i in range(len(txData_JSON["inputs"])):
                sender_addresses.append(txData_JSON["inputs"][i]["prev_out"].get(
                    "addr"))
                sender_purchase_amt.append(txData_JSON["inputs"][i]["prev_out"].get(
                    "value")/100000000)

            receiver_addresses = []
            receiver_sale_amt = []
            for i in range(len(txData_JSON["out"])):
                receiver_addresses.append(txData_JSON["out"][i].get("addr"))
                receiver_sale_amt.append(
                    txData_JSON["out"][i].get("value")/100000000)

            for sender_address in sender_addresses:
                # if there is an address present
                if sender_address is not None and sender_address not in result_dict.keys():
                    # print(sender_address)

                    # total_tx, amt of purchases, btc value of purchases, amt of sales, btc val of sales, profit of within month trades
                    result_dict[sender_address] = [1, 1, sender_purchase_amt[sender_addresses.index(
                        sender_address)], 0, 0, -sender_purchase_amt[sender_addresses.index(sender_address)]]

                    # formatting to be used to call the api once again with the "multi address" call
                    outputFile.write(sender_address + "|")

                elif sender_address is not None and sender_address in result_dict.keys():
                    result_dict[sender_address] = [result_dict[sender_address][0]+1, result_dict[sender_address][1]+1, result_dict[sender_address][2]+sender_purchase_amt[sender_addresses.index(
                        sender_address)], result_dict[sender_address][3], result_dict[sender_address][4], result_dict[sender_address][5]-sender_purchase_amt[sender_addresses.index(sender_address)]]

            for receiver_address in receiver_addresses:
                # if there is an address present
                if receiver_address is not None and receiver_address not in result_dict.keys():
                    # print(receiver_address)

                    # total_tx, amt of purchases, btc value of purchases, amt of sales, btc val of sales, profit of within month trades
                    result_dict[receiver_address] = [1, 0, 0, 1, receiver_sale_amt[receiver_addresses.index(
                        receiver_address)], receiver_sale_amt[receiver_addresses.index(receiver_address)]]

                    # formatting to be used to call the api once again with the "multi address" call
                    outputFile.write(receiver_address + "|")

                elif receiver_address is not None and receiver_address in result_dict.keys():
                    result_dict[receiver_address] = [result_dict[receiver_address][0]+1, result_dict[receiver_address][1], result_dict[receiver_address][2], result_dict[receiver_address][3]+1, result_dict[receiver_address][4]+receiver_sale_amt[receiver_addresses.index(
                        receiver_address)], result_dict[receiver_address][5]+receiver_sale_amt[receiver_addresses.index(receiver_address)]]


print("job complete...")

outputFile.close()
print("pushed to txt file..")

# Finally, push the data out to the CSV file
with open((time.strftime("%m.%d.%Y", time.localtime((start_day - ((dayRangeOfQuery-1)*86400000))/1000)))+"-"+time.strftime("%m.%d.%Y", time.localtime(start_day/1000)) + '_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Address', 'Amt of Transactions', 'Amt of Purchases',
                  'Total Val. of Purchases (BTC)', 'Amt of Sales', 'Total Val. of Sales (BTC)', 'Profit within Query Range']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for address in result_dict:
        writer.writerow(
            {
                'Address': address,
                'Amt of Transactions': result_dict.get(address)[0],
                'Amt of Purchases': result_dict.get(address)[1],
                'Total Val. of Purchases (BTC)': result_dict.get(address)[2],
                'Amt of Sales': result_dict.get(address)[3],
                'Total Val. of Sales (BTC)': result_dict.get(address)[4],
                'Profit within Query Range': result_dict.get(address)[5],
            }
        )

print("pushed to csv file..")
