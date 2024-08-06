import jsonschema

def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        print(f"Validation error: {err}")
        return False

__all__ = ['validate_json']
