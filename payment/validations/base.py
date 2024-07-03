from rest_framework import serializers


class BaseError(Exception):
    MESSAGE = "Unknown error"

    @classmethod
    def raise_error(cls):
        raise serializers.ValidationError(cls.MESSAGE)

    @classmethod
    def to_json(cls):
        return {"error": cls.MESSAGE}
