# Example usage in README.md:
"""
## Error Handling

The Nexus SDK uses a comprehensive error handling system. Here are the different types of exceptions:

1. `NexusError`: Base exception class for all Nexus SDK errors
2. `NexusAPIError`: Raised for errors returned by the Nexus API
3. `NexusFileError`: Raised for file-related errors
4. `NexusValidationError`: Raised for validation-related errors
5. `NexusConfigError`: Raised for configuration errors

Example of handling different types of errors:

```python
from nexus import NexusSDK
from nexus.exceptions import NexusAPIError, NexusFileError, NexusValidationError

sdk = NexusSDK(api_key="your-api-key")

try:
    response = sdk.generate_questions(
        files=["document.pdf"],
        num_questions=5,
        difficulty="medium"
    )
except NexusFileError as e:
    print(f"File error: {e}")
except NexusValidationError as e:
    print(f"Validation error: {e}")
except NexusAPIError as e:
    print(f"API error (status {e.status_code}): {e}")
except NexusError as e:
    print(f"Other Nexus error: {e}")
```

This allows for fine-grained error handling in your applications.
"""