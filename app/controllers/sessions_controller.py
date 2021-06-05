from flask import request, jsonify
from app import app, datetime
from app.models.session import Session
from app.models.patient import Patient
from flask_jwt_extended import jwt_required, current_user

@app.route('/sessions', methods=['POST'])
@jwt_required()
def new_sessions():
  params = session_params()
  patient = Patient.query.filter_by(id = params['patient_id'], user_id = current_user.id).first()
  if not patient : return invalid_session()
  session = Session(**session_params(), user_id = current_user.id )
  if session.save():
      return jsonify(session = session.serialize(['user','patient']))
  else:
    return invalid_session()

@app.route('/sessions/<int:id>', methods=['GET'])
@jwt_required()
def show_sessions(id):
  session = Session.query.filter_by(id = id, user_id = current_user.id).first()
  if session:
      return jsonify(session = session.serialize(['user','patient']))
  else:
    return invalid_session()

@app.route('/sessions', methods=['PUT'])
@jwt_required()
def edit_sessions():
  params = session_params()
  session = Session.query.filter_by(id = params['id'], user_id = current_user.id).first()
  patient = Patient.query.filter_by(id = params['patient_id'], user_id = current_user.id).first()
  if (not session) or (not patient): return invalid_session() 
  if params['start'] : session.start =  datetime.strptime(params['start'], "%Y-%m-%d %H:%M")
  if params['end'] : session.end = datetime.strptime(params['end'], "%Y-%m-%d %H:%M") 
  session.patient = patient
  if session.save():
      return jsonify(session = session.serialize(['user','patient']))
  else:
    return invalid_session()

def session_params():
  return request.params.require('session').permit("id","start", "end", "patient_id")

def invalid_session():
  return jsonify({"status": "Sessão inválida"}), 404