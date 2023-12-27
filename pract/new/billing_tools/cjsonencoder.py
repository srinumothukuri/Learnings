import decimal
from flask import Flask , json
import datetime

class CustomJSONEncoder(Flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.__str__()
        elif isinstance(obj, bytes):
            val = int.from_bytes(obj, "little")
            return str(val)

        return super(CustomJSONEncoder, self).default(obj)
