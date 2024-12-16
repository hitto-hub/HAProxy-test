FROM ubuntu:latest

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    haproxy \
    python3 \
    python3-venv \
    socat \
    && apt-get clean

RUN python3 -m venv /venv

RUN /venv/bin/pip install requests

# HAProxy設定ファイルをコピー
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Pythonスクリプトをコピー
COPY monitor_haproxy.py /monitor_haproxy.py

# 仮想環境をアクティベートして実行
CMD ["sh", "-c", "haproxy -f /usr/local/etc/haproxy/haproxy.cfg & /venv/bin/python /monitor_haproxy.py"]
