# Simple-Blockchain.com-Data-Webscraper
Developed by @mouryavulupala to grab active BTC account data from blockchain.

----------------------------------------------------------------

## WHAT IT DOES:
This program will simply scrape the blockchain.com explorer and pull data about any accounts that were involved with any transaction (sent or recieved BTC) on the blockchain on the day(s) that you specified. It will push out an ***"addresses.txt"*** containing all of the addresses that were involved/had activity on the day(s) you specified (separated with a "|" so you can plug into blockchain.com REST API) and a CSV file with the title of **"*fromDate*_*toDate*_data.csv"** that will contain data about each one of these collected addresses such as TOTAL_TRANSACTIONS, AMT_OF_PURCHASES, VALUE_OF_PURCHASES (BTC), AMT_OF_SALES, VALUE_OF_SALES (BTC), PROFIT_WITHIN_QUERY_PERIOD.

## WHAT DO YOU HAVE TO CHANGE?
- Within the **btc_algo.py** file, the only value that you would have to change would be the *"dayRangeOfQuery"* to open the query/analysis to more days before the one that you enetered. 

## WAYS TO RUN THE PROGRAM/SCRAPING SCRIPT:
1. **SIMPLE METHOD:** Run the "btc_algo.py" file in your choice of integrated development environment (IDE), text-editing program, or simply through the command prompt (cmd).
   - Using this method, the program requires you to give it **1 argument** after the program statement. That argument must be the **epoch_timestamp_in_milliseconds** of the day you wish to initialize the code with. [*use this site to get a epoch_timestamp_in_ms*](https://www.epochconverter.com/)
   
2. **AESTHETIC/AUTOMATIC METHOD:** Put all of the contents of this repository in one directory together on your computer and run the ***master_runner.bat*** file. This  batch program will take care of the rest.
