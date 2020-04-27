import re


def username_is_valid(value):
    """
    Check if value matches with expected string restrictions

    Returns True if value matches. If match failed, returns False instead
    """

    if re.compile('^[a-zA-Z0-9-_.]{5,12}$').match(value):
        return True
    
    return False
