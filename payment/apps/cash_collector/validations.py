from validations.base import BaseError


class ValidateTaskId(BaseError):
    MESSAGE = "Task with this ID does not exist."


class ValidateAmountCollected(BaseError):
    MESSAGE = "Amount collected cannot be greater than amount due."


class CashCollectorFrozenError(BaseError):
    MESSAGE = "CashCollector is frozen and cannot collect more cash."
