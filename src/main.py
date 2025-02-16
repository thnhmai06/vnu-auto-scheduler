import importlib
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/v<version>/<string:name>', methods=['GET', 'POST'])
def handle_request(version, name):
    try:
        # Xác định handler cho API
        module = importlib.import_module(f'API.v{version}.{name}')
        
        # Lấy tham số từ request
        args = request.args
        argv = request.json if request.method == 'POST' else {}

        # Gọi hàm xử lý request
        return module.handle_request(request, args, argv)
    except ModuleNotFoundError:
        return jsonify({'error': 'API not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)