import functools
from flask import Flask, request, jsonify
from thsauto import ThsAuto
import time
import sys
import threading

import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 定义一个自定义的 JSON 编码器
class ORJSONEncoder:
    @staticmethod
    def default(obj):
        # 可以根据需要添加自定义的序列化逻辑
        return str(obj)

    @classmethod
    def encode(cls, obj):
        return orjson.dumps(obj, default=cls.default).decode('utf-8')

# 替换 Flask 的 JSON 编码器
app.json_encoder = ORJSONEncoder

auto = ThsAuto()

client_path = None
def run_client():
    os.system('start ' + client_path)
    

lock = threading.Lock()
next_time = 0
interval = 0.5

VALID_TOKEN = "DSTdqw3Poq1mBzjY8OEUv6Zjl1JAHYoc"
def validate_token():
    token = request.headers.get('Authorization')
    if token and token == f"Bearer {VALID_TOKEN}":
        return True
    return False

def require_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not validate_token():
            return jsonify({"code":1, "status": "unauthorized", "msg": "invalid or missing token"}), 401
        return func(*args, **kwargs)
    return wrapper

def interval_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global interval
        global lock
        global next_time
        lock.acquire()
        now = time.time()
        if now < next_time:
            time.sleep(next_time - now)
        try:
            rt = func(*args, **kwargs)
        except Exception as e:
            rt = ({'code': 1, 'status': 'failed', 'msg': '{}'.format(e)}, 400)
        next_time = time.time() + interval
        lock.release()
        return rt
    return wrapper

@app.route('/balance', methods = ['GET'])
@interval_call
@require_token
def get_balance():
    auto.active_mian_window()
    result = auto.get_balance()
    return jsonify(result), 200

@app.route('/position', methods = ['GET'])
@interval_call
@require_token
def get_position():
    auto.active_mian_window()
    result = auto.get_position()
    return jsonify(result), 200

@app.route('/success_orders', methods = ['GET'])
@interval_call
@require_token
def get_active_orders():
    auto.active_mian_window()
    result = auto.get_active_orders()
    return jsonify(result), 200

@app.route('/filled_orders', methods = ['GET'])
@interval_call
@require_token
def get_filled_orders():
    auto.active_mian_window()
    result = auto.get_filled_orders()
    return jsonify(result), 200

@app.route('/sell', methods = ['GET'])
@interval_call
@require_token
def sell():
    auto.active_mian_window()
    stock = request.args['stock_no']
    amount = request.args['amount']
    price = request.args.get('price', None)
    if price is not None:
        price = float(price)
    result = auto.sell(stock_no=stock, amount=int(amount), price=price)
    return jsonify(result), 200

@app.route('/buy', methods = ['GET'])
@interval_call
@require_token
def buy():
    auto.active_mian_window()
    stock = request.args['stock_no']
    amount = request.args['amount']
    price = request.args.get('price', None)
    if price is not None:
        price = float(price)
    result = auto.buy(stock_no=stock, amount=int(amount), price=price)
    return jsonify(result), 200

@app.route('/buy/kc', methods = ['GET'])
@interval_call
@require_token
def buy_kc():
    auto.active_mian_window()
    stock = request.args['stock_no']
    amount = request.args['amount']
    price = request.args.get('price', None)
    if price is not None:
        price = float(price)
    result = auto.buy_kc(stock_no=stock, amount=int(amount), price=price)
    return jsonify(result), 200

@app.route('/sell/kc', methods = ['GET'])
@interval_call
@require_token
def sell_kc():
    auto.active_mian_window()
    stock = request.args['stock_no']
    amount = request.args['amount']
    price = request.args.get('price', None)
    if price is not None:
        price = float(price)
    result = auto.sell_kc(stock_no=stock, amount=int(amount), price=price)
    return jsonify(result), 200

@app.route('/cancel_entrust', methods = ['GET'])
@interval_call
@require_token
def cancel():
    auto.active_mian_window()
    entrust_no = request.args['entrust_no']
    result = auto.cancel(entrust_no=entrust_no)
    return jsonify(result), 200

@app.route('/client_exit', methods = ['GET'])
@interval_call
@require_token
def kill_client():
    auto.active_mian_window()
    auto.kill_client()
    return jsonify({'code': 0, 'status': 'succeed'}), 200


@app.route('/client_restart', methods = ['GET'])
@interval_call
@require_token
def restart_client():
    auto.active_mian_window()
    auto.kill_client()
    run_client()
    time.sleep(5)
    auto.bind_client()
    if auto.hwnd_main is None:
        return jsonify({'code': 1, 'status': 'failed'}), 200
    else:
        return jsonify({'code': 0, 'status': 'succeed'}), 200


@app.route('/thsauto/test', methods = ['GET'])
@interval_call
@require_token
def test():
    auto.active_mian_window()
    auto.test()
    return jsonify({}), 200


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    if len(sys.argv) > 3:
        client_path = sys.argv[3]
    auto.bind_client()
    if auto.hwnd_main is None and client_path is not None:
        restart_client()
    app.run(host=host, port=port)