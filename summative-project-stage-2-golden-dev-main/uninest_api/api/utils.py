# Import necessary modules from Django REST framework
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler to add status code to the response data.
    
    Args:
        exc: The exception object.
        context: Additional context information.
    
    Returns:
        Response object with modified data if an exception occurred, None otherwise.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If an exception was caught and handled
    if response is not None:
        # Add the status code to the response data
        response.data['status_code'] = response.status_code

    return response
