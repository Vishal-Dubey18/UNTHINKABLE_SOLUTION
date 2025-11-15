import os
import requests
import re
import random
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self):
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_TOKEN', '')
        
        # Enhanced dictionaries for better analysis
        self.engagement_boosters = {
            'questions': [
                "What are your thoughts on this?",
                "Has anyone else experienced this?",
                "What would you do differently?",
                "Which option would you choose?",
                "What's your biggest challenge with this?"
            ],
            'cta_phrases': [
                "Share your experience in the comments!",
                "Tag someone who needs to see this!",
                "Save this for later reference!",
                "Double-tap if you agree!",
                "Share to your story if this resonates!"
            ],
            'emojis': ['🔥', '💡', '🚀', '👏', '💯', '⭐', '🎯', '✨', '🙌', '📈'],
        }

        # Comprehensive sentiment words database
        self.sentiment_words = {
            'positive': {
                'strong': ['love', 'amazing', 'excellent', 'fantastic', 'perfect', 'brilliant', 'outstanding', 'wonderful', 'awesome', 'fabulous'],
                'medium': ['good', 'great', 'nice', 'happy', 'pleased', 'satisfied', 'delighted', 'joy', 'exciting', 'beautiful'],
                'weak': ['like', 'okay', 'fine', 'decent', 'acceptable', 'pleasant', 'comfortable', 'nice', 'cool']
            },
            'negative': {
                'strong': ['hate', 'terrible', 'awful', 'horrible', 'disgusting', 'hateful', 'disastrous', 'miserable', 'tragic', 'devastating'],
                'medium': ['bad', 'sad', 'angry', 'upset', 'disappointed', 'frustrated', 'annoyed', 'problem', 'issue', 'difficult'],
                'weak': ['dislike', 'unhappy', 'concerned', 'worried', 'bother', 'trouble', 'challenge', 'hard']
            }
        }

        # Comprehensive hashtag database by category
        self.hashtag_database = {
            'technology': [
                'Tech', 'Innovation', 'Digital', 'Future', 'AI', 'TechNews', 'Technology', 
                'Software', 'Programming', 'Coding', 'Developer', 'IT', 'DigitalTransformation',
                'TechTips', 'Computer', 'Internet', 'WebDevelopment', 'DataScience'
            ],
            'business': [
                'Entrepreneur', 'Startup', 'BusinessTips', 'Leadership', 'Success', 'Marketing',
                'Sales', 'Finance', 'Money', 'Career', 'Work', 'Office', 'Professional',
                'BusinessStrategy', 'Management', 'Productivity', 'SuccessTips'
            ],
            'lifestyle': [
                'LifeHacks', 'Productivity', 'SelfCare', 'Motivation', 'Growth', 'Health',
                'Fitness', 'Wellness', 'Travel', 'Food', 'Home', 'Family', 'Relationships',
                'Inspiration', 'Happiness', 'Mindfulness', 'PersonalDevelopment'
            ],
            'creative': [
                'Creativity', 'Design', 'Inspiration', 'Art', 'Ideas', 'Photography',
                'Music', 'Writing', 'ContentCreation', 'GraphicDesign', 'Creative',
                'Artist', 'DigitalArt', 'Illustration', 'CreativeProcess'
            ],
            'education': [
                'Learning', 'Knowledge', 'Tips', 'HowTo', 'Education', 'Study',
                'Students', 'Teacher', 'OnlineLearning', 'Skills', 'Tutorial',
                'KnowledgeShare', 'Educational', 'StudyTips'
            ],
            'general': [
                'Tips', 'Advice', 'Help', 'Support', 'Community', 'Daily',
                'Life', 'Update', 'News', 'Info', 'Fact', 'Learn'
            ]
        }

    def analyze_text(self, text):
        """Enhanced text analysis with accurate sentiment and relevant hashtags"""
        if len(text.strip()) < 10:
            return self._get_default_analysis()
        
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Get accurate sentiment analysis
            sentiment = self._accurate_sentiment_analysis(cleaned_text)
            
            # Extract meaningful topics
            topics = self._meaningful_topic_extraction(cleaned_text)
            
            # Generate expert-level suggestions
            suggestions = self._expert_suggestions(cleaned_text, sentiment, topics)
            
            # Calculate engagement score
            engagement_score = self._enhanced_engagement_score(cleaned_text, sentiment, topics)
            
            # Calculate metrics
            metrics = self._calculate_text_metrics(cleaned_text)
            
            # Generate relevant hashtag strategy
            hashtag_strategy = self._relevant_hashtag_strategy(topics, cleaned_text, sentiment)
            
            # Detect content type
            content_type = self._detect_content_type(cleaned_text)
            
            return {
                "sentiment": sentiment,
                "key_topics": topics,
                "engagement_score": engagement_score,
                "suggestions": suggestions,
                "hashtag_strategy": hashtag_strategy,
                "readability_score": metrics['readability'],
                "word_count": metrics['word_count'],
                "sentence_count": metrics['sentence_count'],
                "estimated_reading_time": metrics['reading_time'],
                "content_type": content_type
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return self._get_fallback_analysis(text)

    def _accurate_sentiment_analysis(self, text):
        """Highly accurate sentiment analysis using multiple methods"""
        text_lower = text.lower()
        
        # Method 1: Try Hugging Face API first
        api_sentiment = self._try_huggingface_sentiment(text)
        if api_sentiment and api_sentiment['score'] > 0.7:
            return api_sentiment
        
        # Method 2: Advanced rule-based sentiment with scoring
        return self._advanced_rule_based_sentiment(text_lower)

    def _try_huggingface_sentiment(self, text):
        """Try Hugging Face API for sentiment"""
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
                            "score": round(top_sentiment['score'], 3),
                            "source": "ai_model"
                        }
        except Exception as e:
            logger.warning(f"Hugging Face API failed: {str(e)}")
        
        return None

    def _advanced_rule_based_sentiment(self, text_lower):
        """Advanced rule-based sentiment analysis with better accuracy"""
        positive_score = 0
        negative_score = 0
        
        words = text_lower.split()
        
        # Count sentiment words with weights
        for word in words:
            # Strong positive words
            if word in self.sentiment_words['positive']['strong']:
                positive_score += 3
            # Medium positive words
            elif word in self.sentiment_words['positive']['medium']:
                positive_score += 2
            # Weak positive words
            elif word in self.sentiment_words['positive']['weak']:
                positive_score += 1
            
            # Strong negative words
            if word in self.sentiment_words['negative']['strong']:
                negative_score += 3
            # Medium negative words
            elif word in self.sentiment_words['negative']['medium']:
                negative_score += 2
            # Weak negative words
            elif word in self.sentiment_words['negative']['weak']:
                negative_score += 1
        
        # Analyze sentence structures for better accuracy
        sentences = re.split(r'[.!?]+', text_lower)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check for negation patterns
            if any(negation in sentence for negation in ['not happy', "don't like", "doesn't work", "isn't good", "no good"]):
                negative_score += 2
            
            # Check for positive emphasis
            if any(emphasis in sentence for emphasis in ['very happy', 'so good', 'really love', 'extremely pleased']):
                positive_score += 2
        
        # Calculate final sentiment
        total_score = positive_score + negative_score
        if total_score == 0:
            return {"label": "NEUTRAL", "score": 0.5, "source": "rule_based"}
        
        positive_ratio = positive_score / total_score
        
        if positive_ratio > 0.6:
            confidence = min(positive_ratio, 0.95)
            return {"label": "POSITIVE", "score": round(confidence, 3), "source": "rule_based"}
        elif positive_ratio < 0.4:
            confidence = min((1 - positive_ratio), 0.95)
            return {"label": "NEGATIVE", "score": round(confidence, 3), "source": "rule_based"}
        else:
            # Calculate neutrality confidence
            neutrality = 1 - abs(positive_ratio - 0.5) * 2
            return {"label": "NEUTRAL", "score": round(max(neutrality, 0.5), 3), "source": "rule_based"}

    def _meaningful_topic_extraction(self, text):
        """Extract meaningful and relevant topics"""
        text_lower = text.lower()
        
        # Enhanced stop words
        enhanced_stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'about', 'very', 'really', 'just', 'like', 'more', 'some', 'such', 'only',
            'also', 'than', 'then', 'when', 'where', 'why', 'how', 'what', 'which',
            'who', 'whom', 'their', 'there', 'here', 'from', 'into', 'upon', 'your',
            'my', 'our', 'its', 'him', 'her', 'them', 'would', 'should', 'could'
        }
        
        # Extract meaningful words (nouns, adjectives)
        words = re.findall(r'\b[a-zA-Z]{3,15}\b', text_lower)
        meaningful_words = [word for word in words if word not in enhanced_stop_words]
        
        # Create bigrams for better topic detection
        bigrams = []
        for i in range(len(meaningful_words) - 1):
            bigram = f"{meaningful_words[i]} {meaningful_words[i+1]}"
            # Filter out meaningless bigrams
            if not any(stop in bigram.split() for stop in enhanced_stop_words):
                bigrams.append(bigram)
        
        # Combine and count frequency
        all_terms = meaningful_words + bigrams
        term_freq = Counter(all_terms)
        
        # Get most relevant topics (appear at least twice or are meaningful)
        topics = []
        for term, count in term_freq.most_common(10):
            if count >= 2 or len(term) > 6:  # Prefer longer, more meaningful terms
                # Capitalize first letter for better presentation
                formatted_topic = ' '.join(word.capitalize() for word in term.split())
                topics.append(formatted_topic)
        
        return topics[:5] if topics else ["General", "Content"]

    def _relevant_hashtag_strategy(self, topics, text, sentiment):
        """Generate highly relevant hashtags based on content"""
        if not topics:
            return {"hashtags": ["#SocialMedia", "#Content", "#Engagement"], "strategy": "General hashtags for broad reach"}
        
        content_type = self._detect_content_type(text)
        relevant_hashtags = []
        
        # 1. Add topic-based hashtags
        for topic in topics[:3]:
            hashtag = '#' + topic.replace(' ', '')
            relevant_hashtags.append(hashtag)
        
        # 2. Add category-specific hashtags
        if content_type in self.hashtag_database:
            category_tags = random.sample(self.hashtag_database[content_type], 3)
            relevant_hashtags.extend(['#' + tag for tag in category_tags])
        
        # 3. Add sentiment-based hashtags
        if sentiment['label'] == 'POSITIVE':
            relevant_hashtags.extend(['#PositiveVibes', '#GoodNews', '#Happy'])
        elif sentiment['label'] == 'NEGATIVE':
            relevant_hashtags.extend(['#RealTalk', '#HonestThoughts', '#Discussion'])
        else:
            relevant_hashtags.extend(['#Thoughts', '#Perspective', '#Insights'])
        
        # 4. Add engagement hashtags
        relevant_hashtags.extend(['#SocialMediaTips', '#ContentCreation', '#DigitalMarketing'])
        
        # Remove duplicates and limit to 8 most relevant
        unique_hashtags = list(dict.fromkeys(relevant_hashtags))[:8]
        
        return {
            "hashtags": unique_hashtags,
            "strategy": f"Mix of topic-specific, {content_type} category, and engagement hashtags for optimal reach",
            "content_type": content_type
        }

    def _expert_suggestions(self, text, sentiment, topics):
        """Generate expert-level suggestions"""
        suggestions = []
        words = text.split()
        word_count = len(words)
        
        # Content length optimization
        if word_count < 50:
            suggestions.append("📝 **Expand your content**: Add more details, examples, or personal stories to provide value (ideal: 80-250 words)")
        elif word_count > 400:
            suggestions.append("🧵 **Create a thread**: Break long content into multiple posts for better readability and engagement")
        
        # Engagement elements
        if '?' not in text:
            suggestions.append("💬 **Ask a question**: Questions can increase comments by 2x. Try: 'What's your experience with this?'")
        
        # Sentiment-specific suggestions
        if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.7:
            suggestions.append("🎉 **Leverage positivity**: Share success stories or achievements - positive content gets more shares")
        elif sentiment['label'] == 'NEGATIVE':
            suggestions.append("🤝 **Add solutions**: Balance criticism with constructive solutions or alternative approaches")
        
        return suggestions[:4]

    def _detect_content_type(self, text):
        """Accurate content type detection"""
        text_lower = text.lower()
        
        category_scores = {
            'technology': len(re.findall(r'\b(tech|software|code|programming|ai|digital|computer|data|app|website)\b', text_lower)),
            'business': len(re.findall(r'\b(business|startup|entrepreneur|marketing|sales|money|career|work|office)\b', text_lower)),
            'lifestyle': len(re.findall(r'\b(life|health|fitness|travel|food|home|family|relationship|wellness)\b', text_lower)),
            'creative': len(re.findall(r'\b(design|art|creative|photo|video|music|write|content|inspiration)\b', text_lower)),
            'education': len(re.findall(r'\b(learn|education|study|tips|howto|guide|tutorial|knowledge|skill)\b', text_lower))
        }
        
        # Return category with highest score, or general if no clear winner
        best_category = max(category_scores, key=category_scores.get)
        return best_category if category_scores[best_category] > 0 else 'general'

    def _enhanced_engagement_score(self, text, sentiment, topics):
        """Calculate engagement score"""
        score = 50
        
        words = text.split()
        word_count = len(words)
        
        # Optimal content length
        if 80 <= word_count <= 250:
            score += 20
        
        # Engagement elements
        if '?' in text:
            score += 15
        
        # Good sentiment (positive or balanced negative)
        if sentiment['label'] == 'POSITIVE':
            score += 10
        elif sentiment['label'] == 'NEGATIVE' and sentiment['score'] < 0.8:
            score += 5  # Balanced criticism can also engage
        
        return min(score, 100)

    def _calculate_text_metrics(self, text):
        """Calculate text metrics"""
        words = text.split()
        word_count = len(words)
        
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = len(sentences)
        
        # Readability score
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
        """Clean text"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _get_default_analysis(self):
        return {
            "sentiment": {"label": "NEUTRAL", "score": 0.5, "source": "default"},
            "key_topics": ["Content", "SocialMedia"],
            "engagement_score": 50,
            "suggestions": ["Add more content for detailed analysis and suggestions"],
            "hashtag_strategy": {"hashtags": ["#SocialMedia", "#Content", "#Tips"], "strategy": "Add more content for specific hashtag recommendations"},
            "readability_score": 50,
            "word_count": 0,
            "sentence_count": 0,
            "estimated_reading_time": 0,
            "content_type": "general"
        }

    def _get_fallback_analysis(self, text):
        cleaned_text = self._clean_text(text)
        metrics = self._calculate_text_metrics(cleaned_text)
        sentiment = self._advanced_rule_based_sentiment(cleaned_text.lower())
        topics = self._meaningful_topic_extraction(cleaned_text)
        
        return {
            "sentiment": sentiment,
            "key_topics": topics,
            "engagement_score": self._enhanced_engagement_score(cleaned_text, sentiment, topics),
            "suggestions": self._expert_suggestions(cleaned_text, sentiment, topics),
            "hashtag_strategy": self._relevant_hashtag_strategy(topics, cleaned_text, sentiment),
            "readability_score": metrics['readability'],
            "word_count": metrics['word_count'],
            "sentence_count": metrics['sentence_count'],
            "estimated_reading_time": metrics['reading_time'],
            "content_type": self._detect_content_type(cleaned_text)
        }import os
