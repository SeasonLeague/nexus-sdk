# File: nexus/__init__.py
import requests
from typing import List, Dict, Union, Optional
import os
from .exceptions import (
    NexusError, 
    NexusAPIError, 
    NexusFileError, 
    NexusValidationError,
    NexusConfigError
)

class NexusSDK:
    """
    SDK for interacting with the Nexus Question Generation API.
    
    Args:
        api_key (str): Your Gemini API key
        base_url (str, optional): The base URL for the API. Defaults to the production URL.
    """
    
    SUPPORTED_FILE_TYPES = {
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff'
    }
    
    def __init__(self, api_key: str = None, base_url: str = "https://hackathon-nexus.onrender.com"):
        self.api_key = api_key or os.getenv('NEXUS_API_KEY')
        if not self.api_key:
            raise NexusConfigError("API key must be provided either as an argument or through NEXUS_API_KEY environment variable")
        self.base_url = base_url.rstrip('/')
        
    def _validate_files(self, files: List[str]) -> None:
        """Validate files before uploading."""
        if not files:
            raise NexusValidationError("No files provided")
        
        for file_path in files:
            if not os.path.exists(file_path):
                raise NexusFileError(f"File not found: {file_path}")
                
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension not in self.SUPPORTED_FILE_TYPES:
                raise NexusFileError(
                    f"Unsupported file type: {file_extension}. "
                    f"Supported types are: {', '.join(self.SUPPORTED_FILE_TYPES.keys())}"
                )

    def generate_questions(self, 
                          files: List[str], 
                          num_questions: int, 
                          difficulty: str) -> Dict:
        """
        Generate questions from uploaded files.
        
        Args:
            files (List[str]): List of file paths to upload
            num_questions (int): Number of questions to generate
            difficulty (str): Difficulty level of questions ('easy', 'medium', 'hard')
            
        Returns:
            Dict: JSON response containing:
                - preview: A summary of the uploaded content
                - questions: List of dictionaries, each containing:
                    - question: The question text
                    - difficulty: The difficulty level
                    - correctAnswer: The correct answer
                    
        Raises:
            NexusFileError: If there are issues with the provided files
            NexusValidationError: If the input parameters are invalid
            NexusAPIError: If the API request fails
            NexusError: For other unexpected errors
        """
        try:
            # Validate input parameters
            if not isinstance(num_questions, int) or num_questions <= 0:
                raise NexusValidationError("num_questions must be a positive integer")
                
            if difficulty not in ['easy', 'medium', 'hard']:
                raise NexusValidationError("difficulty must be 'easy', 'medium', or 'hard'")
            
            # Validate files
            self._validate_files(files)
            
            # Prepare files for upload
            upload_files = []
            for file_path in files:
                with open(file_path, 'rb') as f:
                    upload_files.append(('files', f))
                    
            params = {
                'numQuestions': num_questions,
                'difficulty': difficulty,
            }
            
            response = requests.post(
                f"{self.base_url}/upload",
                files=upload_files,
                params=params
            )
            
            if response.status_code != 200:
                raise NexusAPIError(response.text, response.status_code)
                
            return response.json()['data']
            
        except (NexusError, requests.RequestException) as e:
            if isinstance(e, requests.RequestException):
                raise NexusAPIError(str(e), getattr(e.response, 'status_code', None))
            raise
            
    def validate_answer(self, 
                        question: str, 
                        user_answer: str,
                        question_data: Dict) -> Dict:
        """
        Validate a user's answer against the generated correct answer.
        
        Args:
            question (str): The question text to validate against
            user_answer (str): The user's answer to validate
            question_data (Dict): The original question dictionary containing the correct answer
            
        Returns:
            Dict: JSON response containing:
                - result: "Correct" or "Incorrect"
                - explanation: Detailed explanation of why the answer is correct or incorrect
                
        Raises:
            NexusValidationError: If the input parameters are invalid
            NexusAPIError: If the API request fails
            NexusError: For other unexpected errors
        """
        try:
            # Validate input parameters
            if not question or not isinstance(question, str):
                raise NexusValidationError("question must be a non-empty string")
                
            if not user_answer or not isinstance(user_answer, str):
                raise NexusValidationError("user_answer must be a non-empty string")
                
            if not isinstance(question_data, dict) or 'correctAnswer' not in question_data:
                raise NexusValidationError("question_data must be a dictionary containing 'correctAnswer'")
            
            correct_answer = question_data['correctAnswer']
            
            payload = {
                'question': question,
                'correctAnswer': correct_answer,
                'userAnswer': user_answer
            }
            
            response = requests.post(
                f"{self.base_url}/validate-answer",
                json=payload
            )
            
            if response.status_code != 200:
                raise NexusAPIError(response.text, response.status_code)
                
            return response.json()
            
        except (NexusError, requests.RequestException) as e:
            if isinstance(e, requests.RequestException):
                raise NexusAPIError(str(e), getattr(e.response, 'status_code', None))
            raise
