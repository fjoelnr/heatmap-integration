import jsonschema

def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        print(f"Validation error: {err}")
        return False

__all__ = ['validate_json']


import jsonschema
from jsonschema import validate

# Beispielhafte JSON-Schema-Definition
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        print(f"Validation error: {err.message}")
        return False
