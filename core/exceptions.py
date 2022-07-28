from flask import  jsonify


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
KEY_NOT_FOUND = template([], code=404)


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
    def key_not_found(cls):
        return cls(**KEY_NOT_FOUND)

