#!/usr/bin/env python3

# Google SpreadSheet Upload Test
# Pleas install `gspread` and `oauth2client` before runnning.
#  -> $ pip3 install gspread
#  -> $ pip3 install google-auth

import datetime
import gspread
import json
JSON_KEY_NAME = 'sse06-k01-group3-22e158bf23d7.json'
SPREADSHEET_KEY = "10Y0HR7GheCM4zg23Cxq_TkGvJpp0yrMm7bv4hZ4LIh8"

from google.oauth2.service_account import Credentials
# お決まりの文句
# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = Credentials.from_service_account_file(JSON_KEY_NAME, scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログイン。
gc = gspread.authorize(credentials)

# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)
worksheet = workbook.worksheet('trash')

# Date:
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
date = now.strftime('%Y/%m/%d %H:%M:%S')

# Call:
# call = '紙コップ'
call = '食品トレイ'

# Result:
result = 'Open'

# []で囲み2次元リストにしないとエラーになる
add_data = [[date, call, result]]
workbook.values_append(worksheet.title, {"valueInputOption": "USER_ENTERED"}, {"values": add_data})

print("Add new record.")