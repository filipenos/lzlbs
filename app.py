from flask import Flask, request, Response, jsonify, g
from flask_mysqldb import MySQL
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
from functools import wraps
import json, re, jwt
from dao import ClientDAO, FavoriteListDAO, WishlistDAO
from models import Client, FavoriteList, Wishlist
from products import ProductService

app = Flask(__name__)

app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "user"
app.config['MYSQL_PASSWORD'] = "user123"
app.config['MYSQL_DB'] = "mglu"
app.config['MYSQL_PORT'] = 3306

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "LZLBS API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

db = MySQL(app)
clientDAO = ClientDAO(db)
favoriteListDAO = FavoriteListDAO(db)
wishlistDAO = WishlistDAO(db)

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_TOKEN_EXPIRE = 60
AUTHORIZED_KEY = '0123456789'


@app.route('/api/auth', methods=['POST'])
def auth():
    app.logger.info('auth request')
    if not request.is_json:
        app.logger.warning('request is no valid json')
        return jsonify({'message': 'only application/json are allowed'}), 400

    try:
        body = request.get_json()
        key = body['key']
    except:
        app.logger.warning('invalid json on request')
        return jsonify({'message': 'invalid data'}), 400
    if key == '':
        app.logger.warning('key is empty')
        return jsonify({'message': 'invalid key'}), 401
    if key != AUTHORIZED_KEY:
        app.logger.warning('key not authorized')
        return jsonify({'message': 'forbidden key'}), 401

    payload = {
        'key': key,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRE)
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM).decode('utf-8')
    app.logger.info('user authorized')
    return jsonify({'Authorization': 'Bearer {}'.format(encoded)})


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bearer = request.headers.get("Authorization")
        if bearer is None or bearer == '':
            return jsonify({'message': 'authorization header is empty'}), 401
        parts = bearer.split(' ')
        if len(parts) != 2:
            return jsonify({'message': 'invalid authorization header'}), 401
        try:
            token = jwt.decode(parts[1], JWT_SECRET, algorithm=JWT_ALGORITHM)
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'message': 'invalid authorization token'}), 401
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token expired'}), 401

        g.key = token.get('key')
        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/clients', methods=['POST'])
@app.route('/api/clients/<int:id>', methods=['PUT'])
@auth_required
def save_client(id=None):
    app.logger.info('save client')
    body = request.json
    client = None

    if request.method == 'POST':
        app.logger.info('creating new client')
        if clientDAO.get_by_email(body['email']) is not None:
            app.logger.warning('email {} alread stored'.format(body['email']))
            return jsonify({'message': 'email already exists'}), 409
        client = Client(body['name'], body['email'])

    elif request.method == 'PUT':
        app.logger.info('updating the client {}'.format(id))
        client = clientDAO.get(id)
        if client is None:
            app.logger.warningf('client {} not found'.format(id))
            return jsonify({'message': 'client not found'}), 404
        if body['email'] != client.email:
            app.logger.info('email changed, search email on server'.format(body['email']))
            if clientDAO.get_by_email(body['email']) is not None:
                app.logger.warning('email alredy saved on server')
                return jsonify({'message': 'email already exists'}), 409
        client.name = body['name']
        client.email = body['email']

    clientDAO.save(client)
    app.logger.info('client saved {}'.format(client.id))
    return jsonify(client.__dict__), 200 if request.method == 'PUT' else 201


@app.route('/api/clients/<int:id>', methods=['GET'])
@auth_required
def get_client(id):
    app.logger.info('get client {}'.format(id))
    client = clientDAO.get(id)
    if client is None:
        app.logger.warning('client not found')
        return jsonify({'message': 'client not found'}), 404
    app.logger.info('client found')
    return jsonify(client.__dict__)


@app.route('/api/clients/<int:id>', methods=['DELETE'])
@auth_required
def del_client(id):
    app.logger.info('delete client {}'.format(id))
    client = clientDAO.get(id)
    if client is None:
        app.logger.warning('client not found')
        return jsonify({'message': 'client not found'}), 404
    clientDAO.delete(client.id)
    app.logger.info('deleted successfully')
    return jsonify({'message': 'ok'})


@app.route('/api/products')
@auth_required
def list_products():
    app.logger.info('list products')
    products = ProductService.list(request.args.get('page'))
    if products is None:
        app.logger.warning('products not found')
        return jsonify({'message': 'products not found'}), 404
    app.logger.info('successfully')
    return products


@app.route('/api/products/<product_id>')
@auth_required
def get_product(product_id=None):
    app.logger.info('get product {}'.format(product_id))
    if not re.match(r"^[\w-]+$", product_id):
        app.logger.warning('invalid product id')
        return jsonify({'message': 'product_id is invalid'}), 400
    product = ProductService.get(product_id)
    if product is None:
        app.logger.warning('product not found')
        return jsonify({'message': 'product not found'}), 404
    app.logger.info('successfully')
    return product


@app.route('/api/wishlist/<int:client_id>', methods=['GET'])
@auth_required
def get_wishlist(client_id):
    app.logger.info('listing wishlist of client {}'.format(client_id))
    if client_id is None:
        app.logger.warning('client_id is empty')
        return jsonify({'message': 'invalid client_id'}), 400

    client = clientDAO.get(client_id)
    if client is None:
        app.logger.warning('client not found')
        return jsonify({'message': 'client not found'}), 404

    wishlist = wishlistDAO.list(client.id)
    json_string = json.dumps([ob.__dict__ for ob in wishlist])
    app.logger.info('successfully')
    return Response(json_string, mimetype='application/json')


@app.route('/api/wishlist/<int:client_id>/<product_id>', methods=['POST'])
@auth_required
def add_to_wishlist(client_id, product_id):
    app.logger.info('add product {} to wishlist of client {}'.format(product_id, client_id))
    client = clientDAO.get(client_id)
    if client is None:
        app.logger.warning('client not found')
        return jsonify({'message': 'client not found'}), 404

    if wishlistDAO.exists(client.id, product_id):
        app.logger.warning('product already exists')
        return jsonify({'message': 'product already added on wishlist'}), 409

    product = ProductService.get(product_id)
    if product is None:
        app.logger.warning('product not found')
        return jsonify({'message': 'product not found'}), 404

    favorite_list = favoriteListDAO.get(client.id)
    if favorite_list is None:
        app.logger.warning('creating favorite list')
        favorite_list = FavoriteList(client.id)
        favoriteListDAO.save(client, favorite_list)

    wishlist = Wishlist(favorite_list.id, product_id)
    wishlistDAO.save(wishlist)
    app.logger.info('successfully to add product on wishlist')
    return jsonify(wishlist.__dict__), 201


@app.errorhandler(404)
def method_not_allowed(e):
    return jsonify({'message': 'resource not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': 'method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
