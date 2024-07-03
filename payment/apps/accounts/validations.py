from validations.base import BaseError


class UniqueEmailValidation(BaseError):
    MESSAGE = "A user with this email already exists."
