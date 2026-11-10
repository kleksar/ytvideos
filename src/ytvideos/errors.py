class WorkflowError(Exception):
    """An actionable contract violation, never an implicit permission to retry."""


class Conflict(WorkflowError):
    """The current state no longer matches the caller's inputs or lease."""


class CapabilityUnavailable(WorkflowError):
    """A required runtime capability has not been verified."""
