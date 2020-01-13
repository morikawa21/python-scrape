# python-scrape
Python動的スクレイピングAPI

Rest APIとDockerコンテナを使ってブラウザから呼び出す方法とJSONデータをPOSTする方法になります
- 特徴
  - 動的なのでシングルページアプリケーションで作られているページのDOMを読み出す事が可能
  - OGPタグ`og:title` `og:description` `og:img`を取得します
  - `ld+json`タグが有れば テキスト部を抽出します

- 主に使用しているもの
  - flask
  - BeautifulSoup
  - selenium
  - Chromium（headless モード）

- １．Dockerネットワーク作成
```
docker network create -d bridge docker_default
```

- ２．Dockerコンテナ起動
```
docker-compose up -d
```

- ３．コンテナ名 `python-scrape` にはいる
```
docker-compose exec python-scrape bash
```

- ４．アプリケーション起動
  - アプリケーションの実態は `api_scrape.py`
  - `id`、`url`パラメータが渡されると `api_scrape.py`の`scrape`関数を実行
```
python app.py
```

※URLにはhttpからはじまるURLを指定します。

- ４－１．ブラウザからGETmethodで呼び出し

`http://localhost:5050/get?id=12345679&url=URL`

- ４－２．CurlでGETmethodの場合

`curl http://localhost:5050/get?id=12345679\&url=URL`

- ４－３．CurlでPOSTmethodの場合

`curl -X POST -H 'Accept:application/json' -H 'Content-Type:application/json' -d '{"id":123456789,"url":"URL"}' localhost:5050/post`

### ブラウザからシンプルなリクエスト `POSTmethod` を指定してきた場合にCORS対応します
`'Content-Type': 'application/x-www-form-urlencoded'`

### CORS対応
ブラウザ上で異なるドメインのリクエストを要求（クロスドメイン）をしたい場合、通常`JSONP`を使いますが
あらかじめ、リクエストヘッダにOriginフィールドがある場合に、`Access-Control-Allow-Origin`を返却しています。

### 返却データ（順不同）
json
