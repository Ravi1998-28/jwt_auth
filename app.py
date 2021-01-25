from flask import Flask ,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import jwt as pyJwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///home/ravi/PycharmProjects/secure_api/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50))
    apiKey = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())


@app.route('/generateToken', methods=['POST'])
def generate_token():
    master = request.get_json()['master']
    if not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        user_hash = decoded.get('id', None)
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
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200


@app.route('/apiKey', methods=['POST'])
@jwt_required
def save_api_key():
    data = request.get_json()
    api_key = data['apiKey']
    master = data['master']

    if not api_key:
        return jsonify({'message': 'Api Key is missing'}), 403
    elif not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        username = dict(decoded).get('id', None)

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'token is invalid'}), 403

    new_user = Users(user=username, apiKey=api_key)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
                    "success": "true",
                    "message": "Apikey saved",
                    })


@app.route('/apiKey', methods=['DELETE'])
@jwt_required
def api_key_delete():
    data = request.get_json()
    api_key = data['apiKey']
    master = data['master']
    if not api_key:
        return jsonify({'message': 'Api Key is missing'}), 403
    elif not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(master, options={"verify_signature": False})
        username = dict(decoded).get('id', None)

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'token is invalid'}), 403

    user = Users.query.filter_by(user=username, apiKey=api_key).first()

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
