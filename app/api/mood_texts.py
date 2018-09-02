from app.api import bp
from flask import request, jsonify
from app.models import User, MoodText
from app import db
from datetime import datetime
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
import os
from google.oauth2 import service_account
import json

@bp.route('/mood_texts', methods=['POST'])
def create_text():
    data = request.get_json() or {}
    text = MoodText()
    text.from_dict(data)

    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    client = language_v1.LanguageServiceClient(credentials=credentials)
    if isinstance(text.content, six.binary_type):
        text.content = text.content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': text.content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    text.sentiment = round(sentiment.score*255)
    text.date = datetime.now()

    db.session.add(text)
    db.session.commit()

    response = jsonify(text.to_dict())
    response.status_code = 201
    return response
