from app.api import bp
from flask import request, jsonify
from app.models import User, MoodText
from app import db

@bp.route('/mood_texts', methods=['POST'])
def create_text():
    data = request.get_json() or {}
    text = MoodText()
    text.from_dict(data)
    db.session.add(text)
    db.session.commit()
    response = jsonify(text.to_dict())
    response.status_code = 201
    return jsonify(data)
