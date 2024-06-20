from flask import Blueprint, request, jsonify
import src.controllers.transcription as transcription
import src.controllers.extraction as extraction
from flask import Flask, request, jsonify
from flask_cors import cross_origin


bp = Blueprint('api_bp', __name__)


@bp.route('/', methods=['POST'])
@cross_origin()
def classify():
    return extraction.extract(request.json['text'])


@bp.route('/transcribe', methods=['POST'])
@cross_origin()
def transcript():
    return transcription.transcribe(request.files['audio'])



