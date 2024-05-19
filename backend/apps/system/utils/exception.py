from rest_framework.views import exception_handler
from .api_response import APIResponse
from rest_framework import status


def CustomExceptionHandler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            wait_seconds = getattr(exc, "wait", 0)
            message = f"请求过于频繁，请等待{wait_seconds}秒后重试"
            response.data = APIResponse(
                status=status.HTTP_429_TOO_MANY_REQUESTS, message=message
            ).data
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = APIResponse(
                status=status.HTTP_400_BAD_REQUEST, message=response.data["detail"]
            ).data
        if response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = APIResponse(
                status=status.HTTP_400_BAD_REQUEST, message=response.data["detail"]
            ).data

    return response
