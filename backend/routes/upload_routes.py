from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from app.services.text_extraction import TextExtractionService

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    return filename.rsplit('.', 1)[1].lower()

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if file and allowed_file(file.filename):
            # Secure filename and save
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            
            # Extract text based on file type
            file_type = get_file_type(filename)
            extraction_result = TextExtractionService.extract_text(filepath, file_type)
            
            if 'error' in extraction_result:
                return jsonify({
                    'status': 'error',
                    'message': 'File uploaded but text extraction failed',
                    'filename': filename,
                    'error': extraction_result['error']
                }), 200
            
            return jsonify({
                'status': 'success',
                'message': 'File uploaded and processed successfully',
                'filename': filename,
                'file_type': file_type,
                'extraction_method': extraction_result.get('method', 'unknown'),
                'extracted_text': extraction_result.get('text', ''),
                'text_length': len(extraction_result.get('text', ''))
            }), 200
        else:
            allowed_types = ', '.join(ALLOWED_EXTENSIONS)
            return jsonify({
                'error': f'Invalid file type. Allowed types: {allowed_types}'
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Backend is working!'})