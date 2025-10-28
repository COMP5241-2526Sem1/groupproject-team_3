"""
GenAI Service Module
Handles integration with OpenAI GPT-4 for AI-powered features
- Activity generation based on teaching content
- Automatic grouping of student answers
"""

from openai import OpenAI
import logging
import json
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenAIService:
    """
    AI service for generating learning activities and analyzing responses
    Supports both OpenAI API and GitHub Models API
    Uses GPT-4o-mini model
    """
    
    def __init__(self):
        """
        Initialize AI client
        Supports GitHub Models API (using GitHub Personal Access Token)
        and OpenAI API (using OpenAI API key)
        """
        api_key = Config.OPENAI_API_KEY
        
        # Detect if using GitHub PAT (starts with 'github_pat_' or 'ghp_')
        if api_key.startswith('github_pat_') or api_key.startswith('ghp_'):
            # Use GitHub Models API endpoint
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://models.inference.ai.azure.com"
            )
            logger.info("Using GitHub Models API endpoint")
        else:
            # Use standard OpenAI API
            self.client = OpenAI(api_key=api_key)
            logger.info("Using OpenAI API endpoint")
        
        self.model = Config.OPENAI_MODEL
        self.timeout = Config.OPENAI_TIMEOUT
        logger.info(f"GenAI Service initialized with model: {self.model}")
    
    def generate_activity(self, teaching_content, activity_type='short_answer', num_questions=1):
        """
        Generate learning activity based on teaching content
        AI-generated function for creating educational activities
        
        Args:
            teaching_content (str): Teaching topic or keywords
            activity_type (str): Type of activity (poll, short_answer, word_cloud)
            num_questions (int): Number of questions to generate (1-10, only for poll type)
            
        Returns:
            dict: Generated activity with questions and options
        """
        try:
            # Validate num_questions
            num_questions = max(1, min(10, int(num_questions)))
            
            # Construct prompt based on activity type
            prompts = {
                'poll': f"""Create EXACTLY {num_questions} poll question(s) for the topic: {teaching_content}

IMPORTANT: You MUST generate exactly {num_questions} question(s). No more, no less.

For each question, generate:
1. A clear multiple choice question related to the topic
2. Exactly 4 options (labeled A, B, C, D)
3. The correct answer (specify which option: A, B, C, or D)
4. A brief explanation (1-2 sentences) of why that answer is correct

Return the response in valid JSON format:
{{
    "title": "Quiz: [Topic Name]",
    "questions": [
        {{
            "question": "Question text here?",
            "options": [
                {{"label": "A", "text": "First option"}},
                {{"label": "B", "text": "Second option"}},
                {{"label": "C", "text": "Third option"}},
                {{"label": "D", "text": "Fourth option"}}
            ],
            "correct_answer": "A",
            "explanation": "Brief explanation of why option A is correct"
        }},
        ... (repeat for all {num_questions} questions)
    ]
}}

CRITICAL REQUIREMENTS:
- Generate EXACTLY {num_questions} questions in the "questions" array
- Each question MUST have exactly 4 options (A, B, C, D)
- correct_answer MUST be one of: A, B, C, or D
- Make questions challenging but fair for university students
- Ensure proper JSON formatting with correct brackets and commas
- DO NOT add any text outside the JSON structure""",
                
                'short_answer': f"""Create 3 short-answer questions for the topic: {teaching_content}
                
For each question, include:
1. A clear question that tests understanding
2. Key points that should be in a good answer
3. Word limit suggestion (50-200 words)

Return the response in JSON format:
{{
    "questions": [
        {{
            "question": "Question text",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "word_limit": 150
        }}
    ]
}}""",
                
                'word_cloud': f"""Create a word cloud activity for the topic: {teaching_content}
                
Generate:
1. A prompt question that will elicit key terms
2. 5-8 expected keywords related to the topic
3. Instructions for students

Return the response in JSON format:
{{
    "title": "Word Cloud Title",
    "question": "What words come to mind when you think about...",
    "expected_keywords": ["keyword1", "keyword2", "keyword3"],
    "instructions": "Enter single words or short phrases"
}}"""
            }
            
            prompt = prompts.get(activity_type, prompts['short_answer'])
            
            # Calculate appropriate max_tokens based on number of questions
            # Each poll question needs ~150-200 tokens (question + 4 options + explanation)
            # Add buffer for JSON structure
            if activity_type == 'poll':
                base_tokens = 200  # For JSON structure and title
                tokens_per_question = 200  # Per question (question + options + explanation)
                max_tokens = base_tokens + (num_questions * tokens_per_question)
                # Cap at 4000 to stay within model limits
                max_tokens = min(max_tokens, 4000)
            else:
                max_tokens = 1500  # Sufficient for other activity types
            
            # Call OpenAI API
            # Use lower temperature for poll questions to ensure consistent formatting
            temperature = 0.5 if activity_type == 'poll' else 0.7
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator for university lecturers in Hong Kong. Generate high-quality learning activities in English. Always return valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Parse response
            content = response.choices[0].message.content
            logger.info(f"Generated activity for topic: {teaching_content}, num_questions: {num_questions}")
            
            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content)
            result['activity_type'] = activity_type
            result['source_content'] = teaching_content
            
            # Validate poll question count for multi-question polls
            if activity_type == 'poll' and num_questions > 1:
                questions = result.get('questions', [])
                actual_count = len(questions)
                
                if actual_count != num_questions:
                    logger.warning(f"Expected {num_questions} questions but got {actual_count}. Attempting retry...")
                    
                    # If we got fewer questions than expected, this might be due to token limit
                    # Return what we have with a warning
                    if actual_count > 0:
                        logger.info(f"Returning {actual_count} questions instead of {num_questions}")
                        result['note'] = f"Generated {actual_count} questions (requested {num_questions})"
                    else:
                        # If no questions generated, use fallback
                        raise ValueError(f"No questions generated")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}, Content: {content[:200]}...")
            # Return fallback activity on JSON parse error
            return self._get_fallback_activity(activity_type, teaching_content)
        except Exception as e:
            logger.error(f"Error generating activity: {e}")
            # Return fallback activity
            return self._get_fallback_activity(activity_type, teaching_content)
    
    def group_answers(self, answers, question):
        """
        Group student answers based on semantic similarity
        AI-generated function with manual optimization for answer analysis
        
        Args:
            answers (list): List of student answer dictionaries
            question (str): The question being answered
            
        Returns:
            dict: Grouped answers with analysis
        """
        try:
            if not answers:
                return {"groups": [], "analysis": "No answers to analyze"}
            
            # Prepare answers for analysis
            answer_texts = [ans.get('text', '') for ans in answers if ans.get('text')]
            
            if not answer_texts:
                return {"groups": [], "analysis": "No valid answers to analyze"}
            
            prompt = f"""Analyze these student answers to the question: "{question}"

Student Answers:
{json.dumps(answer_texts, indent=2, ensure_ascii=False)}

Group similar answers together based on:
1. Main concepts mentioned
2. Understanding level
3. Common misconceptions

Return the analysis in JSON format:
{{
    "groups": [
        {{
            "group_id": 1,
            "theme": "Brief description of common theme",
            "answer_indices": [0, 2, 5],
            "key_points": ["Main point 1", "Main point 2"],
            "understanding_level": "high/medium/low"
        }}
    ],
    "overall_analysis": "Brief summary of class understanding",
    "common_misconceptions": ["Misconception 1", "Misconception 2"]
}}"""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational analyst. Group and analyze student responses to help teachers understand class comprehension."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            logger.info(f"Grouped {len(answers)} answers into semantic clusters")
            
            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content)
            
            # Add actual answer texts to groups
            for group in result.get('groups', []):
                group['answers'] = [
                    {
                        'index': idx,
                        'text': answer_texts[idx],
                        'student_id': answers[idx].get('student_id', 'Anonymous')
                    }
                    for idx in group['answer_indices']
                    if idx < len(answer_texts)
                ]
            
            return result
            
        except Exception as e:
            logger.error(f"Error grouping answers: {e}")
            # Return simple fallback grouping
            return self._get_fallback_grouping(answers)
    
    def translate_text(self, text, target_language='zh-TW'):
        """
        Translate text to target language using AI
        Optional feature for multi-language support
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code (zh-TW for Traditional Chinese)
            
        Returns:
            str: Translated text
        """
        try:
            language_names = {
                'zh-TW': 'Traditional Chinese (Hong Kong style)',
                'zh-CN': 'Simplified Chinese',
                'en': 'English'
            }
            
            target = language_names.get(target_language, target_language)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following text to {target}."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            translated = response.choices[0].message.content
            logger.info(f"Translated text to {target_language}")
            return translated
            
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return text  # Return original text on error
    
    def evaluate_poll_answer(self, question, options, student_answer, correct_answer):
        """
        Evaluate student's poll answer
        
        Args:
            question (str): The question text
            options (list): List of option dicts with 'label' and 'text'
            student_answer (str): Student's selected option (A, B, C, or D)
            correct_answer (str): The correct option (A, B, C, or D)
            
        Returns:
            dict: Evaluation result with is_correct and feedback
        """
        is_correct = student_answer == correct_answer
        
        return {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'student_answer': student_answer,
            'feedback': 'Correct!' if is_correct else f'Incorrect. The correct answer is {correct_answer}.'
        }
    
    def _get_fallback_activity(self, activity_type, teaching_content):
        """
        Provide fallback activity when API fails
        Manually coded fallback mechanism
        """
        fallback = {
            'poll': {
                'title': f'Poll: {teaching_content}',
                'questions': [
                    {
                        'question': f'What is your current understanding level of {teaching_content}?',
                        'options': [
                            {'label': 'A', 'text': 'Excellent - I understand completely'},
                            {'label': 'B', 'text': 'Good - I understand most concepts'},
                            {'label': 'C', 'text': 'Fair - I need some clarification'},
                            {'label': 'D', 'text': 'Poor - I need more help'}
                        ],
                        'correct_answer': 'B',
                        'explanation': 'This is a self-assessment question.'
                    }
                ],
                'activity_type': 'poll',
                'source_content': teaching_content,
                'note': 'Generated with fallback mechanism'
            },
            'short_answer': {
                'questions': [
                    {
                        'question': f'Explain the main concepts of {teaching_content}',
                        'key_points': ['Key concept 1', 'Key concept 2'],
                        'word_limit': 150
                    }
                ],
                'activity_type': 'short_answer',
                'source_content': teaching_content,
                'note': 'Generated with fallback mechanism'
            },
            'word_cloud': {
                'title': f'Word Cloud: {teaching_content}',
                'question': f'What words describe {teaching_content}?',
                'expected_keywords': [],
                'instructions': 'Enter keywords related to the topic',
                'activity_type': 'word_cloud',
                'source_content': teaching_content,
                'note': 'Generated with fallback mechanism'
            }
        }
        
        return fallback.get(activity_type, fallback['short_answer'])
    
    def _get_fallback_grouping(self, answers):
        """
        Simple fallback grouping when API fails
        Groups all answers into a single group
        """
        return {
            'groups': [
                {
                    'group_id': 1,
                    'theme': 'All responses',
                    'answers': [
                        {
                            'index': i,
                            'text': ans.get('text', ''),
                            'student_id': ans.get('student_id', 'Anonymous')
                        }
                        for i, ans in enumerate(answers)
                    ],
                    'understanding_level': 'mixed'
                }
            ],
            'overall_analysis': 'Automatic grouping unavailable. Manual review recommended.',
            'common_misconceptions': [],
            'note': 'Fallback grouping used'
        }

# Create global GenAI service instance
genai_service = GenAIService()
