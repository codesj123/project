from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_custom(model, **kwargs):
    """
    Fetch a single object by kwargs or raise a standardized 404 error dict.
    Returns (instance, error_response) tuple.
    """
    try:
        return model.objects.get(**kwargs), None
    except model.DoesNotExist:
        error = Response(
            {"error": f"{model.__name__} not found."},
            status=status.HTTP_404_NOT_FOUND
        )
        return None, error


def success_response(data, status_code=status.HTTP_200_OK):
    return Response(data, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    if isinstance(message, dict):
        return Response(message, status=status_code)
    return Response({"error": message}, status=status_code)
