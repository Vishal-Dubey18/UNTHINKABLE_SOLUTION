import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const FileUpload = () => {
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        accept: {
            'application/pdf': ['.pdf'],
            'image/*': ['.png', '.jpg', '.jpeg']
        },
        maxSize: 10 * 1024 * 1024, // 10MB
        multiple: false,
        onDrop: async (acceptedFiles) => {
            if (acceptedFiles.length > 0) {
                await handleFileUpload(acceptedFiles[0]);
            }
        }
    });

    const handleFileUpload = async (file) => {
        setUploading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 30000, // 30 second timeout
            });

            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    const handleFileInput = (event) => {
        const file = event.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
        // Reset the input
        event.target.value = '';
    };

    const getScoreColor = (score) => {
        if (score >= 70) return 'bg-green-500';
        if (score >= 50) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    const getSentimentColor = (sentiment) => {
        switch(sentiment) {
            case 'POSITIVE': return 'text-green-600';
            case 'NEGATIVE': return 'text-red-600';
            default: return 'text-gray-600';
        }
    };

    const cleanDisplayText = (text) => {
        if (!text) return "No text content found.";
        
        // Remove excessive line breaks and clean up OCR artifacts
        let cleaned = text
            .replace(/(\r\n|\r|\n){3,}/g, '\n\n') // Reduce multiple line breaks
            .replace(/[^\S\r\n]+/g, ' ') // Normalize spaces
            .replace(/[|\\{}()[\]^$+*?.]/g, '') // Remove some special characters
            .trim();
        
        // If text is too short or seems like OCR garbage, show message
        if (cleaned.length < 20 || cleaned.split(' ').length < 5) {
            return "Limited text extracted. This might be due to:\n• Low image quality\n• Handwritten text\n• Complex background\n• Small font size\n\nTry uploading a clearer document with printed text.";
        }
        
        return cleaned;
    };

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Social Media Content Analyzer
                    </h1>
                    <p className="text-gray-600">
                        Upload PDF or image files to extract and analyze text for better engagement
                    </p>
                </div>

                {/* Help Section */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <div className="flex items-start">
                        <svg className="h-5 w-5 text-blue-400 mt-0.5 mr-2 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        <div>
                            <h3 className="text-sm font-medium text-blue-800">What files work best?</h3>
                            <div className="mt-1 text-sm text-blue-700">
                                <ul className="list-disc list-inside space-y-1">
                                    <li><strong>PDFs:</strong> Reports, articles, documents with clear text</li>
                                    <li><strong>Images:</strong> Screenshots, scanned documents, signs with printed text</li>
                                    <li><strong>Best results:</strong> High contrast, clear fonts, good lighting</li>
                                    <li><strong>Avoid:</strong> Handwriting, blurry images, complex backgrounds</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Upload Area */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
                    <div className="p-8">
                        <div
                            {...getRootProps()}
                            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                                isDragActive
                                    ? 'border-indigo-500 bg-indigo-50'
                                    : 'border-gray-300 hover:border-indigo-400'
                            } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            <input {...getInputProps()} />
                            
                            {uploading ? (
                                <div className="space-y-4">
                                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                                    <p className="text-gray-600">Processing your file...</p>
                                    <p className="text-xs text-gray-500">Extracting text and analyzing content...</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    <div>
                                        <p className="text-lg font-medium text-gray-900">
                                            {isDragActive ? 'Drop the file here' : 'Drag & drop your file here'}
                                        </p>
                                        <p className="text-gray-500 mt-1">or</p>
                                    </div>
                                    <p className="text-xs text-gray-500">
                                        PDF, PNG, JPG up to 10MB
                                    </p>
                                </div>
                            )}
                        </div>
                        
                        {/* Separate File Input Button */}
                        {!uploading && (
                            <div className="mt-4 text-center">
                                <label className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer">
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                    </svg>
                                    Choose File Manually
                                    <input
                                        type="file"
                                        className="sr-only"
                                        onChange={handleFileInput}
                                        accept=".pdf,.png,.jpg,.jpeg"
                                    />
                                </label>
                            </div>
                        )}
                    </div>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-red-800">Error</h3>
                                <p className="text-sm text-red-700 mt-1">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Results Display */}
                {result && (
                    <div className="bg-white rounded-xl shadow-md overflow-hidden">
                        <div className="p-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-6">Analysis Results</h2>
                            
                            {/* Success Message */}
                            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                                <div className="flex">
                                    <div className="flex-shrink-0">
                                        <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                        </svg>
                                    </div>
                                    <div className="ml-3">
                                        <p className="text-sm font-medium text-green-800">{result.message}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Engagement Score */}
                            <div className="mb-6">
                                <div className="flex justify-between items-center mb-2">
                                    <h3 className="text-lg font-semibold text-gray-900">Engagement Score</h3>
                                    <span className="text-2xl font-bold text-gray-900">
                                        {result.data.analysis.engagement_score}/100
                                    </span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                                    <div 
                                        className={`h-4 rounded-full transition-all duration-1000 ${getScoreColor(result.data.analysis.engagement_score)}`}
                                        style={{ width: `${result.data.analysis.engagement_score}%` }}
                                    ></div>
                                </div>
                                <p className="text-sm text-gray-600">
                                    {result.data.analysis.engagement_score >= 70 ? 'Excellent engagement potential!' :
                                     result.data.analysis.engagement_score >= 50 ? 'Good engagement potential' :
                                     'Needs improvement for better engagement'}
                                </p>
                            </div>

                            {/* Metrics Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                {/* Sentiment Analysis */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Sentiment Analysis</h3>
                                    <div className="flex items-center">
                                        <span className={`text-lg font-medium ${getSentimentColor(result.data.analysis.sentiment.label)}`}>
                                            {result.data.analysis.sentiment.label}
                                        </span>
                                        <span className="text-gray-500 ml-2 text-sm">
                                            ({(result.data.analysis.sentiment.score * 100).toFixed(1)}% confidence)
                                        </span>
                                    </div>
                                    {result.data.analysis.sentiment.source && (
                                        <p className="text-xs text-gray-500 mt-1">
                                            Source: {result.data.analysis.sentiment.source}
                                        </p>
                                    )}
                                </div>

                                {/* Readability Score */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Readability Score</h3>
                                    <div className="flex items-center justify-between">
                                        <span className="text-lg font-medium text-gray-900">
                                            {result.data.analysis.readability_score}/100
                                        </span>
                                        <span className="text-sm text-gray-500">
                                            {result.data.analysis.estimated_reading_time} min read
                                        </span>
                                    </div>
                                    <p className="text-xs text-gray-500 mt-1">
                                        {result.data.analysis.readability_score >= 70 ? 'Easy to read' :
                                         result.data.analysis.readability_score >= 50 ? 'Moderate difficulty' :
                                         'Difficult to read'}
                                    </p>
                                </div>
                            </div>

                            {/* Content Type */}
                            {result.data.analysis.content_type && result.data.analysis.content_type !== 'general' && (
                                <div className="mb-6">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Content Type</h3>
                                    <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 capitalize">
                                        {result.data.analysis.content_type}
                                    </div>
                                </div>
                            )}

                            {/* Key Topics */}
                            {result.data.analysis.key_topics && result.data.analysis.key_topics.length > 0 && (
                                <div className="mb-6">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Key Topics</h3>
                                    <div className="flex flex-wrap gap-2">
                                        {result.data.analysis.key_topics.map((topic, index) => (
                                            <span 
                                                key={index}
                                                className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800"
                                            >
                                                {topic}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Hashtag Strategy */}
                            {result.data.analysis.hashtag_strategy && result.data.analysis.hashtag_strategy.hashtags.length > 0 && (
                                <div className="mb-6">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Hashtag Strategy</h3>
                                    <div className="bg-blue-50 rounded-lg p-4">
                                        <div className="flex flex-wrap gap-2 mb-3">
                                            {result.data.analysis.hashtag_strategy.hashtags.map((hashtag, index) => (
                                                <span 
                                                    key={index}
                                                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                                                >
                                                    {hashtag}
                                                </span>
                                            ))}
                                        </div>
                                        <p className="text-sm text-blue-700">
                                            {result.data.analysis.hashtag_strategy.strategy}
                                        </p>
                                    </div>
                                </div>
                            )}

                            {/* Suggestions */}
                            <div className="mb-6">
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">Improvement Suggestions</h3>
                                <ul className="space-y-3">
                                    {result.data.analysis.suggestions.map((suggestion, index) => (
                                        <li key={index} className="flex items-start">
                                            <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                            </svg>
                                            <span className="text-gray-700">{suggestion}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            {/* Extracted Text */}
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">Extracted Content</h3>
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-700 mb-4">
                                        <div>
                                            <strong>📁 File:</strong> {result.data.original_filename}
                                        </div>
                                        <div>
                                            <strong>📊 Type:</strong> {result.data.original_filename.split('.').pop().toUpperCase()}
                                        </div>
                                        <div>
                                            <strong>🔤 Words:</strong> {result.data.analysis.word_count}
                                        </div>
                                        <div>
                                            <strong>📝 Sentences:</strong> {result.data.analysis.sentence_count}
                                        </div>
                                        <div>
                                            <strong>⏱️ Read Time:</strong> {result.data.analysis.estimated_reading_time} min
                                        </div>
                                        <div>
                                            <strong>⭐ Readability:</strong> {result.data.analysis.readability_score}/100
                                        </div>
                                    </div>
                                    
                                    <div className="bg-white p-4 rounded border">
                                        <h4 className="font-semibold text-gray-800 mb-2">📋 Extracted Text:</h4>
                                        {result.data.extracted_text && result.data.extracted_text !== "No text could be extracted from this image." ? (
                                            <pre className="whitespace-pre-wrap text-sm text-gray-700 max-h-60 overflow-y-auto leading-relaxed">
                                                {cleanDisplayText(result.data.extracted_text)}
                                            </pre>
                                        ) : (
                                            <div className="text-center py-8 text-gray-500">
                                                <svg className="mx-auto h-12 w-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                                <p>No readable text could be extracted from this file.</p>
                                                <p className="text-sm mt-1">Try uploading a clearer image or a text-based PDF.</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Upload Another File Button */}
                            <div className="mt-6 text-center">
                                <button
                                    onClick={() => {
                                        setResult(null);
                                        setError(null);
                                    }}
                                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                >
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                    </svg>
                                    Upload Another File
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default FileUpload;