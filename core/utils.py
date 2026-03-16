"""
Core utility functions for the project.
"""
from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_custom(model_class, pk, model_name="Object"):
    """
    Custom utility function to get an object or return a 404 response.
    
    Args:
        model_class: The Django model class to query
        pk: The primary key to look up
        model_name: The name of the model for the error message
        
    Returns:
        tuple: (object, None) if found, (None, Response) if not found
    """
    try:
        obj = model_class.objects.get(pk=pk)
        return obj, None
    except model_class.DoesNotExist:
        error_response = Response(
            {
                "error": f"{model_name} not found",
                "detail": f"{model_name} with id={pk} does not exist."
            },
            status=status.HTTP_404_NOT_FOUND
        )
        return None, error_response
