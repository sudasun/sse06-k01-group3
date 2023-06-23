# K01-Group3「スマートごみ箱」向け Julius環境セットアップ手順

## 参考資料

- [Raspberry PiとJuliusで特定の単語を認識させる | パソコン工房 NEXMAG](https://www.pc-koubou.jp/magazine/19743)
  - 上記記載と一部手順が異なる点は本資料を参照

## 実行環境

- Raspberry Pi 3
  - K04 のmicroSDカードで起動
``` sh
    pi@raspi4-sse:~ $ uname -a
    Linux raspi4-sse 5.15.84-v7l+ #1613 SMP Thu Jan 5 12:01:26 GMT 2023 armv7l GNU/Linux  
```

## セットアップ手順で参考資料と異なる点（ひとまず差分だけ記載）

- Julius本体はv4.6でも良い
  ``` sh
  $ wget https://github.com/julius-speech/julius/archive/v4.6.tar.gz
  ``` 

- Juliusのコンパイルコマンドは以下のように`--build=aarch64-unknown-linux`を付与する。
  ```sh
  $ ./configure --with-mictype=alsa --build=aarch64-unknown-linux
  ```

- テスト音声認識実行した際、`Warning: strip: sample xxx-xxx has zero value, stripped`が出続ける現象が発生する場合は、`-nostrip` をつけて実行する
  ``` sh
  $ julius -C main.jconf -C am-gmm.jconf -demo -nostrip
  ```

---

## 辞書ファイル登録手順

大まかな手順は以下の通り。
1. 「読み」ファイル作成  - (trash.yomi)
2. 「音素」ファイル作成 - (trash.phone)
3. 「構文」ファイル作成 - (trash.grammar)
4. 「語彙」ファイル作成 - (trash.voca)
5.  辞書ファイル生成実行 - (trash.dfa)


### 1. 「読み」ファイル作成  — (trash.yomi)
``` sh
pi@raspi4-sse:~/julius-4.6/dict $ vi trash.yomi
```
以下のように書き込みして保存。名称と読みの間は半角スペースで区切る。

**trash.yomi**
```
食品トレイ しょくひんとれい
紙コップ かみこっぷ
```

### 2. 「音素」ファイル作成 — (trash.phone)
`yomi2voca.pl`を使って .yomi ファイルから .phone ファイルを生成
``` sh
pi@raspi4-sse:~/julius-4.6/dict $ ~/julius-4.6/gramtools/yomi2voca/yomi2voca.pl ~/julius-4.6/dict/trash.yomi > ~/julius-4.6/dict/trash.phone
```
以下のような内容のファイルが作成される

**trash.phone**
```
食品トレイ	sh o k u h i N t o r e i
紙コップ	k a m i k o q p u
```

### 3. 「構文」ファイル作成 — (trash.grammar)

``` sh
pi@raspi4-sse:~/julius-4.6/dict $ vi trash.grammar
```
以下のように書き込みして保存。
TRASH : xxxxxx の部分は、`trash.phone` の 音素のアルファベットを大文字で入力すること！

**trash.grammar**
```
S : NS_B TRASH NS_E
TRASH : SHOKUHINTOREI
TRASH : KAMIKOQPU
```

### 4. 「語彙」ファイル作成 — (trash.voca)

``` sh
# .phoneファイルをベースにすると作成しやすいのでコピーしてから編集する
pi@raspi4-sse:~/julius-4.6/dict $ cp trash.phone trash.voca
pi@raspi4-sse:~/julius-4.6/dict $ vi trash.voca
```

以下のように書き込みして保存。
- `% SHOKUHINTOREI` の部分は、`trash.grammar` の `TRASH : SHOKUHINTOREI` の右側の内容と同一
- .phoneファイル は作成したときに 名称と 音素の区切りが**タブ**になっているので、本ファイルでは**半角スペースに置き換えが必要**
- 最後の4行は固定文
```
% SHOKUHINTOREI 
食品トレイ sh o k u h i N t o r e i
% KAMIKOQPU
紙コップ k a m i k o q p u
% NS_Btrash.phone
[s] silB
% NS_E
[/s] silE
```

### 5.  辞書ファイル生成実行

- `mkdfa.pl` を実行して辞書ファイルを生成
- 引数で各ファイルの共通のファイル名を指定(ここでは `~/julius-4.6/dict/trash`)
``` sh
pi@raspi4-sse:~/julius-4.6/gramtools/mkdfa $ mkdfa.pl ~/julius-4.6/dict/trash
```

生成後、なぜかdfaファイルができていないので、dfatmpからコピーする
``` sh
pi@raspi4-sse:~/julius-4.6 $ cp ~/julius-4.6/dict/trash.dfatmp ~/julius-4.6/dict/trash.dfa
```

## 辞書ファイルを指定した実行

- 辞書ファイルに `~/julius-4.6/dict/trash` を指定して実行しています。
``` sh
pi@raspi4-sse:~/julius-4.6 $ ~/julius-4.6/julius/julius -C ~/julius-4.6/julius-kit/dictation-kit-4.5/am-gmm.jconf -nostrip -gram ~/julius-4.6/dict/trash -input mic
```

以上
