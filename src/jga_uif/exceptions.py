class IntegrityError(Exception):
    """Base error for integrity failures."""


class VerificationError(IntegrityError):
    """Raised when verification fails."""


class PolicyError(IntegrityError):
    """Raised when policy denies action."""


class TransitionError(IntegrityError):
    """Raised when state transition is invalid."""


class QuarantineRequiredError(IntegrityError):
    """Raised when object must be quarantined."""
