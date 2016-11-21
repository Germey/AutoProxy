from flask import request, Flask, Response
import config
from functools import wraps


def check_auth(username, password):
    if config.NEED_AUTH:
        return username == config.AUTH_USER and password == config.AUTH_PASSWORD
    else:
        return True


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


app = Flask(__name__)


@app.route('/record/<key>', methods=['GET'])
def record(key):
    if key == config.KEY:
        ip = request.remote_addr
        with open('ip', 'w') as f:
            f.write(ip)
            f.close()
        return ip + '\n'
    else:
        return 'Invalid Key'


@app.route('/', methods=['GET'])
@requires_auth
def proxy():
    with open('ip', 'r') as f:
        ip = f.read().strip()
        f.close()
        if ip:
            return ip + ':' + str(config.PORT)
    return '0'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
