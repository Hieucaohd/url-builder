from flask import  jsonify
import copy


def template(data, code=500):
    return {
        'message': {
            'errors': {
                'body': data
            },
            'status_code': code
        }
    }


UNKNOWN_ERROR = template([], code=500)
PARAM_KEY_NOT_FOUND_ERROR = template([], code=404)
PARAM_KEY_DUPLICATE_ERROR = template([], code=400)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def param_key_not_found(cls):
        return cls(**PARAM_KEY_NOT_FOUND_ERROR)

    @classmethod
    def param_key_duplicate_error(cls, keys_exist=None):
        if keys_exist:
            body = dict(key_duplicate_error=keys_exist)
            error_message = template(body, 400)
            return cls(**error_message)
        else:
            return cls(**PARAM_KEY_DUPLICATE_ERROR)

