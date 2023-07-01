# -*- coding: utf-8 -*-

# 必要ライブラリ
import socket
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO     
import time                         


GPIO.setmode(GPIO.BCM)              
GPIO.setup(2, GPIO.OUT)             
GPIO.setup(17, GPIO.OUT)             

def led_emitting(GPIO_num):
    for _ in range(3):
        GPIO.output(GPIO_num,  True)
        time.sleep(0.1)
        GPIO.output(GPIO_num, False)
        time.sleep(0.1)        

# アドレス・ポートの設定
host = 'localhost'   # Raspberry PiのIPアドレス
port = 10500         # juliusの待ち受けポート

# パソコンからTCP/IPで自分PCのjuliusサーバに接続
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# ゴミの名前と分類を定義するkey-value辞書
dict ={
    '紙コップ':'燃えるゴミ',
    'バナナの皮':'燃えるゴミ',
    'ティッシュ':'燃えるゴミ',
    '食品トレイ':'燃えるゴミ',
    'お菓子のごみ':'燃えないゴミ'}

#データの読み込み
data = ""
while True:
    # "/RECOGOUT"を受信するまで、一回分の音声データを全部読み込む。
    while data.find("</RECOGOUT>") == -1:
        data += sock.recv(1024).decode('utf-8')

    # 音声データを受取、XMLから必要部分を抽出
    data = data.strip()  # 前後の空白を取り除く
    if "<RECOGOUT>" in data:
        start_idx = data.index("<RECOGOUT>")
        end_idx = data.index("</RECOGOUT>") + len("</RECOGOUT>")
        recogout_data = data[start_idx:end_idx]
        root = ET.fromstring(recogout_data)
        whypos = root.findall('.//WHYPO')
        words = []
        for whypo in whypos:
            word = whypo.attrib['WORD']
            word = ''.join(word)
            if word not in ['[/s]', '[s]']:
                words.append(word)
        # スタブ的に表示
        if words:
            if words[0] == '紙コップ' or words[0] == 'バナナの皮' or words[0] == 'ティッシュ':
                led_emitting(GPIO_num=2)

                print(words)
                print(words[0] + "なので" + dict[words[0]] + "のフタをぱかっと開きます‼\n\n")
                
            elif words[0] == '食品トレイ' or words[0] == 'お菓子のごみ':
                led_emitting(GPIO_num=17)
                
                print(words)
                print(words[0] + "なので" + dict[words[0]] + "のフタをぱかっと開きます‼\n\n")

    data = data[end_idx:]
