class NexusError(Exception):
    """Base exception class for Nexus SDK errors."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NexusAPIError(NexusError):
    """Exception raised for errors returned by the Nexus API."""
    def __init__(self, message: str, status_code: int):
        super().__init__(f"API Error ({status_code}): {message}", status_code)

class NexusFileError(NexusError):
    """Exception raised for file-related errors."""
    pass

class NexusValidationError(NexusError):
    """Exception raised for validation-related errors."""
    pass

class NexusConfigError(NexusError):
    """Exception raised for configuration errors."""
    pass
