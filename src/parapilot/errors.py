"""Custom exception hierarchy for parapilot."""


class ParapilotError(Exception):
    """Base exception for all parapilot errors."""


class FileFormatError(ParapilotError):
    """Unsupported or unrecognized file format."""


class FieldNotFoundError(ParapilotError):
    """Requested field not found in dataset."""


class EmptyOutputError(ParapilotError):
    """Filter or operation produced empty output."""


class RenderError(ParapilotError):
    """Rendering operation failed."""
