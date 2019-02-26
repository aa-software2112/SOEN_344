
from . import controllers
from uber_sante.services.admin_service import AdminService
from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from flask import request

admin_service = AdminService()

@controllers.route('/loginAdmin', methods=['POST'])
def login_admin():
    """
    The endpoint for logging in as an administrator;
    This is necessary in order to register a doctor or a nurse -
    only an admin can do this
    """
    if request.method == 'POST':

        # User is already logged in (regardless of login-type {patient, admin, nurse, doctor})
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in",
                                  return_code=js.ResponseReturnCode.CODE_400)


        email = request.args.get('email')
        password = request.args.get('password')

        admin_id = admin_service.validate_login_info(email, password)

        if admin_id == -1:
            return js.create_json(data=None, message="Incorrect Admin Login information",
                                  return_code=js.ResponseReturnCode.CODE_400)

        resp = js.create_json(data=None, message="Logged in successfully",
                              return_code=js.ResponseReturnCode.CODE_200)
        resp = cookie_helper.set_user_logged(resp, admin_id,
                                             cookie_helper.UserTypes.ADMIN.value)

        return resp, js.ResponseReturnCode.CODE_200.value


