# ベースイメージ
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    nginx \
    && apt-get clean

# Flaskとpsutilをインストール
RUN pip install flask psutil

# 作業ディレクトリを設定
WORKDIR /app

# Flaskアプリケーションを追加
COPY server.py /app/server.py

# NGINXの設定ファイルを追加
COPY nginx.conf /etc/nginx/nginx.conf

# コンテンツファイルを追加
COPY index.html /var/www/html/index.html

# NGINXとFlaskを起動
CMD ["sh", "-c", "nginx && python /app/server.py"]
