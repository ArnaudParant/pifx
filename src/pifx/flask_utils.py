# External deps
import traceback
import logging
import json
from flask import Response, stream_with_context

# Internal deps
from pifx.utils import ApiException
import pifx.utils as utils

def stream_wrapper(generator):
    try:
        for raw in generator():
            yield raw
    except ApiException as exc:
        logging.error(str(exc))
        logging.error(traceback.format_exc())
        yield json.dumps({"error": exc.message})
    except Exception as exc:
        logging.error(str(exc))
        logging.error(traceback.format_exc())
        yield json.dumps({"error": "internal server error"})

def wrapper(action, mimetype="application/json", stream=False):
    status = 200
    try:
        raw_response = action()
        if not stream:
            if isinstance(raw_response, tuple):
                if len(raw_response) != 2:
                    raise ApiException("Invalid return tuple length")
                elif not isinstance(raw_response[1], int):
                    raise ApiException("Invalid return, status should be integer")
                else:
                    status = raw_response[1]
                    raw_response = raw_response[0]
            if mimetype == "application/json":
                raw_response = utils.obj_to_line(raw_response, suffix=None)
        if stream:
            raw_response = stream_with_context(stream_wrapper(raw_response))
    except ApiException as exc:
        logging.error(traceback.format_exc())
        mimetype = "application/json"
        raw_response = json.dumps({"error": exc.message})
        status = exc.status
    except Exception as exc:
        logging.error(traceback.format_exc())
        mimetype = "application/json"
        raw_response = json.dumps({"error": "internal server error"})
        status = 500
    return Response(raw_response, mimetype=mimetype, status=status)

def get_data(data):
    try:
        j = json.loads(data) if data else {}
        return {"duration": utils.to_float(j.get("duration", 0.8), "duration"),
                "wait": utils.to_boolean(j.get("wait", False), "wait")}
    except ApiException as exc:
        raise exc
    except ValueError:
        raise ApiException("Invalid input json")
