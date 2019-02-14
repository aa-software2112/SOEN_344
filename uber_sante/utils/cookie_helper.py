from enum import Enum

class CookieKeys(Enum):
    LOGGED = "logged"
    PATIENT_ID = "patient_id"


def set_user_logged(response, patient_id):
    """
    Sets the cookie for a response object (will send this cookie to the
    user the response is sent to)
    :param response: The Flask Response object to embed the cookie into
    :param patient_id: The patient id to store in the cookie
    :return: The Response with the cookie attached
    """

    response.set_cookie(CookieKeys.PATIENT_ID.value, str(patient_id))
    response.set_cookie(CookieKeys.LOGGED.value, str(True))
    return response

def user_is_logged(request):
    """

    :param request: The request containing the user's cookie
    :return: True if user is logged, false otherwise
    """
    if request.cookies.get(CookieKeys.LOGGED.value) == "True":
        return True

    return False

def logout_user_cookie(response):
    """

    :param response: Sets the cookie logged status to false
    :return: response w/ user logged out
    """

    response.set_cookie(CookieKeys.LOGGED.value, str(False))
    return response
