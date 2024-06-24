from flask import Blueprint, request, jsonify
import src.controllers.transcription as transcription
import src.controllers.extraction as extraction
from flask import Flask, request, jsonify
from flask_cors import cross_origin
import io
from dotenv import load_dotenv
import os
import src.utils.loadData as loadData


bp = Blueprint('api_bp', __name__)



# Middleware pour vérifier la clé d'API
def check_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        authorized_keys = loadData.authorized_keys
        print(authorized_keys)
        if api_key and api_key in authorized_keys:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Clé d\'API invalide'}), 401
    return wrapper


@bp.route('/', methods=['POST'])
@check_api_key
def classify():
    return extraction.extract(request.json['text'])


@bp.route('/transcribe', methods=['POST'])
@cross_origin()
def transcript():
    if 'audio' not in request.files:
        return jsonify({"message": "No audio file part"}), 400
    
    audio_file = request.files['audio']
    file_stream = io.BytesIO(audio_file.read())
    return transcription.transcribe(file_stream)




