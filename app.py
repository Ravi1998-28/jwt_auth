from flask import Flask ,jsonify , request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import jwt as pyJwt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.route('/createtoken', methods=['POST'])
def CreateToken():
    master = request.get_json()['master']
    if not master:
        return jsonify({'message': 'Token is missing'}), 403

    try:

        decoded = pyJwt.decode(master, options={"verify_signature": False})
        user_hash = dict(decoded).get('id', None)

    except:
        return jsonify({'message': 'token is invalid'}), 403


    ret = {
        'authToken': create_access_token(identity=user_hash),
        'refreshToken': create_refresh_token(identity=user_hash)
    }
    return jsonify(ret), 200



@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():

    refreshToken = request.get_json()['refreshToken']
    if not refreshToken:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded = pyJwt.decode(refreshToken, options={"verify_signature": False})
        identity = dict(decoded).get('identity', None)
        print('identity', identity)
        ret = {
            'authToken': create_access_token(identity=identity)
        }
        return jsonify(ret), 200
    except:
        return jsonify({'message': 'Refresh token is invalid'}), 401



@app.route('/protected', methods=['POST'])
@jwt_required
def protected():
    authToken = request.get_json()['authToken']
    if not authToken:
        return jsonify({'message': 'Token is missing'}), 403
    try:
        decoded = pyJwt.decode(authToken, options={"verify_signature": False})
        username = dict(decoded).get('identity', None)
        return jsonify(logged_in_as=username), 200
    except:
        return jsonify({'message': 'token is invalid'}), 401

if __name__ == "__main__":
    app.run(debug=True)
