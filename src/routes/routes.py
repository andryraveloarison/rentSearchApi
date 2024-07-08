from flask import Blueprint, request, jsonify
import src.controllers.transcription as transcription
import src.controllers.extraction as extraction
from flask import Flask, request, jsonify
from flask_cors import cross_origin
import io
import src.utils.loadData as loadData


bp = Blueprint('api_bp', __name__)

# Middleware pour vérifier la clé d'API
def check_api_key(func):
    def wrapper(*args, **kwargs):

        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')

        authorized_keys = loadData.authorized_keys
        
         # Vérifier si les clés d'API et de secret sont présentes
        if not api_key or not api_secret:
            return jsonify({'error': 'Clé d\'API ou clé secrète manquante'}), 401

        # Vérifier la validité des api_key et api_secret dans une seule condition
        if (api_key in authorized_keys and authorized_keys[api_key] == api_secret) or \
           (api_secret in authorized_keys and authorized_keys[api_secret] == api_key):

            return func(*args, **kwargs)
            
        else:
            return jsonify({'error': 'Clé d\'API ou clé secrète invalide'}), 401


    return wrapper


@bp.route('/', methods=['POST'])
@cross_origin()
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
    return transcription.transcribe(file_stream), 200




