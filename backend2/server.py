from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    # システムの負荷情報を取得
    metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "request_count": 1234  # サンプルデータ
    }
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
