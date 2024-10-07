# Example usage in README.md:

### Python:
```
from nexussdk5 import HackathonNexusAPI

api = HackathonNexusAPI(api_key="your_gemini_api_key_here")

# Generate questions
files = ["path/to/file1.pdf", "path/to/file2.jpg"]
result = api.generate_questions(files, num_questions=5, difficulty="medium")
print(result)
```


# FOR Validate answer
```
validation = api.check_answer(
    question="What is the capital of France?", #Need to pass the generated questions here 
    correct_answer="Paris", #Correct answer here
    user_answer="London" #Pass user answer here too (The API will take care of the rest)
)
print(validation)
```


## Install with:
```
pip install nexussdk5
```
