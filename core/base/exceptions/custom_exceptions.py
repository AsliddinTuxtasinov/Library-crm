from rest_framework import status, response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    resp = exception_handler(exc, context)

    if resp is not None:

        if isinstance(resp.data, dict):
            # If the response data is a dictionary, add the status code
            resp.data['status_code'] = resp.status_code

        elif isinstance(resp.data, list):
            # If the response data is a list, adjust the error format
            errors = []
            for error in resp.data:
                if isinstance(error, dict):
                    for key, messages in error.items():
                        # Flatten the list of messages into a single string for each key
                        if isinstance(messages, list) and len(messages) == 1:
                            errors.append({key: messages[0]})
                        else:
                            errors.append({key: messages})
                else:
                    errors.append({})  # Add an empty dictionary if the error is not a dict
            resp.data = {'status_code': resp.status_code, 'errors': errors}

        custom_response = {'errors': resp.data, 'success': False}
        return response.Response(data=custom_response, status=resp.status_code)
    else:
        # If response is None, provide a generic error response
        return response.Response(
            data={'success': False, 'errors': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
