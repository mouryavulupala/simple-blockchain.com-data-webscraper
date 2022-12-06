%ECHO off
COLOR 02
TITLE BTC Data Algorithm (by: mourya vulupala)
CLS

type title_art.txt
echo.
echo.
SET /p input=Enter time_in_milliseconds for program to analyze:	
echo.
echo running...
echo.

python -u ".\btc_algo.py" %input%