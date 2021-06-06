from flask import request, jsonify
from app import app
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

@app.route('/sign_in', methods=['POST'])
def sign_in_user():    
  user = validate_user(sign_in_user_params())
  if user:
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token = access_token, refresh_token = refresh_token)
  else:
    return jsonify({"status": "usuário inválido"}), 401

@app.route('/sign_up', methods=['POST'])
def sign_up():
    user = User(**sign_up_user_params())
    if user.save():
      access_token = create_access_token(identity=user.id)
      refresh_token = create_refresh_token(identity=user.id)
      return jsonify(access_token = access_token, refresh_token = refresh_token)
    else:
      return jsonify({"status": "usuário inválido"}), 404

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

def validate_user(_user):
  try:
    user = User.query.filter_by(email=_user['email']).first()
    if user and user.check_password(_user['password']):
      return user
  except:
    return None

def sign_in_user_params():
  return request.params.require('user').permit('email', 'password')

def sign_up_user_params():
    return request.params.require('user').permit("name", "email", "password", "phone")
