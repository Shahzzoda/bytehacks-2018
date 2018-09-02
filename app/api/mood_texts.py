from app.api import bp
from flask import request, jsonify
from app.models import User, MoodText
from app import db
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six

@bp.route('/mood_texts', methods=['POST'])
def create_text():
    data = request.get_json() or {}
    text = MoodText()
    text.from_dict(data)

    client = language_v1.LanguageServiceClient()
    if isinstance(text.content, six.binary_type):
        text.content = text.content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': text.content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    text.sentiment = round(sentiment.score*255)

    db.session.add(text)
    db.session.commit()

    response = jsonify(text.to_dict())
    response.status_code = 201
    return response
