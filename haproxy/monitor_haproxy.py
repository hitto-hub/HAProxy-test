import requests
import subprocess
import time

# バックエンドサーバーとAPIエンドポイント
BACKENDS = [
    {"name": "backend1", "url": "http://backend1:8080/metrics"},
    {"name": "backend2", "url": "http://backend2:8080/metrics"}
]

# HAProxyの設定
SOCKET_PATH = "/tmp/haproxy"
BACKEND_NAME = "servers"

# 重みを計算する関数（例: 負荷が高いほど重みを低くする）
def calculate_weight(cpu_usage):
    max_load = 100
    if cpu_usage < 0 or cpu_usage > max_load:  # 負荷データが異常な場合の処理
        print(f"[WARNING] Invalid CPU usage: {cpu_usage}. Defaulting to weight=50.")
        return 50
    return max(1, int((max_load - cpu_usage) / max_load * 100))

# HAProxyのRuntime APIを使って重みを更新
def update_haproxy_weight(backend, server, weight):
    command = f"echo 'set server {backend}/{server} weight {weight}' | socat {SOCKET_PATH} stdio"
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[INFO] Updated {server} weight to {weight}. Response: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to update weight for {server}: {e}. Output: {e.stderr.strip()}")

# main
def monitor_and_update():
    while True:
        for backend in BACKENDS:
            try:
                # APIから負荷データを取得
                response = requests.get(backend["url"])
                response.raise_for_status()
                metrics = response.json()

                # CPU使用率に基づいて重みを計算
                weight = calculate_weight(metrics["cpu_usage"])
                print(f"[INFO] {backend['name']} CPU: {metrics['cpu_usage']}%, Weight: {weight}")

                # HAProxyに重みを反映
                update_haproxy_weight(BACKEND_NAME, backend["name"], weight)
            except Exception as e:
                print(f"[ERROR] Error monitoring {backend['name']}: {e}")

        # 10秒ごとに更新
        time.sleep(10)

if __name__ == "__main__":
    monitor_and_update()
