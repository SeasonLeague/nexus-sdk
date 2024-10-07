import requests
import json
from typing import List, Dict, Union
import os

class HackathonNexusSDK:
    def __init__(self, api_key: str = None, base_url: str = "https://hackathon-nexus.onrender.com"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set it in the constructor or as an environment variable 'GEMINI_API_KEY'.")
        self.base_url = base_url

    def upload_files(self, files: List[str], num_questions: int, difficulty: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Upload files and generate questions.

        Args:
            files (List[str]): List of file paths to upload.
            num_questions (int): Number of questions to generate.
            difficulty (str): Difficulty level of the questions.

        Returns:
            Dict[str, Union[str, List[Dict[str, str]]]]: A dictionary containing preview and questions.
        """
        url = f"{self.base_url}/upload"
        params = {"numQuestions": num_questions, "difficulty": difficulty}
        files_data = [("files", (os.path.basename(file), open(file, "rb"))) for file in files]
        
        response = requests.post(url, params=params, files=files_data)
        response.raise_for_status()
        
        return response.json()["data"]

    def validate_answer(self, question: str, correct_answer: str, user_answer: str) -> Dict[str, str]:
        """
        Validate a user's answer.

        Args:
            question (str): The question text.
            correct_answer (str): The correct answer.
            user_answer (str): The user's answer.

        Returns:
            Dict[str, str]: A dictionary containing the result and explanation.
        """
        url = f"{self.base_url}/validate-answer"
        data = {
            "question": question,
            "correctAnswer": correct_answer,
            "userAnswer": user_answer
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        return response.json()

# API Service
class HackathonNexusAPI:
    def __init__(self, api_key: str = None):
        self.sdk = HackathonNexusSDK(api_key)

    def generate_questions(self, files: List[str], num_questions: int, difficulty: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Generate questions from uploaded files.

        Args:
            files (List[str]): List of file paths to upload.
            num_questions (int): Number of questions to generate.
            difficulty (str): Difficulty level of the questions.

        Returns:
            Dict[str, Union[str, List[Dict[str, str]]]]: A dictionary containing preview and questions.
        """
        return self.sdk.upload_files(files, num_questions, difficulty)

    def check_answer(self, question: str, correct_answer: str, user_answer: str) -> Dict[str, str]:
        """
        Check a user's answer.

        Args:
            question (str): The question text.
            correct_answer (str): The correct answer.
            user_answer (str): The user's answer.

        Returns:
            Dict[str, str]: A dictionary containing the result and explanation.
        """
        return self.sdk.validate_answer(question, correct_answer, user_answer)
