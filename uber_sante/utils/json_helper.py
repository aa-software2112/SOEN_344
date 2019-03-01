
from flask import jsonify
from enum import Enum

class ResponseReturnCode(Enum):
    CODE_200 = 200
    CODE_201 = 201
    CODE_400 = 400
    CODE_500 = 500


def create_json(data=None, message=None, return_code=ResponseReturnCode.CODE_200, as_tuple=True):
    """
    This is the ONLY method that should be called (do not call json_success or json_error)
    :param data: The data (raw, do not call __dict__() on it) to send in the json response
    :param message: The message to send to the front end
    :param return_code: The return code (using the ResponseReturnCode enum)
    :param as_tuple: True if the desired return is (json_response, return_code), False if desired
    return is ONLY json_response (see commend below)
    :return: A tuple of (json_response, ResponseReturnCode.value):

    For example, if data=None, Message=None, return_code=ResponseReturnCode.CODE_200, the returned
    value of this function would be

    ({
    data = null
    message = null
    status = "success"
    }, 200) --> Notice the first index of the tuple is the json response, and the second is the
    return code...

    If you wish to get the response without the return code, call create_json, with a final optional
    parameter as_tuple=False, then the returned value would be
    {
    data = null
    message = null
    status = "success"
    }

    """

    resp = None

    if (return_code == ResponseReturnCode.CODE_200 or return_code == ResponseReturnCode.CODE_201):
        resp = json_success(data, message, "success")
    else:
        resp = json_error(data, return_code.value, message, "error")

    # Allows external server to call this backend API
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
    resp.headers.add('Access-Control-Allow-Headers', 'Origin, Content-Type, X-Auth-Token')


    if as_tuple == True:
        return resp, return_code.value
    else:
        return resp


def json_success(data=None, message=None, status=None):

    return jsonify(data=format_data(data), message=message, status=status)

def json_error(data=None, error_code=None, message=None, status=None):
    '''
    Data passed, if a custom-class, should implement the __dict__() method
    :param data: The data to be sent - do not send it in formatted, it will
    be done by this method
    :param error_code: The desired error code as an integer or string
    :param message: The desired message to be displayed as a string
    :param status: The string status of the message, either "success", or "error"
    :return: The json responses with all data set
    '''
    return jsonify(data=format_data(data),
                   error={"code": error_code, "message": message},
                   status=status)



def format_data(data):
    """
    Takes some data and formats it for json-purposes: add to this method
    for each new format of data
    :param data:
    :return:
    """
    # Dictionary type - do something, return data
    if isinstance(data, dict):
        return data

    # List type - do something, return data
    if isinstance(data, list):
        return data

    # String type - do something, return data
    if isinstance(data, str):
        return data

    # integer or float type - do something, return data
    if isinstance(data, (int, float)):
        return data

    # Check that __dict__ method exists, and don't throw error if it doesn't (3rd param)
    method = getattr(data,"__dict__",None)

    # Method exists
    if not(method is None):

        # Get dictionary-formatted data for json output
        data = data.__dict__()

        return data

    return None
