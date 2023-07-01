# シーケンス図

``` plantuml
@startuml
title ガーベージトーク システム全体シーケンス
actor user
participant mic
box Rasppbery Pi
  participant Julius
  participant client
  participant lid AS "ゴミ箱蓋(LED)"
end box
actor operator
participant cloud
activate mic
operator -> Julius : 音声認識サーバー起動
activate Julius
operator -> client : 音声認識クライアント起動
activate client
client -\ Julius : socket接続、受信待ち
user -> mic : 手に持っているゴミの名前を喋る
mic -> Julius : 音声データ
Julius -> Julius : 音声認識\n(辞書照合含む)
Julius --> client : 文字変換データ受信
client -> client : 構文解析
client -> lid : 蓋の開閉指示
lid -> lid : 対応する蓋が開く\n(LED点灯)
activate cloud
client -> cloud : ごみデータ送信
alt ごみが一杯
  cloud -> operator : 通知
end
user -> lid : ゴミを捨てる
activate lid
@enduml
```


# 状態遷移図

``` plantuml
@startuml
title ガーベージトーク 状態遷移図

[*] --> 音声入力待ち省電力モード : 電源ON
音声入力待ち省電力モード --> 音声入力待ち省電力モード : ユーザーの音声入力なし
音声入力待ち省電力モード --> 音声処理モード : ユーザーの音声入力あり
音声処理モード --> フタ開モード : 対象のごみだった場合
音声処理モード --> 音声入力待ち省電力モード : 対象のごみでなかった場合
フタ開モード  --> 音声入力待ち省電力モード : フタを開く（LED点灯）
@enduml
```


