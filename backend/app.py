from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import requests
import re
from collections import Counter
import logging

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextExtractor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg']

    def extract_text(self, file_path):
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_ext in ['.png', '.jpg', '.jpeg']:
                return self._extract_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise

    def _extract_from_pdf(self, file_path):
        try:
            text = self._extract_pdf_text(file_path)
            if not text or len(text.strip()) < 50:
                text = self._extract_pdf_ocr(file_path)
            return text
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise

    def _extract_pdf_text(self, file_path):
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {page_num + 1} ---\n{page_text}\n\n"
        except Exception as e:
            logger.warning(f"Direct PDF text extraction failed: {str(e)}")
        return text

    def _extract_pdf_ocr(self, file_path):
        text = ""
        try:
            images = convert_from_path(file_path, dpi=200)
            for i, image in enumerate(images):
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                page_text = pytesseract.image_to_string(image)
                text += f"--- Page {i + 1} ---\n{page_text}\n\n"
        except Exception as e:
            logger.error(f"PDF OCR failed: {str(e)}")
            raise
        return text

    def _extract_from_image(self, file_path):
        try:
            image = Image.open(file_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            return text if text.strip() else "No text could be extracted from this image."
        except Exception as e:
            logger.error(f"Image OCR failed: {str(e)}")
            return f"OCR processing error: {str(e)}"

class AIAnalyzer:
    def __init__(self):
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_TOKEN', '')

    def analyze_text(self, text):
        if len(text.strip()) < 10:
            return self._get_default_analysis()

        try:
            cleaned_text = self._clean_text(text)
            sentiment = self._analyze_sentiment(cleaned_text)
            topics = self._extract_topics(cleaned_text)
            suggestions = self._generate_suggestions(cleaned_text, sentiment, topics)
            engagement_score = self._calculate_engagement_score(cleaned_text, sentiment, topics)
            metrics = self._calculate_text_metrics(cleaned_text)

            return {
                "sentiment": sentiment,
                "key_topics": topics,
                "engagement_score": engagement_score,
                "suggestions": suggestions,
                "readability_score": metrics['readability'],
                "word_count": metrics['word_count'],
                "sentence_count": metrics['sentence_count'],
                "estimated_reading_time": metrics['reading_time']
            }

        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return self._get_fallback_analysis(text)

    def _analyze_sentiment(self, text):
        try:
            if self.huggingface_api_key:
                API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
                headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}

                response = requests.post(API_URL, headers=headers, json=text[:512], timeout=10)

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        sentiments = result[0]
                        top_sentiment = max(sentiments, key=lambda x: x['score'])
                        return {
                            "label": top_sentiment['label'].upper(),
                            "score": round(top_sentiment['score'], 3)
                        }
        except Exception as e:
            logger.warning(f"Sentiment API failed: {str(e)}")

        return self._rule_based_sentiment(text)

    def _rule_based_sentiment(self, text):
        positive_words = {'great', 'excellent', 'amazing', 'wonderful', 'good', 'nice', 'awesome', 'fantastic', 'perfect', 'love', 'like', 'happy', 'joy', 'positive', 'best'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry', 'negative', 'worst', 'problem', 'issue', 'error'}

        words = set(text.lower().split())
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))

        if positive_count > negative_count:
            return {"label": "POSITIVE", "score": 0.7}
        elif negative_count > positive_count:
            return {"label": "NEGATIVE", "score": 0.7}
        else:
            return {"label": "NEUTRAL", "score": 0.5}

    def _extract_topics(self, text):
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }

        words = re.findall(r'\b[a-zA-Z]{3,15}\b', text.lower())
        word_freq = Counter([word for word in words if word not in stop_words])
        topics = [word for word, count in word_freq.most_common(5)]

        return topics

    def _generate_suggestions(self, text, sentiment, topics):
        suggestions = []
        words = text.split()
        word_count = len(words)

        if word_count < 30:
            suggestions.append("Your post is very short. Consider adding more context or details.")
        elif word_count > 400:
            suggestions.append("Your content is quite long. Consider breaking it into a thread or adding subheadings.")

        if '?' not in text:
            suggestions.append("Add a question to encourage comments and discussions.")

        cta_words = {'share', 'comment', 'like', 'follow', 'click', 'learn', 'discover', 'join'}
        if not any(word in text.lower() for word in cta_words):
            suggestions.append("Include a clear call-to-action to guide your audience.")

        if text.count('\n') < 2 and word_count > 100:
            suggestions.append("Break your content into smaller paragraphs for better readability.")

        if topics:
            hashtags = [f"#{topic}" for topic in topics[:3]]
            suggestions.append(f"Consider using relevant hashtags: {', '.join(hashtags)}")

        if sentiment['label'] == 'NEGATIVE':
            suggestions.append("Consider balancing negative content with positive solutions or insights.")

        return suggestions[:5]

    def _calculate_engagement_score(self, text, sentiment, topics):
        score = 50

        if sentiment['label'] == 'POSITIVE':
            score += 10

        word_count = len(text.split())
        if 100 <= word_count <= 250:
            score += 15
        elif 50 <= word_count < 100:
            score += 8

        if '?' in text:
            score += 10

        if topics and len(topics) >= 2:
            score += 5

        if text.count('\n') >= 2:
            score += 5

        return min(max(score, 0), 100)

    def _calculate_text_metrics(self, text):
        words = text.split()
        word_count = len(words)

        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = len(sentences)

        if sentence_count > 0 and word_count > 0:
            avg_sentence_length = word_count / sentence_count
            if avg_sentence_length < 15:
                readability = 85
            elif avg_sentence_length < 20:
                readability = 70
            elif avg_sentence_length < 25:
                readability = 60
            else:
                readability = 45
        else:
            readability = 50

        reading_time = max(1, round(word_count / 200))

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'readability': readability,
            'reading_time': reading_time
        }

    def _clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.!?,;:-]', '', text)
        return text.strip()

    def _get_default_analysis(self):
        return {
            "sentiment": {"label": "NEUTRAL", "score": 0.5},
            "key_topics": [],
            "engagement_score": 0,
            "suggestions": ["Text too short for analysis. Please upload a document with more content."],
            "readability_score": 0,
            "word_count": 0,
            "sentence_count": 0,
            "estimated_reading_time": 0
        }

    def _get_fallback_analysis(self, text):
        cleaned_text = self._clean_text(text)
        metrics = self._calculate_text_metrics(cleaned_text)
        sentiment = self._rule_based_sentiment(cleaned_text)
        topics = self._extract_topics(cleaned_text)

        return {
            "sentiment": sentiment,
            "key_topics": topics,
            "engagement_score": self._calculate_engagement_score(cleaned_text, sentiment, topics),
            "suggestions": self._generate_suggestions(cleaned_text, sentiment, topics),
            "readability_score": metrics['readability'],
            "word_count": metrics['word_count'],
            "sentence_count": metrics['sentence_count'],
            "estimated_reading_time": metrics['reading_time']
        }

