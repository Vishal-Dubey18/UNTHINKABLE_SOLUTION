# Social Media Content Analyzer

A powerful web application that analyzes social media content from PDFs and images to provide engagement optimization suggestions. Built with React frontend and Python Flask backend.

## 🚀 Features

### 📁 Document Processing
- **PDF Text Extraction**: Direct text parsing from digital PDFs with formatting preservation
- **Image OCR**: Optical Character Recognition for images and scanned documents using Tesseract
- **Multi-format Support**: PDF, PNG, JPG, JPEG files up to 10MB
- **Multi-page Processing**: Handles documents with multiple pages

### 🤖 AI-Powered Analysis
- **Sentiment Analysis**: Detects positive, negative, or neutral sentiment with confidence scoring
- **Engagement Scoring**: 0-100 score based on content quality and engagement potential
- **Topic Extraction**: Identifies key themes and keywords from content
- **Readability Metrics**: Flesch reading ease score and estimated reading time
- **Content Type Detection**: Automatically categorizes content (Technology, Business, Lifestyle, etc.)

### 💡 Smart Suggestions
- **Content Structure**: Paragraph optimization and formatting recommendations
- **Call-to-Action**: Proven CTAs to increase engagement
- **Hashtag Strategy**: Relevant, categorized hashtags for maximum reach
- **Timing Recommendations**: Best posting times based on content type
- **Emoji Strategy**: When and how to use emojis effectively

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Dropzone** - Drag-and-drop file uploads

### Backend
- **Python Flask** - Lightweight web framework
- **PyPDF2** - PDF text extraction
- **Tesseract OCR** - Optical Character Recognition
- **Pillow** - Image processing
- **Hugging Face API** - AI sentiment analysis
- **Flask-CORS** - Cross-origin resource sharing

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Tesseract OCR installed on system

### 1. Clone the Repository
`ash
git clone https://github.com/Vishal-Dubey18/UNTHINKABLE_SOLUTION.git
cd UNTHINKABLE_SOLUTION
`

### 2. Backend Setup
`ash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Hugging Face API token
`

### 3. Frontend Setup
`ash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
`

### 4. Install System Dependencies

**Windows:**
- Download Poppler from: http://blog.alivate.com.au/poppler-windows/
- Add to system PATH

**Mac:**
`ash
brew install poppler tesseract
`

**Linux (Ubuntu/Debian):**
`ash
sudo apt-get install poppler-utils tesseract-ocr
`

## 🚀 Running the Application

### Start Backend Server
`ash
cd backend
python app.py
`
Backend runs on: http://localhost:5000

### Start Frontend Development Server
`ash
cd frontend
npm run dev
`
Frontend runs on: http://localhost:5173

## 📊 API Endpoints

### GET /api/health
- **Description**: Health check endpoint
- **Response**: Service status and version information

### GET /api/test-analysis
- **Description**: Test analysis without file upload
- **Response**: Sample analysis with demo data

### POST /api/upload
- **Description**: Main file processing endpoint
- **Parameters**: ile (multipart/form-data)
- **Supported Formats**: PDF, PNG, JPG, JPEG
- **Max Size**: 10MB

## 🎯 Usage Guide

### 1. File Upload
- **Drag & Drop**: Drag files directly onto the upload area
- **File Picker**: Click 
Choose
File
Manually to browse files
- **Supported Files**: PDF documents, PNG/JPG images with text

### 2. Analysis Results
After upload, you'll receive:

#### Engagement Metrics
- **Engagement Score**: 0-100 based on content quality
- **Sentiment Analysis**: Emotional tone with confidence percentage
- **Readability Score**: Content complexity assessment
- **Estimated Reading Time**: Time to read the content

#### Content Insights
- **Key Topics**: Main themes extracted from the content
- **Content Type**: Automatic categorization (Tech, Business, etc.)
- **Word & Sentence Count**: Basic content metrics

#### Optimization Suggestions
- **Content Structure**: Paragraph breaks, length optimization
- **Engagement Boosters**: Questions, CTAs, emoji usage
- **Hashtag Strategy**: Relevant hashtags for your content type
- **Posting Timing**: Best times to share your content

### 3. Best Practices for Files

