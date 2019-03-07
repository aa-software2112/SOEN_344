from enum import Enum

class CookieKeys(Enum):
    LOGGED = "logged"
    ID = "id"
    USER_TYPE = "user_type"
    USER_OBJ = "user_obj"

class UserTypes(Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    PATIENT = "patient"
    ADMIN = "admin"


def set_user_logged(response, id, user_type):
    """
    Sets the cookie for a response object (will send this cookie to the
    user the response is sent to)
    :param response: The Flask Response object to embed the cookie into
    :param patient_id: The patient id to store in the cookie
    :param user_type: "doctor", "nurse", or "patient", and should come from
    UserTypes.value --> To set a doctor, use UserTypes.DOCTOR.value as this parameter
    :return: The Response with the cookie attached
    """
    response.set_cookie(CookieKeys.USER_TYPE.value, user_type, domain="127.0.0.1:8084")
    response.set_cookie(CookieKeys.ID.value, str(id), domain="127.0.0.1:8084")
    response.set_cookie(CookieKeys.LOGGED.value, str(True), domain="127.0.0.1:8084")
    return response

def user_is_logged(request, as_user_type=None):
    """

    :param request: The request containing the user's cookie
    :param as_user_type: If selected (using UserTypes enum), makes sure
    that the user is logged in AS the type specified by the UserType
    :return: True if user is logged, false otherwise
    """
    if request.cookies.get(CookieKeys.LOGGED.value) == "True":

        if not as_user_type == None:
            return request.cookies.get(CookieKeys.USER_TYPE.value) == as_user_type.value
        else:
            return True

    return False

def logout_user_cookie(response):
    """

    :param response: Sets the cookie logged status to false
    :return: response w/ user logged out
    """

    response.set_cookie(CookieKeys.LOGGED.value, str(False))
    return response


