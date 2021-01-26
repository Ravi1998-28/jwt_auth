from flask import Flask ,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import jwt as pyJwt
from functools import wraps

app = Flask(__name__)

# use your path for db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/ravi/PycharmProjects/secure_api/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50))
    apiKey = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())


"""Giving access by auth Token as well  by api key using this custom_access function """
def custom_access(f):
   @wraps(f)
   def decorator(*args, **kwargs):
      token = None
      api_key = None

      if 'Authorisation' in request.headers:
         token = request.headers['Authorisation']

      if 'x-api-key' in request.headers:
          api_key = request.headers['x-api-key']

      try:
          # finding current user
         if token and api_key:

             decoded = pyJwt.decode(token, options={"verify_signature": False})
             user_hash = decoded.get('id', None)
             if user_hash is None:
                 user_hash = decoded.get('identity', None)

             current_user = Users.query.filter_by(user=user_hash, apiKey=api_key ).first()

         elif token and api_key is None:

             decoded = pyJwt.decode(token, options={"verify_signature": False})
             user_hash = decoded.get('id', None)
             if user_hash is None:
                 user_hash = decoded.get('identity', None)

             current_user = Users.query.filter_by(user=user_hash).first()

         elif api_key and token is None:
             current_user = Users.query.filter_by(apiKey=api_key).first()

         else:
             return jsonify({'message': 'Not authorised'}), 401

      except Exception as ex:
         print(ex)
         return jsonify({'message': 'Token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator


@app.route('/generateToken', methods=['POST'])
def generate_token():
    """ Generating AuthToken and RefreshToken.
    ---
    POST:
        summary: generateToken endpoint.
        description: Get the authToken and refreshToken by master Token.
        parameters:
            - master: master Token
              type: String
              required: true
        responses:
            200:
                description: ruthToken and refreshToken to be returned.
            403:
                description: Token is missing.
    """
    master = request.get_json()['master']
    if not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        user_hash = decoded.get('id', None)
        if user_hash is None:
            user_hash = decoded.get('identity', None)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Token is invalid'}), 403
    ret = {
        'authToken': create_access_token(identity=user_hash),
        'refreshToken': create_refresh_token(identity=user_hash)
    }
    return jsonify(ret), 200


@app.route('/refreshToken', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    """ Generating Refresh authToken by RefreshToken.
    ---
    POST:
        summary: refreshToken endpoint.
        description: Get a authToken with the refreshToken.
        parameters:
            - Bearer Token: refreshToken
              type: String
              required: true
        responses:
            200:
                description: Refreshed authToken to be returned.
            403:
                description: Token is invalid.
    """
    try:
        current_user = get_jwt_identity()
        ret = {
            'authToken': create_access_token(identity=current_user)
        }
        return jsonify(ret), 200
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Token is invalid'}), 403


@app.route('/protected', methods=['POST'])
@custom_access
def protected(current_user):
    """ Protecting this endpoint by authToken and api key.
    ---
    POST:
        summary: protected endpoint.
        description: Get the  User_hash with the authToken and api key , passing into headers.

        parameters:
            - authToken: authToken
              apiKey:api_key
              type: String
              required: true
        responses:
            200:
                description: User_hash to be returned.
            403:
                description: Token is invalid.
    """
    try:
        return jsonify(logged_in_as=current_user.user), 200
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Token is invalid'}), 403


@app.route('/apiKey', methods=['POST'])
@jwt_required
def save_api_key():
    """ Saving Api key and user_hash using Users model.
    ---
    POST:
        summary: apiKey endpoint.
        description: id, Api key, user and created_at saved into Users model .
        parameters:
            - Bearer Token: authToken
              master: master Token
              api_key: apiKey
              type: String
              required: true
        responses:
            200:
                description: user_hash and api key saved  to be returned.
            403:
                description: Token is invalid.
    """
    data = request.get_json()
    api_key = data['apiKey']
    master = data['master']

    if not api_key:
        return jsonify({'message': 'Api Key is missing'}), 403
    elif not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        user_hash = decoded.get('id', None)
        if user_hash is None:
            user_hash = decoded.get('identity', None)

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Token is invalid'}), 403

    if user_hash is None:
        return "Please give a valid Token"
    else:
        """
        user = Users.query.filter_by(user=user_hash, apiKey=api_key).first()
        
        if user is not None:
            if user.user == user_hash and user.apiKey == api_key:
                return jsonify({'message': 'user already exist'})
            elif user.apiKey == api_key:
                return jsonify({'message': 'Api key should be unique exist'})
        else:
        """
        new_user = Users(user=user_hash, apiKey=api_key)
        db.session.add(new_user)
        db.session.commit()

    return jsonify({
                    "success": "true",
                    "message": "Apikey saved",
                    })


@app.route('/apiKey', methods=['DELETE'])
@jwt_required
def api_key_delete():
    """ Deleting Api key.
    ---
    DELETE:
        summary: apiKey endpoint.
        description: Deleting apiKey.
        parameters:
            - Bearer Token: authToken
              master: master Token
              api_key: apiKey
              type: String
              required: true
        responses:
            200:
                description: Api key Deleted to be returned.
            403:
                description: Token is invalid.
    """
    data = request.get_json()
    api_key = data['apiKey']
    master = data['master']
    if not api_key:
        return jsonify({'message': 'Api Key is missing'}), 403
    elif not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        user_hash = decoded.get('id', None)
        if user_hash is None:
            user_hash = decoded.get('identity', None)

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Token is invalid'}), 403

    user = Users.query.filter_by(user=user_hash, apiKey=api_key).first()

    if not user:
        return jsonify({'message': 'user does not exist'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({
                    "success": "true",
                    "message": "Apikey removed"
                    })


if __name__ == "__main__":
    app.run(debug=True)