#### ✅ Recommended:
- High-contrast images with clear text
- Digital PDFs with selectable text
- Screenshots of web content
- Scanned documents with printed text
- Files under 10MB size

#### ❌ Avoid:
- Handwritten text
- Blurry or low-quality images
- Complex backgrounds
- Very small font sizes
- Password-protected PDFs

## 🔧 Configuration

### Environment Variables
Create a .env file in the backend directory:

`nv
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
FLASK_ENV=development
`

### Getting Hugging Face API Token
1. Visit [Hugging Face](https://huggingface.co)
2. Create a free account
3. Go to Settings → Access Tokens
4. Create a new token with Write permissions
5. Add the token to your .env file

## 🏗️ Project Structure

`
social-media-analyzer/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                  # Environment variables
│   └── uploads/              # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FileUpload.jsx # Main upload component
│   │   ├── App.jsx           # Root component
│   │   └── main.jsx          # Application entry point
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
└── README.md
`

## 🧪 Testing

### Backend Testing
`ash
cd backend
python app.py
# Test endpoints:
curl http://localhost:5000/api/health
curl http://localhost:5000/api/test-analysis
`

### Frontend Testing
`ash
cd frontend
npm run dev
# Visit http://localhost:5173
`

### File Testing
Test with various file types:
- Text-based PDFs
- Image-based PDFs
- Screenshots with text
- Document photos
- Social media post images

## 🚀 Deployment

### Backend Deployment Options
- **Railway**: 
ailway deploy
- **Heroku**: git push heroku main
- **PythonAnywhere**: Upload via dashboard
- **AWS Elastic Beanstalk**: b deploy

### Frontend Deployment Options
- **Vercel**: ercel --prod
- **Netlify**: 
etlify deploy --prod
- **GitHub Pages**: 
pm run build && gh-pages -d dist

### Environment Setup for Production
`nv
FLASK_ENV=production
HUGGINGFACE_API_TOKEN=your_production_token
`

## 🔍 Troubleshooting

### Common Issues

#### Unable
to
get
page
count.
Is
poppler
installed
and
in
PATH?
- **Solution**: Install Poppler utilities for your operating system
- **Windows**: Download from official site and add to PATH
- **Mac**: rew install poppler
- **Linux**: sudo apt-get install poppler-utils

#### No
text
could
be
extracted
from
this
image
- **Cause**: Poor image quality or handwritten text
- **Solution**: Use clearer images with printed text

#### Processing
failed Errors
- **Check**: File size (max 10MB) and format (PDF, PNG, JPG, JPEG)
- **Verify**: Backend server is running on port 5000

#### CORS Errors
- **Solution**: Ensure Flask-CORS is properly configured in backend

### Performance Optimization
- Use compressed images for faster uploads
- Keep PDFs under 10 pages for quick processing
- Ensure good internet connection for file uploads

## 📈 Performance Metrics

- **File Processing**: 5-30 seconds depending on file size and complexity
- **Text Extraction**: PDFs: 2-10s, Images: 5-20s
- **AI Analysis**: 2-5 seconds per document
- **Maximum File Size**: 10MB
- **Supported Languages**: English (primary)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: git checkout -b feature/amazing-feature
3. Commit changes: git commit -m 'Add amazing feature'
4. Push to branch: git push origin feature/amazing-feature
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write meaningful commit messages
- Test all file types before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tesseract OCR** for text extraction capabilities
- **Hugging Face** for AI model inference
- **React & Flask** communities for excellent documentation
- **Tailwind CSS** for beautiful, responsive design

## 📞 Support

For support and questions:
- Create an [Issue](https://github.com/Vishal-Dubey18/UNTHINKABLE_SOLUTION/issues)
- Email: vdubey8511@gmail.com
- Documentation: [GitHub Wiki](https://github.com/Vishal-Dubey18/UNTHINKABLE_SOLUTION/wiki)

## 🎯 Future Enhancements

- [ ] Multi-language support for text extraction
- [ ] Advanced AI models for better suggestions
- [ ] Batch file processing
- [ ] Social media platform-specific recommendations
- [ ] Historical analysis and trends
- [ ] User accounts and saved analyses
- [ ] API rate limiting and authentication
- [ ] Mobile app version

---

**Built with ❤️ by Vishal Dubey**

