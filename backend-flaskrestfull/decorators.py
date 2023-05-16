# Description: Decorators for the project
# Author: İbrahim Şamil Ceyişakar
# License: MIT license
# Date: 11 May 2023
# -----------------------------------------------------------------------------
# decorators.py
# -----------------------------------------------------------------------------

from functools import wraps


def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print("The client IP is: {}".format(kwargs["request"].environ["REMOTE_ADDR"]))
        # print("The client port is: {}".format(kwargs["request"].environ["REMOTE_PORT"]))
        print("preparing to call function")
        return f(*args, **kwargs)

    return decorated_function
