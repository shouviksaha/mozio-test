from rest_framework.exceptions import APIException


class InvalidArgumentsException(APIException):
    status_code = 400
    default_detail = 'Invalid arguments'