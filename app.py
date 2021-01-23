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


@app.route('/createtoken', methods=['GET'])
def CreateToken():
    if request.method == 'GET':
        master = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw"
        if not master:
            return jsonify({'message': 'Token is missing'}), 403
        try:

            decoded = pyJwt.decode(master, options={"verify_signature": False})
            user_hash = dict(decoded).get('id', None)

        except:
            return jsonify({'message': 'token is invalid'}), 403

        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        ret = {
            'authToken': create_access_token(identity=user_hash),
            'refreshToken': create_refresh_token(identity=user_hash)
        }
        return jsonify(ret), 200
    else:
        return jsonify({'message': 'The method is not allowed for the requested URL'}), 405



@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    try:
        current_user = get_jwt_identity()
        ret = {
            'authToken': create_access_token(identity=current_user)
        }
        return jsonify(ret), 200
    except:
        return jsonify({'message': 'Refresh token is invalid'}), 401



@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    if request.method == 'GET':
        try:
            username = get_jwt_identity()
            return jsonify(logged_in_as=username), 200
        except:
            return jsonify({'message': 'token is invalid'}), 401

    else:
        return "The method is not allowed for the requested URL", 405


if __name__ == "__main__":
    app.run(debug=True)
