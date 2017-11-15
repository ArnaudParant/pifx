import json

class ApiException(ValueError):
    def __init__(self, message, status=400):
        super(ApiException, self).__init__(message)
        self.message = message
        self.status = status

def obj_to_line(obj, ensure_ascii=False, encode="utf-8", prefix=None, suffix="\n"):
    if prefix is None:
        prefix = ""
    if suffix is None:
        suffix = ""
    return (prefix + json.dumps(obj, ensure_ascii=ensure_ascii) + suffix)

def to_boolean(string, name=None):
    string = str(string)
    if string == "0" or string.lower() == "false":
        return False
    if string == "1" or string.lower() == "true":
        return True
    if name is not None:
        name += ": "
    else:
        name = ""
    raise ApiException("%sInvalid boolean value: %s" % (name, string))

def to_float(string, name=None):
    string = str(string)
    try:
        return float(string)
    except ValueError:
        if name is not None:
            name += ": "
        else:
            name = ""
        raise ApiException("%sInvalid float value: %s" % (name, string))
