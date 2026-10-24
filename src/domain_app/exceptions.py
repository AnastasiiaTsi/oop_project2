class DomainError(Exception):
    """Base domain exception."""

class RecordValidationError(DomainError):
    """Raised when a record fails validation."""
    def __init__(self, message: str, *, line_number: int | None = None, field: str | None = None):
        super().__init__(message)
        self.line_number = line_number
        self.field = field