# Initialize services
text_extractor = TextExtractor()
ai_analyzer = AIAnalyzer()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'Backend is running',
        'service': 'Social Media Content Analyzer'
    })

# Test analysis route
@app.route('/api/test-analysis', methods=['GET'])
def test_analysis():
    """Test endpoint to check AI analysis without file upload"""
    test_text = "This is a sample social media post about technology and innovation. What do you think about the future of AI? Let's discuss in the comments!"
    
    try:
        analysis_result = ai_analyzer.analyze_text(test_text)
        
        return jsonify({
            'status': 'success',
            'test_text': test_text,
            'data': {
                'analysis': analysis_result
            }
        })
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

# File upload and analysis route
@app.route('/api/upload', methods=['POST'])
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
        if not (file and allowed_file(file.filename)):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, PNG, JPG, JPEG'}), 400
        
        # Validate file size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        
        if file_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'File too large. Maximum size is 10MB'}), 400
        
        if file_length == 0:
            return jsonify({'error': 'File is empty'}), 400
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Extract text
        extracted_text = text_extractor.extract_text(filepath)
        
        # Analyze text with AI
        analysis_result = ai_analyzer.analyze_text(extracted_text)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Warning: Could not delete file {filepath}: {e}")
        
        return jsonify({
            'status': 'success',
            'message': 'File processed and analyzed successfully',
            'data': {
                'original_filename': file.filename,
                'file_size': file_length,
                'extracted_text': extracted_text,
                'analysis': analysis_result
            }
        }), 200
            
    except Exception as e:
        # Clean up on error
        if 'filepath' in locals() and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
                
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 10MB'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Social Media Content Analyzer Server")
    print("📍 http://localhost:5000")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("✅ Health check: http://localhost:5000/api/health")
    print("🧪 Test analysis: http://localhost:5000/api/test-analysis")
    app.run(debug=True, port=5000)